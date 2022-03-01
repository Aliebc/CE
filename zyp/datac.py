import json
import pandas as pd
import numpy as npy
import scipy.stats as st
from django.http import JsonResponse
from . import ce
from .ce import ret2,request_analyse,ret_error,ret_success
from .filer import get_file_data
from .filer import put_file_excel as put_file
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
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
        return ret_error(e)
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
        return ret_error(e)
    return ret2(0,{"CorrMartix":ret},None)

def dtype(request):
    try:
        dta=get_file_data(request)
        args=request_analyse(request)
        retu=dta[args['argu1']]
        return ret_success(json.loads(retu.value_counts().to_json()))
    except Exception as e:
        return ret_error(e)

def dsummary(request):
    try:
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        retu=dta[argu1]
        return JsonResponse(ce.ret(0,json.loads(retu.describe().to_json()),None))
    except Exception as e:
        return ret_error(e)

def xsummary(request):
    try:
        dta=get_file_data(request)
        a2={}
        for key in dta:
            r2=dta[key]
            a2[key]=json.loads(r2.describe().to_json())
        return ret2(0,a2,None)
    except Exception as e:
        return ret_error(e)

def xsummary2(request):
    try:
        argu1=json.loads(request.body)['argu1']
        dta=get_file_data(request)
        a2={}
        for key in argu1:
            r2=dta[key]
            if not r2.dtype == 'object':
                a2[key]=json.loads(r2.describe().to_json())
        a3={}
        df2=pd.read_json(json.dumps(a2),orient="index")
        uid=put_file(df2,True,"Variable")
        return ret_success({'ValueList':a2,'File':{'uid':uid,'f_suffix':'.xlsx'}})
    except Exception as e:
        return ret_error(e)

def dlm3(request):
    try:
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        reg=json.loads(request.body)['reg']
        retu=npy.polyfit(dta[argu1],dta[argu2],reg)
        return JsonResponse(ce.ret(0,{"reg":reg,"RegList":retu.tolist(),"DataList":{argu1:json.loads(dta[argu1].to_json()),argu2:json.loads(dta[argu2].to_json())}},None))
    except Exception as e:
        return ret_error(e)

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
        return ret_error(e)

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

## This Part is developed by Jingwei Luo

def loss_test(request):
    try:
        dta = get_file_data(request)
        argu1 = json.loads(request.body)['argu1']
        loss = 0
        data = []
        for x in dta.index:
            for y in argu1:
                if (pd.isnull(dta.loc[x, y]) or dta.loc[x, y] == " "):
                    loss = loss + 1
                    data.append(dta.loc[x])
                    break
        result_df = pd.DataFrame(data)
        ob1 = len(dta)
        return ret_success({"loss": loss, "Observed": ob1, "Datalist": json.loads(result_df.to_json(orient='index'))})
    except Exception as e:
        return ret_error(e)

def loss_delete(request):
    try:
        dta = get_file_data(request)
        xe = json.loads(request.body)
        argu1 = xe['argu1']
        f_suffix = xe['f_suffix']
        data = []

        for x in dta.index:
            flag = 0
            for y in argu1:
                if (pd.isnull(dta.loc[x, y]) or dta.loc[x, y] == " "):
                    flag = flag + 1
                    break
            if flag == 0:
                data.append(dta.loc[x])
        result_df = pd.DataFrame(data)
        uid = put_file(result_df, f_suffix)
        return ret_success({"uid": uid, "f_suffix": f_suffix, "Datalist": json.loads(result_df.to_json(orient='index'))})
    except Exception as e:
        return ret_error(e)

def str_filter(request):
    try:
        df = get_file_data(request)
        xe = json.loads(request.body)
        f_suffix = xe['f_suffix']
        argu1 = xe['argu1']
        str_select = xe['str_select']
        delete_way = xe['delete_way']
        if (delete_way == 0):
            for x in df.index:
                if (df.loc[x, argu1] == str_select):
                    df.drop(index=x, inplace=True)
        else:
            df = df[~ df[argu1].str.contains(str_select)]
        uid = put_file(df, f_suffix)
        return ret_success({"uid": uid, "f_suffix": f_suffix, "Datalist": json.loads(df.to_json(orient='index'))})
    except Exception as e:
        return ret_error(e)

