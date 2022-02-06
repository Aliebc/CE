import os
import time
import json
import math
import pandas as pd
import numpy as npy
from django.http import HttpResponse,JsonResponse


def calc_corr(a, b):
	a_avg = sum(a)/len(a)
	b_avg = sum(b)/len(b)
	cov_ab = sum([(x - a_avg)*(y - b_avg) for x,y in zip(a, b)])
	sq = math.sqrt(sum([(x - a_avg)**2 for x in a])*sum([(x - b_avg)**2 for x in b]))
	corr_factor = cov_ab/sq
	return corr_factor

def ret(code,data,err):
    return {"respCode":code,"respData":data,"errMsg":err}

def ce_main(request):
    if(request.method!="POST"):
        return JsonResponse(ret(-1,"","Only POST Method allowed."))
    ip={"respCode":0,"respData":request.environ['HTTP_X_FORWARDED_FOR'],"errMsg":""}
    ip=json.dumps(ip)
    y=request.GET.get("rrr",default="No")
    y=request.POST.get("rrr",default="No")
    z=request.environ['HTTP_X_FORWARDED_FOR']
    return JsonResponse(ret(0,request.environ['HTTP_X_FORWARDED_FOR'],None))

def ce_not_found(request):
    return JsonResponse(ret(-1,None,"Not Found"))