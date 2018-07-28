# -*- coding:utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import time
import os
import sys


class screencap:
    
    localTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    remote_path = '/sdcard'

    def capture(self, local_path=sys.path[0]):
        
        cmd_snap = 'adb shell screencap -p %s/1.png' % self.remote_path
        cmd_pull_png = 'adb pull %s/1.png %s/%s.png' % (self.remote_path, local_path, self.localTime)

        os.system(cmd_snap)
        print('Pull picture to your computer ...')
        os.system(cmd_pull_png)
        # print('Screen capture pull to: "{}"'.format(local_path))
        print('OK.')

def main():
    os.system('adb wait-for-device')
    os.system('adb remount')
    os.system('adb root') # userdebug 固件需要此命令才能取到kernel log和tombstones log
    snap = screencap()
    snap.capture()

if __name__ == '__main__':
    main()
