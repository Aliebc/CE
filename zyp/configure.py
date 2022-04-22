"""
   ___                            _        _   _                   _                                        _          
  / __\___  _ __ ___  _ __  _   _| |_ __ _| |_(_) ___  _ __   __ _| |   ___  ___ ___  _ __   ___  _ __ ___ (_) ___ ___ 
 / /  / _ \| '_ ` _ \| '_ \| | | | __/ _` | __| |/ _ \| '_ \ / _` | |  / _ \/ __/ _ \| '_ \ / _ \| '_ ` _ \| |/ __/ __|
/ /__| (_) | | | | | | |_) | |_| | || (_| | |_| | (_) | | | | (_| | | |  __/ (_| (_) | | | | (_) | | | | | | | (__\__ \
\____/\___/|_| |_| |_| .__/ \__,_|\__\__,_|\__|_|\___/|_| |_|\__,_|_|  \___|\___\___/|_| |_|\___/|_| |_| |_|_|\___|___/
                     |_|                                                                                               

计算经济学数据处理工具箱 API
CONFIGURE.PY
CE-API配置文件

包括:
文件类配置(临时存储文件夹)
技术类配置(线程/进程类)
语言包配置(多语言支持)

本页作者:
Aliebc (aliebcx@outlook.com)

Copyright(C)2022 All Rights reserved. 
"""

#文件类配置
file_conf={
    "file_path":"/opt/zypfile", #临时文件的存储路径
    "img_path":"/opt/zypimg", #临时图片的存储路径
    "api_domain":"https://api2.abxmc.live/CE" #CE-Toolbox的域名配置
}

#技术类配置