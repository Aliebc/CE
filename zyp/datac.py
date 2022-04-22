"""
   ___                            _        _   _                   _                                        _          
  / __\___  _ __ ___  _ __  _   _| |_ __ _| |_(_) ___  _ __   __ _| |   ___  ___ ___  _ __   ___  _ __ ___ (_) ___ ___ 
 / /  / _ \| '_ ` _ \| '_ \| | | | __/ _` | __| |/ _ \| '_ \ / _` | |  / _ \/ __/ _ \| '_ \ / _ \| '_ ` _ \| |/ __/ __|
/ /__| (_) | | | | | | |_) | |_| | || (_| | |_| | (_) | | | | (_| | | |  __/ (_| (_) | | | | (_) | | | | | | | (__\__ \
\____/\___/|_| |_| |_| .__/ \__,_|\__\__,_|\__|_|\___/|_| |_|\__,_|_|  \___|\___\___/|_| |_|\___/|_| |_| |_|_|\___|___/
                     |_|                                                                                               

计算经济学数据处理工具箱 API
DATAC.PY
核心数据处理函数,提供纯数据处理类的方法,以单个函数的方式提供
包括但不仅限于:
相关系数矩阵
核心变量描述性统计
三大回归模型(OLS/Probit/Logit)

本页作者:
Aliebc (aliebcx@outlook.com)
Andy (andytsangyuklun@gmail.com)
Jingwei Luo

Copyright(C)2022 All Rights reserved. 
"""
import json
from django.http import JsonResponse,HttpRequest
import pandas as pd
import numpy as npy
import scipy.stats as st
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from sklearn import preprocessing
import re
from .ce import ret2,request_analyse,ret_error,ret_success
from .filer import get_file_data,put_file_excel
from .filer import put_file_all as put_file

def dcorr(request:HttpRequest) -> JsonResponse:
    """
    HTTP请求处理:获取单个相关系数
    """
    try:
        dta=get_file_data(request)
        argus=request_analyse(request)
        argu1=argus['argu1']
        argu2=argus['argu2']
        c2=st.pearsonr(dta[argu1],dta[argu2])
        cord=dta.corr()
        d=cord.to_json()
    except Exception as e:
        return ret_error(e)
    return ret_success({"CorrMartix":json.loads(d),"Significance":c2})

def xcorr_single(
    dataset:pd.DataFrame,
    cord:list
    ) -> dict:
    """
    内部函数:获取单个相关系数
    """
    dta=dataset
    ret={}
    for i in cord:
        ret[i]={}
        for j in cord:
            cor=st.pearsonr(dta[i],dta[j])
            ret[i][j]=cor
            if i==j:
                ret[i][j]=[1,0] #防止精度问题出现(0.9999...)
    return ret

def xcorr_safe(request:HttpRequest)->JsonResponse:
    """
    HTTP请求处理:获取相关系数矩阵
    """
    try:
        dta=get_file_data(request)
        args=request_analyse(request)
        cord=args['argu1']
        ret=xcorr_single(dta,cord)
    except Exception as e:
        return ret_error(e)
    return ret2(0,{"CorrMartix":ret},None)

def dtype(request:HttpRequest)->JsonResponse:
    """
    HTTP请求处理:单个变量的描述性统计
    """
    try:
        dta=get_file_data(request)
        args=request_analyse(request)
        retu=dta[args['argu1']]
        return ret_success(json.loads(retu.value_counts().to_json()))
    except Exception as e:
        return ret_error(e)

def dsummary(request:HttpRequest)->JsonResponse:
    """
    HTTP请求处理:全变量的描述性统计
    """
    try:
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        retu=dta[argu1]
        return ret2(0,json.loads(retu.describe().to_json()),None)
    except Exception as e:
        return ret_error(e)

def xsummary(request:HttpRequest)->JsonResponse:
    """
    HTTP请求处理:多个变量的描述性统计
    """
    try:
        dta=get_file_data(request)
        a2={}
        for key in dta:
            r2=dta[key]
            a2[key]=json.loads(r2.describe().to_json())
        return ret2(0,a2,None)
    except Exception as e:
        return ret_error(e)

