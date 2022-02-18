from .ce import ret2,request_analyse,ret_error,ret_success
from .filer import get_file_data
import scipy.stats as st

class TEST_API_STD:
    def __init__(self,request):
        self.request=request
        self.args = request_analyse(self.request)
        self.dta = get_file_data(self.request)
    def execute(self,func,func2=None):
        try:
            ret=func(self.dta)
            ret=func2(ret)
            return ret_success(ret)
        except Exception as e:
            return ret_error(e)

def meant(request):
    try:
        r=TEST_API_STD(request)
        def func(df):
            return st.ttest_ind(df[r.args['argu1']],df[r.args['argu2']])
        def func2(rt):
            pval=rt.pvalue
            stat=rt.statistic
            return {'t-statistic':stat,'p-value':pval}
        return r.execute(func,func2)
    except Exception as e:
        return ret_error(e)

def ks(request):
    try:
        r=TEST_API_STD(request)
        def func(df):
            return st.kstest(df[r.args['argu1']],df[r.args['argu2']])
        def func2(rt):
            pval=rt.pvalue
            stat=rt.statistic
            return {'d-statistic':stat,'p-value':pval}
        return r.execute(func,func2)
    except Exception as e:
        return ret_error(e)

def normal(request):
    try:
        r=TEST_API_STD(request)
        def func(df):
            return st.normaltest(df[r.args['argu1']])
        def func2(rt):
            pval=rt.pvalue
            stat=rt.statistic
            return {'statistic':stat,'p-value':pval}
        return r.execute(func,func2)
    except Exception as e:
        return ret_error(e)

def anova(request):
    try:
        r=TEST_API_STD(request)
        def func(df):
            z=df.groupby(r.args['argu2'])
            estr=""
            for k in range(0,len(z)):
                estr+="list(z)[{}][1]['{}'],".format(k,r.args['argu1'])
            print(estr)
            x="st.f_oneway("+estr[0:-1]+")"
            t=eval(x)
            return t
        def func2(rt):
            pval=rt.pvalue
            stat=rt.statistic
            return {'F-statistic':stat,'p-value':pval}
        return r.execute(func,func2)
    except Exception as e:
        return ret_error(e)

def levene(request):
    try:
        r=TEST_API_STD(request)
        def func(df):
            z=df.groupby(r.args['argu2'])
            estr=""
            for k in range(0,len(z)):
                estr+="list(z)[{}][1]['{}'],".format(k,r.args['argu1'])
            print(estr)
            x="st.levene("+estr[0:-1]+")"
            t=eval(x)
            return t
        def func2(rt):
            pval=rt.pvalue
            stat=rt.statistic
            return {'L-statistic':stat,'p-value':pval}
        return r.execute(func,func2)
    except Exception as e:
        return ret_error(e)

def estimate_mean(request):
    try:
        r=TEST_API_STD(request)
        def func(df):
            t1=df[r.args['argu1']]
            r.args['argu2']=float(r.args['argu2'])
            m=t1.mean()
            ts=st.tsem(t1)
            sss=st.t.interval(r.args['argu2'],len(t1)-1,m,ts)
            return sss
        def func2(rt):
            return {'method':'t','c-level':r.args['argu2'],'interval':rt}
        return r.execute(func,func2)
    except Exception as e:
        return ret_error(e)

def estimate_var(request):
    try:
        r=TEST_API_STD(request)
        def func(df):
            t1=df[r.args['argu1']]
            r.args['argu2']=float(r.args['argu2'])
            cl=1-r.args['argu2']
            sz=len(t1)-1
            est1=sz*st.tvar(t1)
            sss=[est1/st.chi2.ppf(1-cl/2,sz),est1/st.chi2.ppf(cl/2,sz)]
            return sss
        def func2(rt):
            return {'method':'chi-square','c-level':r.args['argu2'],'interval':rt}
        return r.execute(func,func2)
    except Exception as e:
        return ret_error(e)

def estimate_var_ratio(request):
    try:
        r=TEST_API_STD(request)
        def func(df):
            t1=df[r.args['argu1'][0]]
            t2=df[r.args['argu1'][1]]
            vart=st.tvar(t1)/st.tvar(t2)
            r.args['argu2']=float(r.args['argu2'])
            cl=1-r.args['argu2']
            sz1=len(t1)-1
            sz2=len(t2)-1
            sss=[vart/st.f.ppf(1-cl/2,sz1,sz2),vart/st.f.ppf(cl/2,sz1,sz2)]
            return sss
        def func2(rt):
            return {'method':'F','c-level':r.args['argu2'],'interval':rt}
        return r.execute(func,func2)
    except Exception as e:
        return ret_error(e)