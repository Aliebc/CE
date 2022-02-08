"""zyp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import ce
from . import filer
from . import datac
from . import imgc


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ce.ce_main),
    path('filer/',filer.recv_file),
    path('getd/',filer.getd),
    path('corr/',datac.dcorr),
    path('dtype/',datac.dtype),
    path('dhist/',datac.dhist),
    path('dsummary/',datac.dsummary),
    path('lm3/',datac.dlm3),
    path('dbar/',filer.imgtest),
    path('dimg_density/',imgc.density),
    path('dimg_hist/',imgc.hist),
    path('dimg_hetero_density/',imgc.hetero_density),
    path('dimg_density_type/',imgc.type_density),
    path('dimg_hetero_regress/',imgc.type_regress),
    path('dimg_regress/',imgc.two_reg),
    path('dimg_line/',imgc.two_line),
    path('dimg_bar_type/',imgc.type_bar),
    path('test/',ce.test),
    path('ols/',datac.ols),
    path('getf/',filer.ret_file),
]
