# -*- coding:utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import re
import subprocess
import logging
import sys
import os

# 获取Python主版本号，int型
py_ver_info = sys.version_info.major
# -------------------------------*logger*-------------------------------
# 创建一个logger
logger = logging.getLogger('GETAPK')
logger.setLevel(logging.DEBUG)

# # 创建一个handler，用于写入日志文件
fh = logging.FileHandler('Reports.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
# -------------------------------*logger*-------------------------------

def getApkList(path):
    for i in os.walk(path):
        print(i)


apksPath = '/Users/zhangshuaiju/Downloads/apks/new/'
def gci(filepath):
#遍历filepath下所有文件
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath,fi)
        if os.path.isdir(fi_d):
            # gci(fi_d)  #包含子目录
            pass  # 不包含子目录
        else:
            apk = os.path.join(filepath,fi_d)
            print(apk)
            os.system('adb install ' + apk)
            print('ok')

#递归遍历/root目录下所有文件
gci(apksPath)