def num_filter(request):
    try:
        df = get_file_data(request)
        xe = json.loads(request.body)
        argu1 = xe['argu1']
        argu2 = xe['argu2']
        f_suffix = xe['f_suffix']
        num1 = argu2[0][1]
        num2 = argu2[1][1]
        if (argu2[0][0] == 0 and argu2[1][0] == 0):
            for x in df.index:
                if (pd.notnull(df.loc[x, argu1])):
                    if (df.loc[x, argu1] >= num1 and df.loc[x, argu1] <= num2):
                        df.drop(index=x, inplace=True)
                else:
                    df.drop(index=x, inplace=True)
        elif (argu2[0][0] != 0 & argu2[1][0] == 0):
            for x in df.index:
                if (pd.notnull(df.loc[x, argu1])):
                    if (df.loc[x, argu1] > num1 and df.loc[x, argu1] <= num2):
                        df.drop(index=x, inplace=True)
                else:
                    df.drop(index=x, inplace=True)
        elif (argu2[0][0] == 0 & argu2[1][0] != 0):
            for x in df.index:
                if (pd.notnull(df.loc[x, argu1])):
                    if (df.loc[x, argu1] >= num1 and df.loc[x, argu1] < num2):
                        df.drop(index=x, inplace=True)
                else:
                    df.drop(index=x, inplace=True)
        else:
            for x in df.index:
                if (pd.notnull(df.loc[x, argu1])):
                    if (df.loc[x, argu1] > num1 and df.loc[x, argu1] < num2):
                        df.drop(index=x, inplace=True)
                else:
                    df.drop(index=x, inplace=True)
        uid = put_file(df, f_suffix)
        return ret_success({"uid": uid, "f_suffix": f_suffix, "Datalist": json.loads(df.to_json(orient='index'))})
    except Exception as e:
        return ret_error(e)

## End this part

def ols_plain_inter(df,argu_i,argu_e):
    argu_e=sm.add_constant(df[argu_e])
    mod=sm.OLS(df[argu_i],argu_e)
    results=mod.fit()
    pvalue = results.pvalues
    coeff = results.params
    std_err = results.bse
    r2 = results.rsquared
    res_df=pd.DataFrame({
        "pvalue":pvalue,
        "coeff":coeff,
        "std_err":std_err,
    })
    res_js=json.loads(res_df.to_json())
    res_js['n']=df.shape[0]
    res_js['r2']=r2
    return {"argu_i":argu_i,"Result":res_js}

def ols_effect_inter(df,argu_i,argu_e,entity_effects,time_effects):
    argu_e=sm.add_constant(df[argu_e])
    mod=PanelOLS(df[argu_i],argu_e,entity_effects=entity_effects,time_effects=time_effects)
    results=mod.fit()
    pvalue = results.pvalues
    coeff = results.params
    std_err = results.std_errors
    r2 = results.rsquared
    res_df=pd.DataFrame({
        "pvalue":pvalue,
        "coeff":coeff,
        "std_err":std_err,
    })
    res_js=json.loads(res_df.to_json())
    res_js['n']=df.shape[0]
    res_js['time_effect']=time_effects
    res_js['entity_effect']=entity_effects
    res_js['r2']=r2
    return {"argu_i":argu_i,"Result":res_js}

def ols_effect_repeat(request):
    try:
        args=request_analyse(request)
        dta=get_file_data(request)
        count=args['argu1']['count']
        olss=args['argu1']['argus']
        dta=dta.set_index(args['argu1']['argue'])
        ols_res=[]
        argu_il=set(olss[0]['argu_i'])
        argu_el=set(olss[0]['argu_e'])
        for i in range(0,count):
            ols_res.append(ols_effect_inter(dta,olss[i]['argu_i'],olss[i]['argu_e'],olss[i]['entity_effect'],olss[i]['time_effect']))
            argu_il=argu_il.union(olss[i]['argu_i'])
            argu_el=argu_el.union(olss[i]['argu_e'])
        return ret_success({"count":len(ols_res),"OLSList":ols_res,"ArgeList":list(argu_el)})
    except Exception as e:
        return ret_error(e)

def ols_repeat(request):
    try:
        args=request_analyse(request)
        dta=get_file_data(request)
        count=args['argu1']['count']
        olss=args['argu1']['argus']
        ols_res=[]
        argu_il=set(olss[0]['argu_i'])
        argu_el=set(olss[0]['argu_e'])
        for i in range(0,count):
            ols_res.append(ols_plain_inter(dta,olss[i]['argu_i'],olss[i]['argu_e']))
            argu_il=argu_il.union(olss[i]['argu_i'])
            argu_el=argu_el.union(olss[i]['argu_e'])
        
        return ret_success({"count":len(ols_res),"OLSList":ols_res,"ArgeList":list(argu_el)})
    except Exception as e:
        return ret_error(e)
    

class OLS_ADVANCE:
    def __init__(self,count,dta,argu_t,argu_effect):
        self.df=dta
        self.src=[]
        self.point=0
        if not argu_t:
            self.df['__STIME__']=1
        if not argu_effect:
            self.df['__EFFECT__']=1
        for i in range(0,count):
            self.src[i]={}
    def add_res(self,res):
        self.src[self.point]=res
        self.point+=1
        return self.point
    def any_ols(self,argu_i,argu_e,time_effect,entity_effect):
        return None

        


def ols_effect(request):
    args=request_analyse(request)
    dta=get_file_data(request)
    argu1=args['argu1']
    return None