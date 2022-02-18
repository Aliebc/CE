import os
from django.http import HttpResponse,JsonResponse
from . import ce
from .ce import ret2,ret_error,ret_success
from .datac import heter_compare_df
from .filer import get_file_data,generate_uid,image_path
from plotnine import *

right="<!--This image is created by computational economics project(CE-API) by Aliebc, Tsinghua University(E-mail:ad_xyz@outlook.com).-->\n"

def sav_svg(img,width,height):
    img_uid=generate_uid()
    f_name=img_uid+".svg"
    img.save(os.path.join(image_path,f_name),format="svg",width=width,height=height)
    return img_uid


def sav_and_ret_svg(img,width,height,request=None):
    img_uid=generate_uid()
    f_name=img_uid+".svg"
    img.save(os.path.join(image_path,f_name),format="svg",width=width,height=height)
    img_file=open(os.path.join(image_path,f_name),'r')
    img_cont=img_file.readline()+right+"<!--Image tuid:"+img_uid+"-->\n"+img_file.read()
    if request:
        try:
            if request.GET.get('dl',default=None)=='1':
                res=HttpResponse(img_cont,headers={'Content-Type':'application/octet-stream','image-tuid':img_uid,"Content-Disposition":"attachment ;filename="+img_uid+".svg"})
            else:
                res=HttpResponse(img_cont,headers={'Content-Type':'image/svg+xml','image-tuid':img_uid})
        except Exception as e:
            res=HttpResponse(img_cont,headers={'Content-Type':'image/svg+xml','image-tuid':img_uid})
    else:
        res=HttpResponse(img_cont,headers={'Content-Type':'image/svg+xml','image-tuid':img_uid})
    return res

def ret_svg_tuid(request):
    try:
        img_uid=request.GET.get('tuid')
    except Exception as e:
        return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
    return None


def density(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            title=request.GET.get('title',default=str("Density of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        img_density=(ggplot(dta,aes(x=argu1))+geom_density()+ggtitle(title))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        try:
            dta=get_file_data(request)
            argu1=request.POST.get('argu1',default=None)
            title=request.POST.get('title',default=str("Density of "+argu1))
            width=int(request.POST.get('width',default=12))
            height=int(request.POST.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        img_density=(ggplot(dta,aes(x=argu1))+geom_density()+ggtitle(title))
        return JsonResponse(ce.ret(0,{'tuid':sav_svg(img_density,width,height)},None))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))


def hist(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            title=request.GET.get('title',default=str("Histogram of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        img_density=(ggplot(dta,aes(x=argu1))+geom_histogram()+ggtitle(title)+theme(text=element_text(family='SimHei')))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))

def cdf(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            title=request.GET.get('title',default=str("CDF of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        img_density=(ggplot(dta,aes(x=argu1))+stat_ecdf()+ggtitle(title)+theme(text=element_text(family='SimHei')))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))


def hetero_density(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu_type=request.GET.get('argu_type',default=None)
            title=request.GET.get('title',default=str("Heterogeneity Density of "+argu1))
            width=int(request.GET.get('width',default=12))
            segment=float(request.GET.get('segment',default=None))
            height=int(request.GET.get('height',default=8))+'_type'
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        try:
            dta2=heter_compare_df(dta,argu_type,float(segment))
            img_density=(ggplot(dta2,aes(x=argu1,colour=argu_type+'_type'))+geom_density()+ggtitle(title))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#4):Plot.'))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))

def type_density(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu2=request.GET.get('argu2',default=None)
            title=request.GET.get('title',default=str("Type Density of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        img_density=(ggplot(dta,aes(x=argu1,colour=argu2))+geom_density()+ggtitle(title))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))


def type_regress(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu2=request.GET.get('argu2',default=None)
            argu_type=request.GET.get('argu_type',default=None)
            title=request.GET.get('title',default=str("Regression of "+argu1+ " ~ "+argu2))
            width=int(request.GET.get('width',default=12))
            segment=float(request.GET.get('segment',default=None))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        try:
            dta2=heter_compare_df(dta,argu_type,float(segment))
            img_density=(ggplot(dta2,aes(x=argu1,y=argu2,colour=argu_type+'_type'))+geom_smooth(method='lm')+geom_point()+ggtitle(title))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#4):Plot.'))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))

def two_reg(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu2=request.GET.get('argu2',default=None)
            title=request.GET.get('title',default=str("Regression of "+argu2+" ~ "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        try:
            img_density=(ggplot(dta,aes(x=argu1,y=argu2))+geom_smooth(method='lm')+geom_point(fill='blue')+ggtitle(title))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#4):Plot.'))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))

def two_reg_d2(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu2=request.GET.get('argu2',default=None)
            title=request.GET.get('title',default=str("Regression of "+argu2+" ~ "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        try:
            img_density=(ggplot(dta,aes(x=argu1,y=argu2))+geom_smooth(method='lm',formula='y~pow(x,2)')+geom_point(fill='blue')+ggtitle(title))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#4):Plot.'))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))

def two_line(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu2=request.GET.get('argu2',default=None)
            title=request.GET.get('title',default=str("Broken line of "+argu2+" ~ "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        try:
            img_density=(ggplot(dta,aes(x=argu1,y=argu2,group=1))+geom_line()+geom_point(fill='blue')+ggtitle(title))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#4):Plot.'))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))

def type_bar(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            argu2=request.GET.get('argu2',default=None)
            title=request.GET.get('title',default=str("Bar of mean("+argu1+") with type of "+argu2))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,'Error(#3):Request.'))
        dta2=dta.groupby([argu2]).mean().reset_index()
        dta3=dta.groupby([argu2]).std().reset_index()
        dta2['errbar_max']=dta2[argu1]+dta3[argu1]
        dta2['errbar_min']=dta2[argu1]-dta3[argu1]
        img_density=(ggplot(dta2,aes(x=argu2,y=argu1,fill=argu2))+geom_bar(stat = 'identity')+geom_errorbar(aes(ymax='errbar_max',ymin='errbar_min'))+ggtitle(title))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))

def tuid(request):
    return None

def qqplot(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            title=request.GET.get('title',default=str("QQ-Plot of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return ret2(-1,None,'Error(#3):Request.')
        try:
            img_density=(ggplot(dta,aes(sample=argu1))+stat_qq()+stat_qq_line()+ggtitle(title))
        except Exception as e:
            return ret2(-1,None,'Error(#4):Plot.')
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return ret2(-1,None,'Method Not Allowed.')
    else:
        return ret2(-1,None,'Method Not Allowed.')

def plot_advance(request):
    if request.method =='GET':
        try:
            dta=get_file_data(request)
            argu1=request.GET.get('argu1',default=None)
            title=request.GET.get('title',default=str("QQ-Plot of "+argu1))
            width=int(request.GET.get('width',default=12))
            height=int(request.GET.get('height',default=8))
        except Exception as e:
            return ret2(-1,None,'Error(#3):Request.')
        try:
            img_density=eval('('+argu1+')')
        except Exception as e:
            return ret2(-1,None,'Error(#4):'+repr(e))
        return sav_and_ret_svg(img_density,width,height,request)
    elif request.method =='POST':
        return ret2(-1,None,'Method Not Allowed.')
    else:
        return ret2(-1,None,'Method Not Allowed.')