#!/usr/bin/env python

"""
   ___                            _        _   _                   _                                        _          
  / __\___  _ __ ___  _ __  _   _| |_ __ _| |_(_) ___  _ __   __ _| |   ___  ___ ___  _ __   ___  _ __ ___ (_) ___ ___ 
 / /  / _ \| '_ ` _ \| '_ \| | | | __/ _` | __| |/ _ \| '_ \ / _` | |  / _ \/ __/ _ \| '_ \ / _ \| '_ ` _ \| |/ __/ __|
/ /__| (_) | | | | | | |_) | |_| | || (_| | |_| | (_) | | | | (_| | | |  __/ (_| (_) | | | | (_) | | | | | | | (__\__ \
\____/\___/|_| |_| |_| .__/ \__,_|\__\__,_|\__|_|\___/|_| |_|\__,_|_|  \___|\___\___/|_| |_|\___/|_| |_| |_|_|\___|___/
                     |_|                                                                                               

计算经济学数据处理工具箱 API

数据处理及分析(Data analysis)是进行经济学研究的必要流程。
从获得原始数据集开始,需要经过一系列数据清洗工作才可以得到用于最终分析的数据集,并基于该数据集进行描述性统计以发现数据中变量的相关关系。
本项目提供了一个数据分析的标准化流程,避免在数据清洗及分析过程中产生遗漏或错误。

开发语言:Python3
稳定推荐版本:Python3.6.8
推荐运行操作系统:CentOS 7/8

调试环境默认情况下被开启,正式部署时请关闭调试模式

指导者:
Tracy Xiao Liu
Shu Wang

开发者/贡献者:
Aliebc (aliebcx@outlook.com)
Andy (andytsangyuklun@gmail.com)
Jingwei Luo
Kai Bian
Xiaolong Yuan
Yang He
Zihan Wang

使用如下python开源项目:
Numpy
Scipy 
Pandas 
openpyxl 
xlrd 
xlwt 
Django 
plotnine 
matplotlib 
sklearn 
pandasql 
linearmodels

Copyright(C)2022 All Rights reserved. 
"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zyp.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
