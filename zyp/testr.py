import json
import pandas as pd
import numpy as npy
import scipy.stats as st
from django.http import HttpResponse,JsonResponse
from . import ce
from . import filer

def meant(request):
    try:
        dta = filer.get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        try:
            pval=st.ttest_ind(dta[argu1],dta[argu2]).pvalue
            return JsonResponse(ce.ret(0,{'pvalue':pval},None))
        except Exception as e:
            return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
    except Exception as e:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Req)."))