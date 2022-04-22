"""
   ___                            _        _   _                   _                                        _          
  / __\___  _ __ ___  _ __  _   _| |_ __ _| |_(_) ___  _ __   __ _| |   ___  ___ ___  _ __   ___  _ __ ___ (_) ___ ___ 
 / /  / _ \| '_ ` _ \| '_ \| | | | __/ _` | __| |/ _ \| '_ \ / _` | |  / _ \/ __/ _ \| '_ \ / _ \| '_ ` _ \| |/ __/ __|
/ /__| (_) | | | | | | |_) | |_| | || (_| | |_| | (_) | | | | (_| | | |  __/ (_| (_) | | | | (_) | | | | | | | (__\__ \
\____/\___/|_| |_| |_| .__/ \__,_|\__\__,_|\__|_|\___/|_| |_|\__,_|_|  \___|\___\___/|_| |_|\___/|_| |_| |_|_|\___|___/
                     |_|                                                                                               

计算经济学数据处理工具箱 API
FILER.PY
文件处理函数,提供所有文件相关处理的方法,以单个函数的方式提供
包括但不仅限于:
数据读取
数据写入

本页作者:
Aliebc (aliebcx@outlook.com)

Copyright(C)2022 All Rights reserved. 
"""

import os
import re
import time
import json
import hashlib
import pathlib
import pandas as pd
import platform
import threading
import multiprocessing
import gc
from django.http import HttpResponse,HttpRequest, JsonResponse
from .ce import CEOptions, request_analyse, ret2, ret_error, ret_success, CERunningError
from .configure import file_conf

MAX_LINES=1000
dtalist=multiprocessing.Manager().dict()

try:
    conf=file_conf
    file_dir_path=conf['file_path']
    image_path=conf['img_path']
    if(os.path.isdir(file_dir_path) and os.path.isdir(image_path)):
        print('Load config file successfully!')
    else:
        raise CERunningError("Cannot open and load the config file!")
except Exception as e:
    raise CERunningError("Cannot open and load the config file!")

def generate_uid(m_name='md5')->str:
    """
    UID生成函数
    """
    return str(hashlib.md5((str(m_name)+str(time.time())).encode("utf-8")).hexdigest()) #使用MD5生成唯一的UID

def rend1(request:HttpRequest)->HttpResponse:
    """
    内部测试页面主渲染函数
    """
    if(conf['api_domain'][-1]!='/'):
        conf['api_domain']+='/'
    skey={
        '__DOMAIN__':conf['api_domain'],
        '__YEAR__':time.strftime("%Y",time.localtime()),
        '__CET_VERSION__':'0.4.2',
        '__CDN_JQUERY__':'https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js',
        '__CDN_LAYER__':'https://www.layuicdn.com/layer-v3.5.1/layer.js',
        '__REGION__':'中国大陆地区'
    }  #参数替换列表
    html_src=open(os.path.join('zyp','render_main.source'),encoding="utf-8").read()
    html_str=html_src
    for key in skey:
        html_str=html_str.replace(key,skey[key])
    if request.method == 'GET':
        return HttpResponse(html_str)
    else:
        return ret2(-1,None,"Bad Method")

def recv_file(request:HttpRequest)->JsonResponse:
    if request.method == 'POST':
        if request.FILES:
            myf=None
            myf=request.FILES['file']
            if myf:
                uid=str(hashlib.md5((str(myf.name)+str(time.time())).encode("utf-8")).hexdigest())
                suffixinfo=str(pathlib.Path(str(myf.name)).suffix)
                name_x=re.match(r'^(.*).(xls|xlsx|dta|csv)$',myf.name)
                if not name_x:
                    return ret2(-1,None,"File type not allowed.")
                dest=open(os.path.join(file_dir_path,uid+suffixinfo),"wb+")
                for chunk in myf.chunks():
                    dest.write(chunk)
                dest.close()
                return ret_success({"f_name":myf.name,"f_suffix":suffixinfo,"uid":uid,"size":myf.size,"timestamp":int(time.time())})
            else:
                return ret2(-1,None,"File(file) field not found.")
        else:
            return ret2(-1,None,"Files field not found.")
    elif request.method=='OPTIONS':
        return ret_success("OPTIONS")
    else:
        print(request.method)
        return ret2(-1,None,"Only POST method is allowed.")

def check_memory():
    """
    内存巡查,启用一个线程每15秒检查并释放多余的内存
    """
    global dtalist
    while(True): #死循环
        n_time=int(time.time())
        dlist=[]
        for i in dtalist:
            if (n_time-dtalist[i]['time'])>600: #判断大于10分钟没有被使用过的内存
                dlist.append(i)
        for k in dlist:
            dtalist.pop(k)
        gc.collect() #内存回收
        time.sleep(15) #等待15秒

cmr=threading.Thread(target=check_memory) #启用线程
cmr.start()

def get_file_data(request:HttpRequest)->pd.DataFrame:
    """
    统一获取数据列表的函数,调用可以获得一个DataFrame
    """
    global dtalist
    if __name__ == 'zyp.filer' and platform.system()=='Linux': #判断是否Linux,对Linux启用多进程优化处理
        pread=multiprocessing.Process(target=get_file_data_src,args=(request,))
        pread.start()
        pread.join()
        fd=get_file_data_src(request)
    else:
        fd=get_file_data_src(request) #对Windows和MacOS使用普通的单进程处理
    return fd

