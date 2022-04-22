"""
   ___                            _        _   _                   _                                        _          
  / __\___  _ __ ___  _ __  _   _| |_ __ _| |_(_) ___  _ __   __ _| |   ___  ___ ___  _ __   ___  _ __ ___ (_) ___ ___ 
 / /  / _ \| '_ ` _ \| '_ \| | | | __/ _` | __| |/ _ \| '_ \ / _` | |  / _ \/ __/ _ \| '_ \ / _ \| '_ ` _ \| |/ __/ __|
/ /__| (_) | | | | | | |_) | |_| | || (_| | |_| | (_) | | | | (_| | | |  __/ (_| (_) | | | | (_) | | | | | | | (__\__ \
\____/\___/|_| |_| |_| .__/ \__,_|\__\__,_|\__|_|\___/|_| |_|\__,_|_|  \___|\___\___/|_| |_|\___/|_| |_| |_|_|\___|___/
                     |_|                                                                                               

计算经济学数据处理工具箱 API
CE.PY
核心函数,包括返回处理、版本控制等

本页作者:
Aliebc (aliebcx@outlook.com)

Copyright(C)2022 All Rights reserved. 
"""

import json
import os
from django.http import HttpResponse, HttpResponseNotFound,JsonResponse,HttpRequest

ce_version_str="1.6.0 Debug"

class CEOptions(Exception):
    """
    Options处理
    """
    pass

class CERunningError(Exception):
    """
    CE错误类
    """
    pass

class CEResponse(HttpResponse):
    pass

def ret(code,data,err):
    """
    JSON返回函数v1
    """
    return {"respCode":code,"respData":data,"errMsg":err}

def ce_version(request:HttpRequest):
    """
    CE-API版本控制函数,给前端返回当前的CE-API版本
    """
    if(request.method not in ["POST","GET"]):
        return ret2(-1,"","Bad Method")
    return ret2(0,{"api_name":"CE API","version":ce_version_str},None)

def ce_not_found(request,e):
    return HttpResponseNotFound("Noe",status=404)

def ret2(
    code:int,
    data:dict,
    err:str) -> JsonResponse:
    """
    JSON返回函数v2
    核心返回函数,返回JsonReponse供Django进行处理
    """
    s_code=int(200)
    if err==None:
        s_code=200
    else:
        s_code=200
    return JsonResponse({
        "respCode":code,
        "respData":data,
        "errMsg":err
    },headers={
        'CE-VERSION':ce_version_str
    },status=s_code)

def ret_success(data)->JsonResponse:
    """
    成功返回函数
    """
    return ret2(0,data,None)

def ret_error(e)->JsonResponse:
    """
    错误返回函数
    """
    if(type(e)==CEOptions):
        return ret_success("OPTIONS")
    return ret2(-1,None,"Error"+repr(e))

def request_analyse(request:HttpRequest)->dict:
    """
    核心解析函数,从前端解析请求
    如果解析失败会报错
    """
    try:
        srcq=json.loads(request.body)
        return srcq
    except:
        raise CERunningError("JSON from web analyse Failed!")

def language(request:HttpRequest)->JsonResponse:
    """
    语言包处理函数
    """
    try:
        lang=json.loads(open(os.path.join('zyp','language.json'),encoding="utf-8").read())
        args=request_analyse(request)
        if args['language'] in lang:
            return ret_success({"Language":lang[args['language']]})
        else:
            raise CERunningError("Language Package not found!")
    except Exception as e:
        return ret_error(e)
