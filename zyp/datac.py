import json
import pandas as pd
import numpy as npy
import scipy.stats as st
from django.http import JsonResponse
from . import ce
from .ce import ret2,request_analyse
from .filer import get_file_data
import statsmodels.api as sm
from sklearn import preprocessing

def dcorr(request):
    try:
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        c2=st.pearsonr(dta[argu1],dta[argu2])
        cord=dta.corr()
        d=cord.to_json()
    except Exception as e:
        return ret2(-1,None,"Error(#3:Internal):"+repr(e))
    return ret2(0,{"CorrMartix":json.loads(d),"Significance":c2},None)

def xcorr(request):
    try:
        dta=get_file_data(request)
        cord=json.loads(dta.corr().to_json())
        ret={}
        for i in cord:
            ret[i]={}
            for j in cord[i]:
                cor=st.pearsonr(dta[i],dta[j])
                ret[i][j]=cor
    except Exception as e:
        return ret2(-1,None,repr(e))
    return ret2(0,{"CorrMartix":ret},None)

def dtype(request):
    try:
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        retu=dta[argu1]
        return JsonResponse(ce.ret(0,json.loads(retu.value_counts().to_json()),None))
    except Exception as e:
        return ret2(-1,None,"Error(#3:Internal):"+repr(e))

def dsummary(request):
    try:
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        retu=dta[argu1]
        return JsonResponse(ce.ret(0,json.loads(retu.describe().to_json()),None))
    except Exception as e:
        return ret2(-1,None,"Error(#3:Internal):"+repr(e))

def xsummary(request):
    try:
        dta=get_file_data(request)
        a2={}
        for key in dta:
            r2=dta[key]
            a2[key]=json.loads(r2.describe().to_json())
        return JsonResponse(ce.ret(0,a2,None))
    except Exception as e:
        return ret2(-1,None,"Error(#3:Internal):"+repr(e))

def dlm3(request):
    try:
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        reg=json.loads(request.body)['reg']
        retu=npy.polyfit(dta[argu1],dta[argu2],reg)
        return JsonResponse(ce.ret(0,{"reg":reg,"RegList":retu.tolist(),"DataList":{argu1:json.loads(dta[argu1].to_json()),argu2:json.loads(dta[argu2].to_json())}},None))
    except Exception as e:
        return ret2(-1,None,"Error(#3:Internal):"+repr(e))

def heter_compare_apply(value,y,c_name):
    if value>y:
        return str(c_name)+">"+str(y)
    else:
        return str(c_name)+"<="+str(y)

def heter_compare_df(df,col_name,s):
    df.loc[:,col_name+'_type']=df[col_name].apply(heter_compare_apply,y=s,c_name=col_name)
    return df

def type_corr(request):
    try:
        dta=get_file_data(request)
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
    except Exception as e:
        return ret2(-1,None,"Error(#3:Internal):"+repr(e))

#By Andy at 2022/2/7 17:30
#Modified By Aliebc at 2022/2/7 17:50

def ols(request):
    try:
        dta = get_file_data(request)
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
        y=results.summary()
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
    except Exception as e:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal):"+str(e)))
    return JsonResponse(ce.ret(0,{"Regression Summary":json.loads(results_df.to_json()),"s_text":str(y)},None))

def binary_probit(request):
    try:
        label_encoder = preprocessing.LabelEncoder()
        dta = get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        y=label_encoder.fit_transform(dta[argu2])
        x=sm.add_constant(dta[argu1])
        model = sm.Probit(y, x)
        results = model.fit()
        
        pvals = results.pvalues
        coeff = results.params
        conf_lower = results.conf_int()[0]
        conf_higher = results.conf_int()[1]
        ll = results.llf
        pseudor2 = results.prsquared
        llnull = results.llnull
        llrpvalue = results.llr_pvalue
        f_test = results.f_test
        y=results.summary()

        results_df = pd.DataFrame({"pvals":pvals,
                               "coeff":coeff,
                               "conf_lower":conf_lower,
                               "conf_higher":conf_higher,
                               "log_likelihood":ll,
                               "pseudo_r_squared":pseudor2,
                               "ll_null":llnull,
                               "llr_p_value":llrpvalue,
                               "f_statistic":f_test
                                })
        results_df = results_df[["pseudo_r_squared","log_likelihood","ll_null","llr_p_value","f_statistic","coeff","pvals","conf_lower","conf_higher"]]
    except Exception as e:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal). Check if argu2 is binary."))
    return JsonResponse(ce.ret(0,{"Regression Summary":json.loads(results_df.to_json()),"s_text":str(y)},None))

def binary_logit(request):
    try:
        label_encoder = preprocessing.LabelEncoder()
        dta = get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        y=label_encoder.fit_transform(dta[argu2])
        x=sm.add_constant(dta[argu1])
        model = sm.Logit(y, x)
        results = model.fit()
        
        pvals = results.pvalues
        coeff = results.params
        conf_lower = results.conf_int()[0]
        conf_higher = results.conf_int()[1]
        ll = results.llf
        pseudor2 = results.prsquared
        llnull = results.llnull
        llrpvalue = results.llr_pvalue
        f_test = results.f_test
        y=results.summary()

        results_df = pd.DataFrame({"pvals":pvals,
                               "coeff":coeff,
                               "conf_lower":conf_lower,
                               "conf_higher":conf_higher,
                               "log_likelihood":ll,
                               "pseudo_r_squared":pseudor2,
                               "ll_null":llnull,
                               "llr_p_value":llrpvalue,
                               "f_statistic":f_test
                                })
        results_df = results_df[["pseudo_r_squared","log_likelihood","ll_null","llr_p_value","f_statistic","coeff","pvals","conf_lower","conf_higher"]]
    except Exception as e:
        return JsonResponse(ce.ret(-1,None,"Error(#3:Internal). Check if argu2 is binary."))
    return JsonResponse(ce.ret(0,{"Regression Summary":json.loads(results_df.to_json()),"s_text":str(y)},None))
