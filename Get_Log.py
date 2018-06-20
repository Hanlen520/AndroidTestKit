# -*- coding: utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import os
import subprocess
import sys
import time
import codecs
import logging

# 获取Python主版本号，int型
py_ver_info = sys.version_info.major
# -------------------------------*logger*-------------------------------
# 创建一个logger
logger = logging.getLogger('GETLOG')
logger.setLevel(logging.DEBUG)

# # 创建一个handler，用于写入日志文件，默认保存在同级目录下
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

localtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
local_path = sys.path[0] + "/log/" + localtime
os.makedirs(local_path)


# 指定log name获取log,如:main, radio, system, event
def getlogs(logname):
    if logname is 'logcat':
        os.system('adb shell "rm /sdcard/logcat.log"')
        cmd = 'adb shell "logcat -d >/sdcard/logcat.log"'
        logger.info('Getting <logcat> log ......')
    else:
        cmd = 'adb shell "logcat -d -v time -b {} > /sdcard/{}.log"'.format(
            logname, logname)
        logger.info('Getting <{}> log ......'.format(logname))
    # 保存log到文件（如果文件存在会直接覆盖）
    os.system(cmd)
    # 将log文件取出到本地
    os.system('adb pull /sdcard/{}.log {}'.format(logname, local_path))


# 获取内核log（也叫串口log、Kernel log）
def get_dmesg_log():
    logger.info('Getting for <Kernel> log ......')
    os.system('adb shell dmesg > {}/Kernel.txt'.format(local_path))


# 获取ANR log
def get_anr_log():
    logger.info('Getting for <ANR> log ......')
    cmd = 'adb pull /data/anr/ {}/'.format(local_path)
    os.system(cmd)


# 获取bugreport log
def getbugreport():
    logger.info('Getting <bugreport> log ......')
    # Android 7.x之后可以使用"adb bugreport +path"导出zip包，但会与早期Android版本不兼容
    # 因此暂时不考虑使用zip包方式导出Bugreport
    cmd = 'adb shell bugreport > {}/bugreport.txt'.format(local_path)
    os.system(cmd)


def main():
    os.system('adb wait-for-device')
    os.system('adb root')
    # 获取的logcat及其子类log
    loglst = ['logcat', 'system', 'radio', 'events', 'main']
    for log in loglst:
        getlogs(log)
    if get_dmesg_log() != 0:
        logger.info('done!')
    # 获取ANR log
    if get_anr_log() != 0:
        logger.info("done!")
    # 获取bugreport
    if getbugreport() != 0:
        logger.info('done!')
    logger.info('Has been saved to [{}]'.format(local_path))


if __name__ == '__main__':
    main()
