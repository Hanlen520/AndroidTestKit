# -*- coding:utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import os
import subprocess
import sys
import logging

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


adb_shell = 'adb shell'
apk_path = 'adb shell pm path'


# 根据包名获取apk路径
def get_pkg_path(x):
    cmd = ['adb', 'shell', 'pm', 'path', x]
    pkg = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    # 等待进行完成
    if pkg.wait() != 0:
        logger.info("There were some errors")
    # 处理数据，将结果中的包名取出，并去掉换行符，因返回数据只有一行所以读取时只读一行
    # 只使用readline
    if py_ver_info == 3:
        path = str(pkg.stdout.readline(), "utf-8")
    else:
        path = pkg.stdout.readline()
    pkg_path = path.split(':')[1].strip()
    logger.info('Package path is :%s' % (pkg_path))
    # 返回一个列表
    return pkg_path


# 通过adb shell pm list packages获取设备中的所有包名
def get_pkg_list(keyword):
    if keyword == '':
        cmd = ['adb', 'shell', 'pm list package']
    else:
        cmd = ['adb', 'shell', 'pm list package | grep {}'.format(keyword)]
    get_pkg_info = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 读取所有数据，返回一个列表，Python3中元素为字节类型，Python2中元素为字符串口
    pkgs = get_pkg_info.stdout.readlines()
    # 定义一个空列表，将原始数据中的"package:"和换行符去除后放入此列表。
    pkg_list = []
    for name in pkgs:
        if py_ver_info == 3:
            name = str(name, 'utf-8')
        pkg_name = name.split(':')[1].strip()
        pkg_list.append(pkg_name)
    return pkg_list


# 拖出apk
def pull_apk(pkg_name):
    # 根据包名获取apk路径
    pkg_path = get_pkg_path(pkg_name)
    # 定义拖出后的本地路径和名称，这里以包名进行命名
    local_name = sys.path[0] + '/' + pkg_name + '.apk'
    # 生成最终adb命令，并执行adb pull命令
    pull_cmd = ['adb', 'pull', pkg_path, local_name]
    subprocess.check_call(pull_cmd)


if __name__ == '__main__':
    logger.info('Wait for device:')
    os.system('adb root')
    os.system('adb wait-for-device')
    logger.info('Device is fond.')
    # 循环判断关键字规则
    while True:
        # 输入一个包名中可能的关键字，可以方便过滤一部分应用
        if py_ver_info == 3:
            keyword = input('Enter a "keyword" for package name: ')
        elif py_ver_info == 2:
            keyword = raw_input('Enter a "keyword" for package name: ')
        pkg_list = get_pkg_list(keyword)
        if pkg_list == []:
            logger.info('Nothing!!!')
        else:
            logger.info('Something is fond.')
            break
    for m, n in enumerate(pkg_list):
        logger.info("{id} --- {pkgname}".format(id=m, pkgname=n))
    # 循环判断输入ID规则
    while True:
        logger.info('You enter in is not a number.')
        # r = input('Enter a ID(number) for pakage: ')
        # 判断输入是否为数字，如果不是数字则跳出本次循环
        if py_ver_info == 3:
            r = input('Enter a ID(number) for pakage: ')
        else:
            r = raw_input('Enter a ID(number) for pakage: ')
        if r.isdigit():
            r = int(r)
        else:
            continue
        # 判断输入的数字，是否在引用范围之内，如果是则跳出循环，如果否则要求继续输入
        if r < len(pkg_list):
            logger.info('You choice is: [%s] --- %s' % (r, pkg_list[r]))
            break
    # 判断异常
    try:
        pull_apk(pkg_list[r])
    except Exception as e:
        logger.exception('Exception: %s, %s' % (Exception, e))
        logger.info('Try again and enter a number.')
