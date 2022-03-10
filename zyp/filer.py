import os
import re
import time
import json
import hashlib
import pathlib
import pandas as pd
import threading
from django.http import HttpResponse
from .ce import ret2,ret_error

MAX_LINES=1000
dtalist={}

try:
    conf=json.loads(open(os.path.join('zyp','config.json'),encoding="utf-8").read())
    file_dir_path=conf['file_path']
    image_path=conf['img_path']
    if(os.path.isdir(file_dir_path) and os.path.isdir(image_path)):
        print('Load config file successfully!')
    else:
        raise RuntimeError("Cannot open and load the config file!")
except Exception as e:
    raise RuntimeError("Cannot open and load the config file!")

def generate_uid(m_name='md5'):
    return str(hashlib.md5((str(m_name)+str(time.time())).encode("utf-8")).hexdigest())

def rend1(request):
    if(conf['api_domain'][-1]!='/'):
        conf['api_domain']+='/'
    skey={
        '__DOMAIN__':conf['api_domain'],
        '__YEAR__':time.strftime("%Y",time.localtime()),
        '__CET_VERSION__':'0.4.2',
        '__CDN_JQUERY__':'https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js',
        '__CDN_LAYER__':'https://www.layuicdn.com/layer-v3.5.1/layer.js',
        '__REGION__':'中国大陆地区'
    }
    html_src=open(os.path.join('zyp','render_main.source'),encoding="utf-8").read()
    html_str=html_src
    for key in skey:
        html_str=html_str.replace(key,skey[key])
    if request.method == 'GET':
        return HttpResponse(html_str)
    else:
        return ret2(-1,None,"Bad Method")

def recv_file(request):
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
                return ret2(0,{"f_name":myf.name,"f_suffix":suffixinfo,"uid":uid,"size":myf.size,"timestamp":int(time.time())},None)
            else:
                return ret2(-1,None,"File(file) field not found.")
        else:
            return ret2(-1,None,"Files field not found.")
    else:
        return ret2(-1,None,"Only POST method is allowed.")

def check_memory():
    global dtalist
    while(True):
        n_time=int(time.time())
        dlist=[]
        for i in dtalist:
            if int(n_time-dtalist[i]['time'])>300:
                dlist.append(i)
        for k in dlist:
            dtalist.pop(k)
        time.sleep(15)

cmr=threading.Thread(target=check_memory)
cmr.start()

def get_file_data(request):
    global dtalist
    if request.method in ['POST','GET']: 
        if request.method=='POST':
            try:
                rp=json.loads(request.body)
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
                raise RuntimeError("Bad Request")
        if uid and f_suffix:
            if uid in dtalist:
                dtalist[uid]['time']=int(time.time())
                return dtalist[uid]['df']
            f_name=str(uid)+str(f_suffix)
            f_path=os.path.join(file_dir_path,f_name)
            try:
                if f_suffix == '.xlsx':
                    fdata=pd.read_excel(f_path,engine='openpyxl')
                elif f_suffix == '.xls':
                    fdata=pd.read_excel(f_path)
                elif f_suffix == '.dta':
                    fdata=pd.read_stata(f_path)
                elif f_suffix == '.csv':
                    fdata=pd.read_csv(f_path)
                else:
                    raise RuntimeError("Suffix Error")
                dtalist[uid]={'df':fdata,'time':int(time.time())}
                return fdata
            except Exception as e:
                raise RuntimeError("Read Error")
        else:
            raise RuntimeError("Incomplete arguments")
    else:
        raise RuntimeError("Method Not allowed")

def getd(request):
    try:
        fdata=get_file_data(request)
        if fdata.shape[0]>MAX_LINES:
            fdata=fdata.head(MAX_LINES)
        return ret2(0,{"DataList":json.loads(fdata.to_json(orient='records')),"Type":json.loads(fdata.dtypes.to_json())},None)
    except Exception as e:
        ret_error(e)

def ret_file(request):
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
    return HttpResponse(f_cont,headers={'Content-Type':'application/octet-stream',"Content-Disposition":"attachment ;filename="+f_name})

def del_file(request):
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
        os.remove(f_path)
    except Exception as e:
        return ret2(-1,None,"Error(#1):Type")
    return ret2(0,"Your data has been deleted.",None)

def put_file_excel(df,ind=False,index_label=None):
    uid=generate_uid()
    f_name=os.path.join(file_dir_path,uid+".xlsx")
    df.to_excel(f_name,index=ind,sheet_name="CE-API",index_label=index_label)
    return uid