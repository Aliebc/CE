from .filer import get_file_data
import pandas as pd
import json
from .ce import ret
from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

def sql_select_simple(request):
    try:
        global dta
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        dta2=pysqldf("SELECT * FROM dta WHERE "+argu1)
        return JsonResponse(ret(0,{"DataList":json.loads(dta2.to_json(orient='records'))},None))
    except Exception as e:
        return JsonResponse(ret(-1,None,"Error:"+str(e)))


def sql_select_advance(request):
    try:
        global dta
        dta=get_file_data(request)
        argu1=json.loads(request.body)['argu1']
        argu2=json.loads(request.body)['argu2']
        dta2=pysqldf(argu1+" FROM dta "+argu2)
        return JsonResponse(ret(0,{"DataList":json.loads(dta2.to_json(orient='records'))},None))
    except Exception as e:
        return JsonResponse(ret(-1,None,"Error:"+str(e)))