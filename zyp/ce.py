from email import header
import os
import time
import json
import math
import pandas as pd
import numpy as npy
from django.http import HttpResponse,JsonResponse

ce_version_str="1.1.5 Debug"

def ret(code,data,err):
    return {"respCode":code,"respData":data,"errMsg":err}

def ce_version(request):
    if(request.method not in ["POST","GET"]):
        return JsonResponse(ret(-1,"","Bad Method"))
    return JsonResponse(ret(0,{"api_name":"CE API","version":ce_version_str},None))

def ce_not_found(request):
    return JsonResponse(ret(-1,None,"Not Found"))

def test(request):
    df2 = pd.DataFrame({"Distance": [1,2,3], 'Force': [4,5.5,6], 'yerr': [0.1, 0.5, 3]})
    df2.to_excel('/opt/rrr.xlsx')
    rp=HttpResponse(open('/opt/rrr.xlsx','rb').read(),headers={'Content-Type':'application/octet-stream','Content-Disposition':'attachment;filename=test.xlsx'})
    return rp