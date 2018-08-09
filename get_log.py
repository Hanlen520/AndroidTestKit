# -*- coding: utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import os
import sys
import time
import logging
from screencap import screencap

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


class GetLogs:
    '''
    Get logs:
        1. logcat
        2. kernel
        3. anr
        4. tombstones
        5. bugreport
    '''

    def __init__(self):
        self.localtime = time.strftime(
            '%Y%m%d%H%M%S', time.localtime(time.time()))
        self.local_path = sys.path[0] + "/log/" + self.localtime
        self.loglst = ['all', 'system', 'radio', 'events', 'main', 'crash']
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

    def logcat(self):
        '''
        指定log name获取log,如:main, radio, system, event
        :param logname: logcat的子log模块，如-b main, -b radio等
        '''
        for logname in self.loglst:
            os.system('adb shell "rm /sdcard/logcat-{}.log"'.format(logname))
            cmd = 'adb shell "logcat {} -d >/sdcard/logcat-{}.log"'.format(
                logname, logname)
            logger.info('Getting <logcat> log ......')
            # 保存log到文件（如果文件存在会直接覆盖）
            os.system(cmd)
            # 将log文件取出到本地
            os.system(
                'adb pull /sdcard/logcat-{}.log {}'.format(logname, self.local_path))

    def dmesg_log(self):
        '''
        获取内核log（也叫串口log、Kernel log），并写入到指定文件中。
        '''
        logger.info('Getting for <Kernel> log ......')
        os.system('adb shell dmesg > {}/Kernel.txt'.format(self.local_path))

    def anr_log(self):
        '''
        获取ANR log，将/data/anr目录下的所有文件都pull到指定目录。
        ANR: Application Not Responding，即应用无响应
        '''
        logger.info('Getting for <ANR> log ......')
        cmd = 'adb pull /data/anr/ {}/'.format(self.local_path)
        os.system(cmd)

    def tombstones_log(self):
        '''
        获取tombstones log，将/data/tombstones目录下的所有文件都pull到指定目录。
        '''
        logger.info('Getting for <tombstones> log ......')
        cmd = 'adb pull /data/tombstones/ {}/'.format(self.local_path)
        os.system(cmd)

    def misc_logd(self):
        '''
        获取/data/misc/logd目录下的所有文件, pull到指定目录。
        '''
        logger.info('Getting for <misc_logd> log ......')
        cmd = 'adb pull /data/misc/logd {}/'.format(self.local_path)
        os.system(cmd)

    def bugreport(self):
        '''
        获取bugreport log
        Android 7.x之后可以使用"adb bugreport +path"导出zip包，但会与早期Android版本不兼容
        '''
        logger.info('Getting <bugreport> log ......')
        # 导出Bugreport(zip)
        cmd = 'adb bugreport {}'.format(self.local_path)
        os.system(cmd)


def main():
    '''
    执行log获取
    '''
    os.system('adb wait-for-device')
    os.system('adb remount')
    os.system('adb root')  # userdebug 固件需要此命令才能取到kernel log和tombstones log
    get = GetLogs()
    get.logcat()
    get.anr_log()
    get.dmesg_log()
    get.tombstones_log()
    get.misc_logd()
    get.bugreport()
    screencap().capture(get.local_path)
    logger.info('Has been saved to [%s]' % get.local_path)


if __name__ == '__main__':
    main()
