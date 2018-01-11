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
        cmd = 'adb shell logcat '
        print 'Getting <default> log ......'
    else:
        cmd = 'adb shell logcat -v time -b {}'.format(logname)
        print 'Getting <{}> log ......'.format(logname)
    lst = []
    log = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    # 结束以时间判断
    endtime = getandroidtime()
    print 'Endtime:', endtime
    # 逐行读取log,并放到列表lst中
    while True:
        buff = log.stdout.readline()
        # print buff
        nowtime = buff[0:14]
        lst.append(buff)
        # 结束判断
        if nowtime > endtime:
            print nowtime
            break
    return lst


# 获取内核log（也叫串口log、Kernel log）
def get_dmesg_log():
    print 'Getting for <Kernel> log ......',
    os.system('adb shell dmesg > {}/Kernel.txt'.format(local_path))


# 获取ANR log
def get_anr_log():
    print 'Getting for <ANR> log ......',
    cmd = 'adb pull /data/anr/traces.txt {}/'.format(local_path)
    os.system(cmd)


# 获取bugreport log
def getbugreport():
    print 'Getting <bugreport> log ......',
    cmd = 'adb shell bugreport > {}/bugreport.txt'.format(local_path)
    os.system(cmd)


# 保存log,context为获取到的log(list类型)
def savelog(filename, context, path):
    print 'start save [{}] log ......'.format(filename)
    fullname = path + '/' + filename + '.log'
    f = open(fullname, 'w+', buffering=-1)
    for line in context:
        f.write(line)
    f.close()
    print 'done!'


# 获取Android系统时间
def getandroidtime():
    # 获取系统时间戳的命令
    cmd = 'adb shell date +"%s"'
    print cmd
    t = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    androidlocaltime = t.stdout.readline().strip()
    # 将时间戳转化成指定时间格式
    SysTime = time.strftime(
        '%m-%d %H:%M:%S', time.localtime(int(androidlocaltime)))
    print type(SysTime), SysTime
    return SysTime


# 获取Android版本号
def getandroidbuild():
    cmd = 'adb shell getprop ro.build.version.release'
    bulid = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    # print bulid.stdin.readline()
    bulidversion = bulid.stdout.read().strip()
    return bulidversion


def main():
    os.system('adb wait-for-device')
    loglst = ['main', 'system', 'radio', 'event', 'crash', 'default']
    # loglst = ['radio']
    for log in loglst:
        tar = getlogs(log)
        savelog(filename=log, context=tar, path=local_path)
    if get_dmesg_log() != 0:
        print 'done!'
    # 获取ANR log
    if get_anr_log() != 0:
        print "done!"
    # 获取bugreport
    if getbugreport() != 0:
        print 'done!'
    print 'Has been saved to [{}]'.format(local_path)


if __name__ == '__main__':
    # print local_path
    main()