def get_file_data_src(request:HttpRequest)->pd.DataFrame:
    """
    内部获取数据表函数
    """
    global dtalist
    if request.method in ['POST','GET']: 
        if request.method=='POST':
            try:
                rp=request_analyse(request)
                uid=rp['uid']
                f_suffix=rp['f_suffix']
            except Exception as e:
                uid=request.POST.get('uid',default=None)
                f_suffix=request.POST.get('f_suffix',default=None)
        else:
            try:
                uid=request.GET.get('uid',default=None)
                f_suffix=request.GET.get('f_suffix',default=None)
            except Exception as e:
                raise CERunningError("Bad Request")
        if uid and f_suffix:
            print("[CE-API LOG][%s]READ %s %s" % 
            (time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()),"d",uid))
            if uid in dtalist:
                dtalist[uid]['time']=int(time.time())
                return dtalist[uid]['df']
            f_name=str(uid)+str(f_suffix)
            f_path=os.path.join(file_dir_path,f_name)
            try:
                if f_suffix == '.xlsx': #判断后缀名,对不同的文件调用不同的处理方法
                    fdata=pd.read_excel(f_path,engine='openpyxl')
                elif f_suffix == '.xls':
                    fdata=pd.read_excel(f_path)
                elif f_suffix == '.dta':
                    fdata=pd.read_stata(f_path)
                elif f_suffix == '.csv':
                    fdata=pd.read_csv(f_path)
                else:
                    raise CERunningError("Suffix Error") #后缀名不对
                dtalist[uid]={'df':fdata,'time':int(time.time())}
                return fdata
            except Exception as e:
                raise CERunningError("Read Error") #文件不存在或读取格式错误导致读取失败
        else:
            raise CERunningError("Incomplete arguments") #不完整的参数 
    elif request.method=='OPTIONS':
        raise CEOptions("OPTIONS")
    else:
        raise CERunningError("Method Not allowed") #不允许的HTTP方法

def getd(request:HttpRequest)->JsonResponse:
    try:
        fdata=get_file_data(request)
        if fdata.shape[0]>MAX_LINES: #最大返回值
            fdata=fdata.head(MAX_LINES)
        return ret_success({
            "DataList":json.loads(fdata.to_json(orient='records')), #数据表转JSON
            "Type":json.loads(fdata.dtypes.to_json())})
    except Exception as e:
        return ret_error(e)

def ret_file(request:HttpRequest)->HttpResponse:
    """
    HTTP处理函数:文件下载处理,给前端返回对应的请求数据文件
    """
    try:
        if request.method == 'POST':
            rp=json.loads(request.body)
            uid=rp['uid']
            f_suffix=rp['f_suffix']
        elif request.method == 'GET':
            uid=request.GET.get('uid')
            f_suffix=request.GET.get('f_suffix')
        f_name=str(uid)+str(f_suffix)
        f_path=os.path.join(file_dir_path,f_name)
        f_cont=open(f_path,'rb').read()
    except Exception as e:
        return ret_error(e)
    return HttpResponse(f_cont,headers={
        'Content-Type':'application/octet-stream',
        'Content-Length':str(len(f_cont)),
        "Content-Disposition":"attachment ;filename="+f_name}) #文件下载

def del_file(request:HttpRequest)->JsonResponse :
    """
    HTTP处理函数:删除前端请求的文件
    """
    try:
        if request.method == 'POST':
            rp=json.loads(request.body)
            uid=rp['uid']
            f_suffix=rp['f_suffix']
        elif request.method == 'GET':
            uid=request.GET.get('uid')
            f_suffix=request.GET.get('f_suffix')
        f_name=str(uid)+str(f_suffix)
        f_path=os.path.join(file_dir_path,f_name)
        os.remove(f_path) #从磁盘中删除文件
        global dtalist
        del dtalist[uid]
        gc.collect() #回收对应的内存
    except Exception as e:
        return ret2(-1,None,"Error(#1):Type")
    return ret_success("Your data has been deleted.")

def put_file_excel(df,ind=False,index_label=None)->str:
    """
    封装好的数据表转文件函数
    """
    uid=generate_uid()
    f_name=os.path.join(file_dir_path,uid+".xlsx")
    df.to_excel(f_name,index=ind,sheet_name="CE-API",index_label=index_label) #分别控制表名、索引导出
    return uid

def put_file_all(df,f_suffix):
    """
    通用的封装好的数据表转文件函数(对应所有后缀名)
    """
    uid=generate_uid()
    f_name=os.path.join(file_dir_path,uid+f_suffix)
    if f_suffix == '.xlsx':
        df.to_excel(f_name,index=False,sheet_name="CE-API",index_label=None)
    elif f_suffix == '.dta':
        df.to_stata(f_name,write_index=False)
    elif f_suffix == '.xls':
        df.to_excel(f_name,index=False,sheet_name="CE-API",index_label=None)
    elif f_suffix == '.csv':
        df.to_csv(f_name,index=False)
    return uid

def switch_file_type(request:HttpRequest)->JsonResponse:
    """
    HTTP处理:数据类型转换函数
    """
    try:
        dta1=get_file_data(request)
        args=request_analyse(request)
        uid2=put_file_all(dta1,args['argu1'])
        return ret_success({
            "uid":uid2,
            "f_suffix":args['argu1']})
    except Exception as e:
        return ret_error(e)