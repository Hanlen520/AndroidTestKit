# -*- coding: utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import os
import subprocess
import sys
import time

localtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
local_path = sys.path[0] + "/" + localtime
os.mkdir(local_path)


# 指定log name获取log,如:main, radio, system, event
def getlogs(logname):
    if logname is 'default':
        cmd = 'adb shell logcat -d'
        print('Getting <default> log ......')
    else:
        cmd = 'adb shell logcat -d -v time -b {}'.format(logname)
        print('Getting <{}> log ......'.format(logname))
    # lst = []
    log = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    data = log.stdout.readlines()  # 读取结果为一个列表，其中默认元素为字节类型
    return data


# 获取内核log（也叫串口log、Kernel log）
def get_dmesg_log():
    print('Getting for <Kernel> log ......', end=' ')
    os.system('adb shell dmesg > {}/Kernel.txt'.format(local_path))


# 获取ANR log
def get_anr_log():
    print('Getting for <ANR> log ......', end=' ')
    cmd = 'adb pull /data/anr/traces.txt {}/'.format(local_path)
    os.system(cmd)


# 获取bugreport log
def getbugreport():
    print('Getting <bugreport> log ......', end=' ')
    # Android 7.x之后可以使用"adb bugreport +path"导出zip包，但会与早期Android版本不兼容
    # 因此暂时不考虑使用zip包方式导出Bugreport
    cmd = 'adb shell bugreport > {}/bugreport.txt'.format(local_path)
    os.system(cmd)


# 保存log,context为获取到的log(list类型)
def savelog(filename, context, path):
    print('start save [{}] log ......'.format(filename))
    fullname = path + '/' + filename + '.log'
    f = open(fullname, 'w+', buffering=-1)
    for line in context:
        f.write(str(line, encoding='utf-8'))
    f.close()
    print('done!')


def main():
    os.system('adb wait-for-device')
    loglst = ['main', 'system', 'radio', 'events', 'default']
    # loglst = ['system']
    for log in loglst:
        tar = getlogs(log)
        savelog(filename=log, context=tar, path=local_path)
    if get_dmesg_log() != 0:
        print('done!')
    # 获取ANR log
    if get_anr_log() != 0:
        print("done!")
    # 获取bugreport
    if getbugreport() != 0:
        print('done!')
    print('Has been saved to [{}]'.format(local_path))


if __name__ == '__main__':
    main()
