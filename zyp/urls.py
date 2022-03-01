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
    path('language/',ce.language),
    path('filer/',filer.recv_file),
    path('getd/',filer.getd),
    path('corr/',datac.dcorr),
    path('xcorr/',datac.xcorr),
    path('dtype/',datac.dtype),
    path('dsummary/',datac.dsummary),
    path('xsummary/',datac.xsummary),
    path('xsummary2/',datac.xsummary2),
    path('lm3/',datac.dlm3),
    path('dimg_tuid/',imgc.tuid),
    path('dimg_density/',imgc.density),
    path('dimg_hist/',imgc.hist),
    path('dimg_hetero_density/',imgc.hetero_density),
    path('dimg_density_type/',imgc.type_density),
    path('dimg_hetero_regress/',imgc.type_regress),
    path('dimg_regress/',imgc.two_reg),
    path('dimg_regress_d2/',imgc.two_reg_d2),
    path('dimg_line/',imgc.two_line),
    path('dimg_bar_type/',imgc.type_bar),
    path('dimg_qq/',imgc.qqplot),
    path('dimg_cdf/',imgc.cdf),
    path('dimg_advance/',imgc.plot_advance),
    path('dtest_mean/',testr.meant),
    path('dtest_ks/',testr.ks),
    path('dtest_norm/',testr.normal),
    path('dtest_anova/',testr.anova),
    path('dtest_std/',testr.levene),
    path('dest_mean/',testr.estimate_mean),
    path('dest_var/',testr.estimate_var),
    path('dest_varr/',testr.estimate_var_ratio),
    path('ols/',datac.ols),
    path('olss/',datac.ols_repeat),
    path('olsse/',datac.ols_effect_repeat),
    path('dimg_hetero_corr/',datac.type_corr),
    path('getf/',filer.ret_file),
    path('delf/',filer.del_file),
    path('binary_probit/',datac.binary_probit),
    path('binary_logit/',datac.binary_logit),
    path('select_simple/',editr.sql_select_simple),
    path('select_advance/',editr.sql_select_advance),
    path('loss_test/', datac.loss_test),
    path('loss_delete/', datac.loss_delete),
    path('str_filter/', datac.str_filter),
    path('num_filter/', datac.num_filter),
]

#handler404=ce.ce_not_found
