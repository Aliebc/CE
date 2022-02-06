from email.policy import default
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
from . import datac
from . import filer
from plotnine import *

image_path="/opt/zypimg"
right="<!--This image is created by computational economics project by Aliebc, Tsinghua University(E-mail:ad_xyz@outlook.com).-->\n"

def sav_and_ret_svg(img,width,height):
    img_uid=str(hashlib.md5((str(time.time())).encode("utf-8")).hexdigest())
    f_name=img_uid+".svg"
    img.save(os.path.join(image_path,f_name),format="svg",width=width,height=height)
    img_file=open(os.path.join(image_path,f_name),'r')
    img_cont=img_file.readline()+right+"<!--Image tuid:"+img_uid+"-->\n"+img_file.read()
    res=HttpResponse(img_cont,headers={'Content-Type':'image/svg+xml','image-tuid':img_uid})
    return res

def ret_svg_tuid(request):
    try:
        img_uid=request.GET.get('tuid')
    except:
        return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
    return None


def density(request):
    if request.method =='GET':
        try:
            dta=filer.get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            title=request.GET.get('title',default=str("Density of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        img_density=(ggplot(dta,aes(x=argu1))+geom_density()+ggtitle(title))
        return sav_and_ret_svg(img_density,width,height)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))


def hist(request):
    if request.method =='GET':
        try:
            dta=filer.get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            title=request.GET.get('title',default=str("Density of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        img_density=(ggplot(dta,aes(x=argu1))+geom_histogram()+ggtitle(title)+theme(text=element_text(family='SimHei')))
        return sav_and_ret_svg(img_density,width,height)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))


def hetero_density(request):
    if request.method =='GET':
        try:
            dta=filer.get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu_type=request.GET.get('argu_type',default=None)
            title=request.GET.get('title',default=str("Density of "+argu1))
            width=int(request.GET.get('width',default=12))
            segment=int(request.GET.get('segment',default=None))
            height=int(request.GET.get('height',default=8))
        except:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        try:
            dta2=datac.heter_compare_df(dta,argu_type,float(segment))
            img_density=(ggplot(dta2,aes(x=argu1,colour=argu_type+'_type'))+geom_density()+ggtitle(title))
        except:
            return JsonResponse(ce.ret(-1,None,'Error(#4):Plot.'))
        return sav_and_ret_svg(img_density,width,height)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))

def type_density(request):
    if request.method =='GET':
        try:
            dta=filer.get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu2=request.GET.get('argu2',default=None)
            title=request.GET.get('title',default=str("Density of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        img_density=(ggplot(dta,aes(x=argu1,colour=argu2))+geom_density()+ggtitle(title))
        return sav_and_ret_svg(img_density,width,height)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))


def type_regress(request):
    if request.method =='GET':
        try:
            dta=filer.get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu2=request.GET.get('argu2',default=None)
            argu_type=request.GET.get('argu_type',default=None)
            title=request.GET.get('title',default=str("Density of "+argu1))
            width=int(request.GET.get('width',default=12))
            segment=int(request.GET.get('segment',default=None))
            height=int(request.GET.get('height',default=8))
        except:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        try:
            dta2=datac.heter_compare_df(dta,argu_type,float(segment))
            img_density=(ggplot(dta2,aes(x=argu1,y=argu2,colour=argu_type+'_type'))+geom_smooth(method='lm')+geom_point()+ggtitle(title))
        except:
            return JsonResponse(ce.ret(-1,None,'Error(#4):Plot.'))
        return sav_and_ret_svg(img_density,width,height)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))

def two_reg(request):
    if request.method =='GET':
        try:
            dta=filer.get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu2=request.GET.get('argu2',default=None)
            title=request.GET.get('title',default=str("Density of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        try:
            img_density=(ggplot(dta,aes(x=argu1,y=argu2))+geom_smooth(method='lm')+geom_point(fill='blue')+ggtitle(title))
        except:
            return JsonResponse(ce.ret(-1,None,'Error(#4):Plot.'))
        return sav_and_ret_svg(img_density,width,height)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))