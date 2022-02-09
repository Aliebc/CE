import os
import re
import time
import json
from pandas import DataFrame
import hashlib
import pathlib
import pandas as pd
import numpy as npy
import scipy.stats as st
from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from . import ce
from . import filer
from numpy import mean, median, pv, var, std
import statsmodels.api as sm
from scipy.stats import ttest_ind

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
        c2=st.pearsonr(dta[argu1],dta[argu2])
        cord=DataFrame(dta).corr()
        d=cord.to_json()
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
    return JsonResponse(ce.ret(0,{"CorrMartix":json.loads(d),"Significance":c2},None))

def dtype(request):
    try:
        dta=filer.get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        retu=dta[argu1]
        #print(retu.value_counts().to_json())
        return JsonResponse(ce.ret(0,json.loads(retu.value_counts().to_json()),None))
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))

def dhist(request):
    try:
        dta=filer.get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        count=int(json.loads(request.body)['count'])
        retu=dta[argu1]
        return JsonResponse(ce.ret(0,json.loads(pd.cut(retu,count).value_counts().to_json()),None))
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))

def dsummary(request):
    try:
        dta=filer.get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        retu=dta[argu1]
        return JsonResponse(ce.ret(0,json.loads(retu.describe().to_json()),None))
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))

def dlm3(request):
    try:
        dta=filer.get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        reg=json.loads(request.body)['reg']
        retu=npy.polyfit(dta[argu1],dta[argu2],reg)
        return JsonResponse(ce.ret(0,{"reg":reg,"RegList":retu.tolist(),"DataList":{argu1:json.loads(dta[argu1].to_json()),argu2:json.loads(dta[argu2].to_json())}},None))
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))

def heter_compare_apply(value,y,c_name):
    if value>y:
        return str(c_name)+">"+str(y)
    else:
        return str(c_name)+"<="+str(y)

def heter_compare_df(df,col_name,s):
    df.loc[:,col_name+'_type']=df[col_name].apply(heter_compare_apply,y=s,c_name=col_name)
    return df


def ttest(request):
    try:
        dta = filer.get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        try:
            pval=ttest_ind(dta[argu1],dta[argu2]).pvalue
            return JsonResponse(ce.ret(0,{'pvalue':pval},None))
        except:
            return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Req)."))

def type_corr(request):
    try:
        dta=filer.get_file_data(request)
        xe=json.loads(request.body)
        argu1=xe['argu1']
        argu2=xe['argu2']
        argu_type=xe['argu_type']
        segment=xe['segment']
        dta2=dta[dta[argu_type]>segment]
        re1=st.pearsonr(dta2[argu1],dta2[argu2])
        dta3=dta[dta[argu_type]<=segment]
        re2=st.pearsonr(dta3[argu1],dta3[argu2])
        return JsonResponse(ce.ret(0,{'More':re1,'Less':re2},None))
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))

#By Andy at 2022/2/7 17:30
#Modified By Aliebc at 2022/2/7 17:50

def ols(request):
    try:
        dta = filer.get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        x=sm.add_constant(dta[argu1])
        model = sm.OLS(dta[argu2], x)
        results = model.fit()
        pvals = results.pvalues
        coeff = results.params
        conf_lower = results.conf_int()[0]
        conf_higher = results.conf_int()[1]
        r2 = results.rsquared
        r2adj = results.rsquared_adj
        ll = results.llf
        f_test = results.f_test
        fvalue = results.fvalue
        results_df = pd.DataFrame({"pvals":pvals,
                                "coeff":coeff,
                                "conf_lower":conf_lower,
                                "conf_higher":conf_higher,
                                "r_squared":r2,
                                "r_squared_adj":r2adj,
                                "log_likelihood": ll,
                                "f_statistic":fvalue
                                    })
    #Reordering...
        #results_df = results_df[["r_squared","r_squared_adj","coeff","pvals","conf_lower","conf_higher"]]
    except:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal)."))
    return JsonResponse(ce.ret(0,{"Regression Summary":json.loads(results_df.to_json())},None))