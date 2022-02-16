import os
import re
import time
import json
import hashlib
import pathlib
import pandas as pd
from django.http import HttpResponse,JsonResponse
from . import ce

try:
    conf=json.loads(open(os.path.join('zyp','config.json'),encoding="utf-8").read())
    file_dir_path=conf['file_path']
    image_path=conf['img_path']
    if(os.path.isdir(file_dir_path) and os.path.isdir(image_path)):
        print('Load config file successfully!')
    else:
        raise RuntimeError("Cannot open and load the config file!")
except:
    raise RuntimeError("Cannot open and load the config file!")

def generate_uid(m_name='md5'):
    return str(hashlib.md5((str(m_name)+str(time.time())).encode("utf-8")).hexdigest())

def rend1(request):
    if(conf['api_domain'][-1]!='/'):
        conf['api_domain']+='/'
    skey={
        '__DOMAIN__':conf['api_domain'],
        '__YEAR__':time.strftime("%Y",time.localtime()),
        '__CET_VERSION__':'0.4.1',
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
        return JsonResponse(ce.ret(-1,None,"Bad Method"))

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
                    return JsonResponse(ce.ret(-1,None,"File type not allowed."))
                dest=open(os.path.join(file_dir_path,uid+suffixinfo),"wb+")
                for chunk in myf.chunks():
                    dest.write(chunk)
                dest.close()
                return JsonResponse(ce.ret(0,{"f_name":myf.name,"f_suffix":suffixinfo,"uid":uid,"size":myf.size,"timestamp":int(time.time())},None))
            else:
                return JsonResponse(ce.ret(-1,None,"File(file) field not found."))
        else:
            return JsonResponse(ce.ret(-1,None,"Files field not found."))
    else:
        return JsonResponse(ce.ret(-1,None,"Only POST method is allowed."))

def get_file_data(request):
    if request.method in ['POST','GET']: 
        if request.method=='POST':
            try:
                rp=json.loads(request.body)
                uid=rp['uid']
                f_suffix=rp['f_suffix']
            except:
                uid=request.POST.get('uid',default=None)
                f_suffix=request.POST.get('f_suffix',default=None)
        else:
            try:
                uid=request.GET.get('uid',default=None)
                f_suffix=request.GET.get('f_suffix',default=None)
            except:
                raise RuntimeError("Bad Request")
        if uid and f_suffix:
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
                    #f_sep=request.POST.get("f_sep",default=None)
                    fdata=pd.read_csv(f_path)
                else:
                    raise RuntimeError("Suffix Not allowed")
                return fdata
            except:
                raise RuntimeError("Read Error")
        else:
            raise RuntimeError("Suffix Not allowed")
    else:
        raise RuntimeError("Method Not allowed")

def getd(request):
    if request.method == 'POST':
        try:
            rp=json.loads(request.body)
            uid=rp['uid']
            f_suffix=rp['f_suffix']
        except:
            return JsonResponse(ce.ret(-1,None,"Error(#1:Format)."))
        if uid and f_suffix:
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
                    return JsonResponse(ce.ret(-1,None,"Error(#2:Suffix)."))
                if fdata.shape[0]>1000:
                    fdata=fdata.head(1000)
                return JsonResponse(ce.ret(0,{"DataList":json.loads(fdata.to_json(orient='records'))},None))
            except:
                return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
        else:
            return JsonResponse(ce.ret(-1,None,"Error(#1:Format)."))
    else:
        return JsonResponse(ce.ret(-1,None,"Only POST method is allowed."))

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
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#1):Type"))
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
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#1):Type"))
    return JsonResponse(ce.ret(0,"Your data has been deleted.",None))

def put_file_excel(df):
    uid=generate_uid()
    f_name=os.path.join(file_dir_path,uid+".xlsx")
    df.to_excel(f_name,index=False,sheet_name="CE-API")
    return uid