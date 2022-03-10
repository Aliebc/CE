import json
import os
from django.http import HttpResponseNotFound,JsonResponse

ce_version_str="1.4.0 Pre-Release"

def ret(code,data,err):
    return {"respCode":code,"respData":data,"errMsg":err}

def ce_version(request):
    if(request.method not in ["POST","GET"]):
        return ret2(-1,"","Bad Method")
    return ret2(0,{"api_name":"CE API","version":ce_version_str},None)

def ce_not_found(request,e):
    return HttpResponseNotFound("Noe",status=404)

def ret2(code,data,err):
    return JsonResponse({"respCode":code,"respData":data,"errMsg":err})

def ret_success(data):
    return ret2(0,data,None)

def ret_error(e):
    return ret2(-1,None,"Error"+repr(e))

def request_analyse(request):
    try:
        srcq=json.loads(request.body)
        return srcq
    except:
        raise RuntimeError("JSON analyse Failed!")

def language(request):
    try:
        lang=json.loads(open(os.path.join('zyp','language.json'),encoding="utf-8").read())
        args=request_analyse(request)
        if args['language'] in lang:
            return ret_success({"Language":lang[args['language']]})
        else:
            raise RuntimeError("Language Package not found!")
    except Exception as e:
        return ret_error(e)
