import os
import re
import time
import json
import math
from pandas import DataFrame
import hashlib
import pathlib
import pandas as pd
import numpy as npy
from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from . import ce
from . import filer
from numpy import mean, median, var, std

def dsummary(request):
    try:
        argu1=request.POST.get('argu1')
        dta=filer.get_file_data(request)
        return HttpResponse(mean(dta[argu1]))
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
    return 1

def dcorr(request):
    try:
        dta=filer.get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        cord=DataFrame(dta).corr()
        d=cord.to_json()
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
    return JsonResponse(ce.ret(0,json.loads(d),None))

def dtype(request):
    try:
        dta=filer.get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        retu=dta[argu1]
        #print(retu.value_counts().to_json())
        return JsonResponse(ce.ret(0,json.loads(retu.value_counts().to_json()),None))
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
    return 0

def dhist(request):
    try:
        dta=filer.get_file_data(request)

    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
    return HttpResponse("dhist")

