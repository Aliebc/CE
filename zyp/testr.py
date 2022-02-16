from .ce import ret2,request_analyse
from .filer import get_file_data
import scipy.stats as st

def meant(request):
    try:
        dta = get_file_data(request)
        args = request_analyse(request)
        try:
            res=st.ttest_ind(dta[args['argu1']],dta[args['argu2']])
            pval=res.pvalue
            stat=res.statistic
            return ret2(0,{'t-statistic':stat,'p-value':pval},None)
        except Exception as e:
            return ret2(-1,None,"Error(#3:Internal).")
    except Exception as e:
        return ret2(-1,None,"Error(#3:Req).")

def test_std_api(request):
    try:
        dta = get_file_data(request)
        args = request_analyse(request)
        try:
            res=st.ttest_ind(dta[args['argu1']],dta[args['argu2']])
            pval=res.pvalue
            stat=res.statistic
            return ret2(0,{'t-statistic':stat,'p-value':pval},None)
        except Exception as e:
            return ret2(-1,None,"Error(#3:Internal).")
    except Exception as e:
        return ret2(-1,None,"Error(#3:Req).")