def xsummary2(request:HttpRequest)->JsonResponse:
    """
    HTTP请求处理:多个变量的描述性统计-带文件处理
    """
    try:
        args=request_analyse(request)
        argu1=args['argu1']
        dta=get_file_data(request)
        a2={}
        for key in argu1:
            r2=dta[key]
            if not r2.dtype == 'object':
                a2[key]=json.loads(r2.describe().to_json())
        df2=pd.read_json(json.dumps(a2),orient="index")
        uid=put_file_excel(df2,True,"Variable")
        return ret_success({'ValueList':a2,'File':{'uid':uid,'f_suffix':'.xlsx'}})
    except Exception as e:
        return ret_error(e)

def dlm3(request)->JsonResponse:
    """
    HTTP请求处理:参数型回归分析
    """
    try:
        dta=get_file_data(request)
        args=request_analyse(request)
        argu1=args['argu1']
        argu2=args['argu2']
        reg=args['reg']
        retu=npy.polyfit(dta[argu1],dta[argu2],reg)
        return ret_success({
            "reg":reg,"RegList":retu.tolist(),
            "DataList":{
                argu1:json.loads(dta[argu1].to_json()),
                argu2:json.loads(dta[argu2].to_json())
            }
        })
    except Exception as e:
        return ret_error(e)

def heter_compare_apply(value,y,c_name)->str:
    """
    内部函数:大于小于处理
    """
    if value>y:
        return str(c_name)+">"+str(y)
    else:
        return str(c_name)+"<="+str(y)

def heter_compare_df(df,col_name,s)->pd.DataFrame:
    """
    内部函数:比较处理
    """
    df.loc[:,col_name+'_type']=df[col_name].apply(heter_compare_apply,y=s,c_name=col_name)
    return df

def type_corr(request:HttpRequest)->JsonResponse:
    """
    HTTP处理函数:异质性分析的分段相关系数
    """
    try:
        dta=get_file_data(request)
        xe=request_analyse(request)
        argu1=xe['argu1']
        argu_type=xe['argu_type']
        segment=xe['segment']
        dta2_t=dta[dta[argu_type]>segment]
        re1=xcorr_single(dta2_t,argu1)
        dta3_t=dta[dta[argu_type]<=segment]
        re2=xcorr_single(dta3_t,argu1)
        return ret_success({'More':re1,'Less':re2})
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
        return ret_error(e)
    return ret_success({
        "Regression Summary":json.loads(results_df.to_json()),
        "s_text":re.sub(r"Notes(.|\n)*","",str(y))
        })

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
        results_df = results_df[[
            "pseudo_r_squared",
            "log_likelihood",
            "ll_null",
            "llr_p_value",
            "f_statistic",
            "coeff",
            "pvals",
            "conf_lower",
            "conf_higher"]]
    except Exception as e:
        return ret2(-1,None,"Error(#3:Internal). Check if argu2 is binary.")
    return ret_success({"Regression Summary":json.loads(results_df.to_json()),"s_text":str(y)})

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
        return ret2(-1,None,"Error(#3:Internal). Check if argu2 is binary.")
    return ret2(0,{"Regression Summary":json.loads(results_df.to_json()),"s_text":str(y)},None)

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

