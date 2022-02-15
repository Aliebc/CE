from django.http import HttpResponseNotFound,JsonResponse

ce_version_str="1.1.7 Debug"

def ret(code,data,err):
    return {"respCode":code,"respData":data,"errMsg":err}

def ce_version(request):
    if(request.method not in ["POST","GET"]):
        return JsonResponse(ret(-1,"","Bad Method"))
    return JsonResponse(ret(0,{"api_name":"CE API","version":ce_version_str},None))

def ce_not_found(request,e):
    return HttpResponseNotFound("Noe",status=404)

def ret2(code,data,err):
    return JsonResponse({"respCode":code,"respData":data,"errMsg":err})