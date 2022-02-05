from email.policy import default
import os
import re
import time
import json
import math
from turtle import width
from pandas import DataFrame
import hashlib
import pathlib
import pandas as pd
import numpy as npy
from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from . import ce
from . import filer
from plotnine import *

image_path="/opt/zypimg"

def density(request):
    if request.method =='GET':
       
        
        return HttpResponse('yes')
    elif request.method =='POST':
        return HttpResponse('2')
    else:
        return JsonResponse(ce.ret(-1,None,'Method Not Allowed.'))
    return HttpResponse('0')