# -*- coding:utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com
'''
'''

import re
import subprocess
import logging
import sys
import os

# 获取Python主版本号，int型
py_ver_info = sys.version_info.major
# -------------------------------*logger*-------------------------------
# 创建一个logger
logger = logging.getLogger('GETLOG')
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


class get_apk:
    '''
    get_pkg_list: 获取最近启动过的应用列表
    pull_apk: 使用adb命令推出到指定路径
    '''

    def get_pkg_list(self):
        cmd = 'adb logcat -d ActivityManager:I *:s'
        p = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lst = p.stdout.readlines()
        pkg_list = []  # test
        pattern = re.compile('(.*)START(.*)cmp=(.*)\/')
        for i in reversed(lst):
            x = i.decode(encoding='utf-8', errors='strict')
            m = pattern.match(x)
            if m:
                pkg_name = m.groups()[-1]
                # print('m: ', pkg_name)
                if pkg_name not in pkg_list:
                    pkg_list.append(pkg_name)
        print('Package Name: ', pkg_list)
        return pkg_list

    # 根据包名获取apk路径
    def pull_apk(self, pkg_name):
        get_path_cmd = 'adb shell pm path {}'.format(pkg_name)
        pkg = subprocess.Popen(get_path_cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        if py_ver_info == 3:
            path = str(pkg.stdout.readline(), "utf-8")
        else:
            path = pkg.stdout.readline()
        pkg_path = path.split(':')[1].strip()
        # 本地保存apk路径
        self.local_path = sys.path[0] + '/apk/'
        # 创建目录
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)
        # 定义拖出后的本地路径和名称，这里以包名进行命名
        local_name = self.local_path + pkg_name + '.apk'
        # 生成最终adb命令，并执行adb pull命令
        pull_cmd = 'adb pull {REMOTE} {LOCAL}'.format(
            REMOTE=pkg_path, LOCAL=local_name)
        run_pull = subprocess.Popen(
            pull_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = run_pull.stdout.readlines()
        print(bytes.decode(stdout[-2]).strip())
        print(bytes.decode(stdout[-1]).strip())


def main():
    pkg_list = get_apk().get_pkg_list()
    logger.info("最近启动过的应用列表：")
    for m, n in enumerate(pkg_list):
        logger.info("{id} --- {pkgname}".format(id=m, pkgname=n))
    while True:
        keyword = input('Enter a ID(number) for package: ')
        if isinstance(keyword, int):  # 判断是否为int型，Python2中input为int型
            if keyword < len(pkg_list):  # 判断输入的数字，是否超出范围之内
                break
        if isinstance(keyword, str):  # 判断是否为str型，Python3中input为str型
            keyword = int(keyword)
            if keyword < len(pkg_list):
                break
        else:  # 其它所有非int型都需要重新输入
            continue  # 进入下一个循环
    logger.info(
        'You choice is: {id} --- {pkg_name}'.format(id=keyword, pkg_name=pkg_list[keyword]))
    try:
        get_apk().pull_apk(pkg_list[keyword])
    except Exception as e:
        logger.exception('Exception: %s, %s' % (Exception, e))
        logger.info('Try again and enter a number.')


if __name__ == '__main__':
    main()
