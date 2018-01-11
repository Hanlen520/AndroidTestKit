# -*- coding:utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import time
import os
import sys


localTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
remote_obj = '/sdcard/%s.png' % localTime
local_obj = sys.path[0]

a = 'adb shell screencap -p %s' % remote_obj
c = 'adb pull %s %s' % (remote_obj, local_obj)

os.system(a)
# print 'Screen capture saved to {}'.format(remote_obj)
print 'Pull picture to your computer ...'
os.system(c)
print 'Screen capture pull to: "{}"'.format(local_obj)

print 'OK.'