def var_filter(request):
    try:
        df = get_file_data(request)
        xe = json.loads(request.body)
        f_suffix = xe['f_suffix']
        params = xe['params']
        for param in params:
            variable = param['variable']
            type = param['type']
            where = param['where']
            if(type == 1):
                label1 = where[0]['condition']
                num1 = where[0]['number']
                if(len(where) == 1):
                    if(label1 == 1):
                        for x in df.index:
                            if (pd.notnull(df.loc[x, variable])):
                                if (df.loc[x, variable] > num1):
                                    df.drop(index=x, inplace=True)
                            else:
                                df.drop(index=x, inplace=True)
                    elif(label1 == 2):
                        for x in df.index:
                            if (pd.notnull(df.loc[x, variable])):
                                if (df.loc[x, variable] >= num1):
                                    df.drop(index=x, inplace=True)
                            else:
                                df.drop(index=x, inplace=True)
                    elif (label1 == 3):
                        for x in df.index:
                            if (pd.notnull(df.loc[x, variable])):
                                if (df.loc[x, variable] == num1):
                                    df.drop(index=x, inplace=True)
                            else:
                                df.drop(index=x, inplace=True)
                    elif (label1 == 4):
                        for x in df.index:
                            if (pd.notnull(df.loc[x, variable])):
                                if (df.loc[x, variable] <= num1):
                                    df.drop(index=x, inplace=True)
                            else:
                                df.drop(index=x, inplace=True)
                    elif (label1 == 5):
                        for x in df.index:
                            if (pd.notnull(df.loc[x, variable])):
                                if (df.loc[x, variable] < num1):
                                    df.drop(index=x, inplace=True)
                            else:
                                df.drop(index=x, inplace=True)
                elif(len(where) == 2):
                    label2 = where[1]['condition']
                    num2 = where[1]['number']
                    if(num1 == num2):
                        return ret2(-1, None, "Error(#:number_choose).")

                    if(label1 == 3):
                        for x in df.index:
                            if (pd.notnull(df.loc[x, variable])):
                                if (df.loc[x, variable] == num1):
                                    df.drop(index=x, inplace=True)
                            else:
                                df.drop(index=x, inplace=True)

                    if label1 == 1 and label2 == 5:
                        if num1 < num2:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if (df.loc[x, variable] > num1 and df.loc[x, variable] < num2):
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)
                        else:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if (df.loc[x, variable] > num1 or df.loc[x, variable] < num2):
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)

                    elif label1 == 5 and label2 == 1:
                        if num1 < num2:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] < num1 or df.loc[x, variable] > num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)
                        else:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] < num1 and df.loc[x, variable] > num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)

                    elif label1 == 2 and label2 == 5:
                        if num1 < num2:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] >= num1 and df.loc[x, variable] < num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)
                        else:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] >= num1 or df.loc[x, variable] < num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)

                    elif label1 == 5 and label2 == 2:
                        if num1 < num2:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] < num1 or df.loc[x, variable] >= num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)
                        else:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] < num1 and df.loc[x, variable] >= num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)

                    elif label1 == 1 and label2 == 4:
                        if num1 < num2:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] > num1 and df.loc[x, variable] <= num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)
                        else:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] > num1 or df.loc[x, variable] <= num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)

                    elif label1 == 4 and label2 == 1:
                        if num1 < num2:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] <= num1 or df.loc[x, variable] > num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)
                        else:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] <= num1 and df.loc[x, variable] > num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)

                    elif label1 == 2 and label2 == 4:
                        if num1 < num2:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] >= num1 and df.loc[x, variable] <= num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)
                        else:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] >= num1 or df.loc[x, variable] <= num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)

                    elif label1 == 4 and label2 == 2:
                        if num1 < num2:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] <= num1 or df.loc[x, variable] >= num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)
                        else:
                            for x in df.index:
                                if (pd.notnull(df.loc[x, variable])):
                                    if df.loc[x, variable] <= num1 and df.loc[x, variable] >= num2:
                                        df.drop(index=x, inplace=True)
                                else:
                                    df.drop(index=x, inplace=True)

                    else:
                        if label1 and label2:
                            return ret2(-1, None, "Error(#:label):" + "con1:" + str(label1) + "num1:" + str(num1) + "con2:" + str(label2) + "num2:" + str(num2))
                        elif not label1:
                            return ret2(-1, None, "Error(#:label1_null).")
                        elif not label2:
                            return ret2(-1, None, "Error(#:label2_null).")
                        else:
                            return ret2(-1, None, "Error(#:label_all_null).")
                else:
                    return ret2(-1, None, "Error(#:num_length).")

            elif(type == 2):
                delete_way = where[0]['way']
                str_select = where[0]['str_select']
                if(delete_way == 1):
                    for x in df.index:
                        if (df.loc[x, variable] == str_select):
                            df.drop(index=x, inplace=True)
                else:
                    df = df[~ df[variable].str.contains(str_select)]

            else:
                return ret2(-1, None, "Error(#:Type).")
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
    res_df=pd.DataFrame({ #从回归结果中提取需要的结果
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
    res_df=pd.DataFrame({ #从回归结果中提取需要的结果
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

def g_p_str(pval)->str:
    """
    内部函数:显著性判断打星号
    """
    if pval <0.01:
        return "***"
    elif pval >=0.01 and pval<0.05:
        return "**"
    elif pval >=0.05 and pval<0.1:
        return "*"
    else:
        return ""

def smols2excel(ols_res_dict:dict)->pd.DataFrame:
    """
    内部函数:把回归结果格式化处理到Excel
    """
    ret_dict={}
    ArgList=ols_res_dict['ArgeList']
    ArgList.append("const")
    for i in range(0,ols_res_dict['count']): #按个数循环
        ret_dict['('+str(i+1)+')']={"被解释变量":ols_res_dict['OLSList'][i]['argu_i']} #建立索引
        for key in ArgList:
            if key in ols_res_dict['OLSList'][i]['Result']['coeff']:
                p_str=g_p_str(ols_res_dict['OLSList'][i]['Result']['pvalue'][key])
                ret_dict['('+str(i+1)+')'][key]=str(round(ols_res_dict['OLSList'][i]['Result']['coeff'][key],3))+p_str #拼接显著性标记
            else:
                ret_dict['('+str(i+1)+')'][key]=""
        if 'entity_effect' in ols_res_dict['OLSList'][i]['Result']: #把剩下的项目加入这个文件
            ret_dict['('+str(i+1)+')']['时间固定效应']=ols_res_dict['OLSList'][i]['Result']['entity_effect']
            ret_dict['('+str(i+1)+')']['个体固定效应']=ols_res_dict['OLSList'][i]['Result']['time_effect']
        ret_dict['('+str(i+1)+')']['观测值']=str(ols_res_dict['OLSList'][i]['Result']['n'])
        ret_dict['('+str(i+1)+')']['R^2']=str(round(ols_res_dict['OLSList'][i]['Result']['r2'],3))
    ret_df=pd.DataFrame(ret_dict)
    return ret_df

def ols_effect_repeat(request:HttpRequest)->JsonResponse:
    """
    HTTP处理函数:格式化输出OLS固定效应回归的结果
    """
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
            ols_res.append(ols_effect_inter(dta,
            olss[i]['argu_i'], #被解释变量
            olss[i]['argu_e'], #解释变量
            olss[i]['entity_effect'], #个体固定效应(Bool)
            olss[i]['time_effect'])) #时间固定效应(Bool)
            argu_il=argu_il.union(olss[i]['argu_i'])
            argu_el=argu_el.union(olss[i]['argu_e'])
        ret_s={"count":len(ols_res), #计数
        "OLSList":ols_res, #被解释变量
        "ArgeList":list(argu_el)} #参数的并集
        ret_df=smols2excel(ret_s)
        ret_uid=put_file_excel(ret_df,True)
        ret_s['File']={"uid":ret_uid,"f_suffix":".xlsx"}
        return ret_success(ret_s)
    except Exception as e:
        return ret_error(e)

def ols_repeat(request:HttpRequest)->JsonResponse:
    """
    HTTP处理函数:格式化输出OLS回归的结果
    """
    try:
        args=request_analyse(request)
        dta=get_file_data(request)
        count=args['argu1']['count']
        olss=args['argu1']['argus']
        ols_res=[]
        argu_il=set(olss[0]['argu_i'])
        argu_el=set(olss[0]['argu_e'])
        for i in range(0,count):
            ols_res.append(ols_plain_inter(dta,
            olss[i]['argu_i'], #被解释变量
            olss[i]['argu_e'])) #解释变量
            argu_il=argu_il.union(olss[i]['argu_i'])
            argu_el=argu_el.union(olss[i]['argu_e'])
        ret_s={"count":len(ols_res), #计数
            "OLSList":ols_res, #回归结果
            "ArgeList":list(argu_el)} #参数的并集
        ret_df=smols2excel(ret_s)
        ret_uid=put_file_excel(ret_df,True) #输出索引
        ret_s['File']={"uid":ret_uid,"f_suffix":".xlsx"} #文件列表
        return ret_success(ret_s)
    except Exception as e:
        return ret_error(e)