"""
   ___                            _        _   _                   _                                        _          
  / __\___  _ __ ___  _ __  _   _| |_ __ _| |_(_) ___  _ __   __ _| |   ___  ___ ___  _ __   ___  _ __ ___ (_) ___ ___ 
 / /  / _ \| '_ ` _ \| '_ \| | | | __/ _` | __| |/ _ \| '_ \ / _` | |  / _ \/ __/ _ \| '_ \ / _ \| '_ ` _ \| |/ __/ __|
/ /__| (_) | | | | | | |_) | |_| | || (_| | |_| | (_) | | | | (_| | | |  __/ (_| (_) | | | | (_) | | | | | | | (__\__ \
\____/\___/|_| |_| |_| .__/ \__,_|\__\__,_|\__|_|\___/|_| |_|\__,_|_|  \___|\___\___/|_| |_|\___/|_| |_| |_|_|\___|___/
                     |_|                                                                                               

计算经济学数据处理工具箱 API
EDITR.PY
核心函数,包括变量生成、缺失值删除等

作者:
Aliebc (aliebcx@outlook.com)

Copyright(C)2022 All Rights reserved. 
"""

from .filer import get_file_data,put_file_excel
from .ce import ret_success,ret_error,request_analyse
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())
dtasql=True

class SQL_API_STD:
    def __init__(self,request):
        self.request=request
        self.args = request_analyse(self.request)
    def execute(self,sql_str):
        try:
            global dtasql
            dtasql = get_file_data(self.request)
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
    return r.execute("SELECT * FROM dtasql WHERE "+r.args['argu1'])

def sql_select_advance(request):
    r=SQL_API_STD(request)
    return r.execute(r.args['argu1']+" FROM dtasql "+r.args['argu2'])