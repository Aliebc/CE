from .filer import get_file_data,generate_uid,file_dir_path
import os
import json
from .ce import ret2
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

def put_file(df):
    uid=generate_uid()
    f_name=os.path.join(file_dir_path,uid+".xlsx")
    df.to_excel(f_name,index=False,sheet_name="CE-API")
    return uid

def sql_select_simple(request):
    try:
        global dta
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        dta2=pysqldf("SELECT * FROM dta WHERE "+argu1)
        uid=put_file(dta2)
        return ret2(0,{"uid":uid},None)
    except Exception as e:
        return ret2(-1,None,"Error(#3:Internal):"+repr(e))


def sql_select_advance(request):
    try:
        global dta
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        dta2=pysqldf(argu1+" FROM dta "+argu2)
        uid=put_file(dta2)
        return ret2(0,{"uid":uid},None)
    except Exception as e:
        return ret2(-1,None,"Error(#3:Internal):"+repr(e))