from .filer import get_file_data,put_file_excel
from .ce import ret_success,ret_error,request_analyse
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

class SQL_API_STD:
    def __init__(self,request):
        self.request=request
        self.args = request_analyse(self.request)
    def execute(self,sql_str):
        try:
            global dta
            dta = get_file_data(self.request)
            dta2=pysqldf(sql_str)
            uid=put_file_excel(dta2)
            return ret_success({"uid":uid,"f_suffix":".xlsx"})
        except Exception as e:
            return ret_error(e)

class EDIT_API_STD:
    def __init__(self,request):
        self.request=request
        self.args = request_analyse(self.request)
        self.dta = get_file_data(self.request)
    def execute(self,dta2):
        try:
            uid=put_file_excel(dta2)
            return ret_success({"uid":uid,"f_suffix":".xlsx"})
        except Exception as e:
            return ret_error(e)

def sql_select_simple(request):
    r=SQL_API_STD(request)
    return r.execute("SELECT * FROM dta WHERE "+r.args['argu1'])

def sql_select_advance(request):
    r=SQL_API_STD(request)
    return r.execute(r.args['argu1']+" FROM dta "+r.args['argu2'])