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
# TODO(Kevin): loggging 没有正常起作用
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
local_path = sys.path[0] + "/" + localtime
os.mkdir(local_path)


# 指定log name获取log,如:main, radio, system, event
def getlogs(logname):
    if logname is 'logcat':
        cmd = 'adb shell logcat -d'
        logger.info('Getting <logcat> log ......')
    else:
        cmd = 'adb shell logcat -d -v time -b {}'.format(logname)
        logger.info('Getting <{}> log ......'.format(logname))
    log = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    data = log.stdout.readlines()  # 读取结果为一个列表，其中默认元素为字节类型
    return data


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


# 保存log,context为获取到的log(list类型)
def savelog(filename, context, path):
    logger.info('start save [{}] log ......'.format(filename))
    fullname = path + '/' + filename + '.log'
    if py_ver_info == 3:
        f = codecs.open(fullname, 'w', 'utf-8')
        for line in context:
            line = str(line, encoding='utf-8')
            f.write(line)
    else:
        f = open(fullname, 'w')
        for line in context:
            f.write(line)
    f.close()
    logger.info('done!')


def main():
    os.system('adb wait-for-device')
    os.system('adb root')
    loglst = ['main', 'system', 'radio', 'events', 'logcat']
    for log in loglst:
        tar = getlogs(log)
        savelog(filename=log, context=tar, path=local_path)
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
