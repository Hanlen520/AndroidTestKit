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


class get_apk:
    '''
    get_pkg_list: 获取最近启动过的应用列表
    pull_apk: 使用adb命令推出到指定路径
    '''

    def __init__(self):
        # 本地保存apk路径
        self.local_path = sys.path[0] + '/apk/'
        # 创建目录
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)


    def pkgs_of_recent(self):
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
                if "/" not in pkg_name and pkg_name not in pkg_list:
                    pkg_list.append(pkg_name)

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
        return [pkg_list[keyword]]

    # all of the third party packages, reture a list.
    def pkgs_of_third_party(self):
        pkgNames = []
        cmd = 'adb shell cmd package list packages -3'
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        names = run.stdout.readlines()
        for n in names:
            name = n.decode(encoding='utf-8', errors='strict')
            name = name.split(':')[1].strip()
            pkgNames.append(name)
        return pkgNames

    # 根据包名获取apk路径
    def pull_apk(self, pkgs):
        for pkg in pkgs:
            get_path_cmd = 'adb shell pm path {}'.format(pkg)
            pkgPath = subprocess.Popen(get_path_cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
            if py_ver_info == 3:
                path = str(pkgPath.stdout.readline(), "utf-8")
            else:
                path = pkgPath.stdout.readline()
            pkgPath = path.split(':')[1].strip()

            # 定义拖出后的本地路径和名称，这里以包名进行命名
            local_name = self.local_path + pkg + '.apk'
            # 生成最终adb命令，并执行adb pull命令
            pull_cmd = 'adb pull {REMOTE} {LOCAL}'.format(
                REMOTE=pkgPath, LOCAL=local_name)
            run_pull = subprocess.Popen(
                pull_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout = run_pull.stdout.readlines()
            for st in stdout:
                logger.info(bytes.decode(st).strip())
                # logger.info(bytes.decode(st).strip())
            # rename
            logger.info('Renaming this apk ......')
            apkLabel, apkVersion = self.aapt_dump_badging(local_name)
            newName = self.local_path + apkLabel + '_' + apkVersion +'_' + pkg + '.apk'
            os.rename(local_name, newName)
            logger.info('Work done.')

    # Add apk's Application label to the filename.
    def aapt_dump_badging(self, apk_path):
        # Check the system, because different systems use different tools
        if 'win' in sys.platform:
            aapt_badging = sys.path[0] + '/resource/aapt dump badging '
        else:
            aapt_badging = sys.path[0] + '/resource/aapt.exe dump badging '
        get_app_info_cmd = aapt_badging + apk_path
        run = subprocess.Popen(
            get_app_info_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = run.stdout.readlines()
        # 正则匹配application label
        app_label_pattern = re.compile("application-label:'(.*)'")
        # 正则匹配version name
        app_version_pattern = re.compile(
            "(.*)versionName='(.*)' platformBuildVersionName='(.*)'")
        app_info = {}
        # 遍历aapt dump badging结果的每一行
        for i in stdout:
            x = i.decode(encoding='utf-8', errors='strict')
            app_version = app_version_pattern.match(x)
            app_label = app_label_pattern.match(x)
            if app_version:
                app_info['VersionName'] = app_version.groups()[-2]
            elif app_label:
                app_info['ApplicationLabel'] = app_label.groups()[-1]
        label = app_info['ApplicationLabel'].replace(" ", "_")
        version = app_info['VersionName'].replace(" ", "_")
        return (label, version)


def main():
    logger.info('1. Pull apk of RECENT;')
    logger.info('2. Pull apks all of the third party;')

    keyword = input('Enter a ID(number) : ')
    if not isinstance(keyword, int):
        try:
            keyword = int(keyword)
        except:
            logger.info('Wrong enter, please re-enter! ')

    if keyword not in [1, 2]:  # 判断输入的数字，是否超出范围之内
        logger.info('Wrong enter, please re-enter! ')
    elif keyword == 1:
        logger.info('You picked: {id}'.format(id=keyword))
        pkgs = get_apk().pkgs_of_recent()
        get_apk().pull_apk(pkgs)
    elif keyword == 2:
        logger.info('You picked: {id}'.format(id=keyword))
        pkgs = get_apk().pkgs_of_third_party()
        get_apk().pull_apk(pkgs)


if __name__ == '__main__':
    main()
