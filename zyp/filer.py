import os
import re
import time
import json
import math
import hashlib
import pathlib
import pandas as pd
import numpy as npy
from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from . import ce


file_dir_path="/opt/zypfile"

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
                return JsonResponse(ce.ret(-1,None,"Error(#1:Format)."))
        else:
            try:
                uid=request.GET.get('uid',default=None)
                f_suffix=request.GET.get('f_suffix',default=None)
            except:
                return JsonResponse(ce.ret(-1,None,'Error(#1:Format).'))
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
                    return JsonResponse(ce.ret(-1,None,"Error(#2:Suffix)."))
                return fdata
            except:
                return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
        else:
            return JsonResponse(ce.ret(-1,None,"Error(#1:Format)."))
    else:
        return JsonResponse(ce.ret(-1,None,"Only POST method is allowed."))

def getd(request):
    if request.method == 'POST':
        try:
            rp=json.loads(request.body)
            uid=rp['uid']
            f_suffix=rp['f_suffix']
        except:
            return JsonResponse(ce.ret(-1,None,"Error(#1:Format)."))
        #uid=request.POST.get("uid",default=None)
        #f_suffix=request.POST.get("f_suffix",default=None)
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
                    return JsonResponse(ce.ret(-1,None,"Error(#2:Suffix)."))
                return JsonResponse(ce.ret(0,{"DataList":json.loads(fdata.to_json(orient='records'))},None))
            except:
                return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
        else:
            return JsonResponse(ce.ret(-1,None,"Error(#1:Format)."))
    else:
        return JsonResponse(ce.ret(-1,None,"Only POST method is allowed."))


def imgtest(request):
    sv=open("/opt/test/t2.svg","r").read()
    return HttpResponse(sv,content_type="image/svg+xml")