from django.contrib import admin
from django.urls import path
from . import ce
from . import filer
from . import datac
from . import imgc
from . import editr
from . import testr

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',filer.rend1),
    path('version/',ce.ce_version),
    path('filer/',filer.recv_file),
    path('getd/',filer.getd),
    path('corr/',datac.dcorr),
    path('xcorr/',datac.xcorr),
    path('dtype/',datac.dtype),
    path('dsummary/',datac.dsummary),
    path('xsummary/',datac.xsummary),
    path('lm3/',datac.dlm3),
    path('dimg_tuid/',imgc.tuid),
    path('dimg_density/',imgc.density),
    path('dimg_hist/',imgc.hist),
    path('dimg_hetero_density/',imgc.hetero_density),
    path('dimg_density_type/',imgc.type_density),
    path('dimg_hetero_regress/',imgc.type_regress),
    path('dimg_regress/',imgc.two_reg),
    path('dimg_line/',imgc.two_line),
    path('dimg_bar_type/',imgc.type_bar),
    path('dtest_mean/',testr.meant),
    path('ols/',datac.ols),
    path('dimg_hetero_corr/',datac.type_corr),
    path('getf/',filer.ret_file),
    path('delf/',filer.del_file),
    path('binary_probit/',datac.binary_probit),
    path('binary_logit/',datac.binary_logit),
    path('select_simple/',editr.sql_select_simple),
    path('select_advance/',editr.sql_select_advance),
]

#handler404=ce.ce_not_found
