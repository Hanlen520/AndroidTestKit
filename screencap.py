# -*- coding:utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import time
import os
import sys


class screencap:
    
    localTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    remote_obj = '/sdcard/%s.png' % localTime
    local_obj = sys.path[0]

    def capture(self):
        a = 'adb shell screencap -p %s' % self.remote_obj
        c = 'adb pull %s %s' % (self.remote_obj, self.local_obj)

        os.system(a)
        # print 'Screen capture saved to {}'.format(remote_obj)
        print('Pull picture to your computer ...')
        os.system(c)
        print('Screen capture pull to: "{}"'.format(self.local_obj))
        print('OK.')

def main():
    snap = screencap()
    snap.capture()

if __name__ == '__main__':
    main()
