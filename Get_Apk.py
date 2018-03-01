# -*- coding:utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import os
import subprocess
import sys

adb_shell = 'adb shell'
apk_path = 'adb shell pm path'


# 根据包名获取apk路径
def get_pkg_path(x):
    cmd = ['adb', 'shell', 'pm', 'path', x]
    pkg = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    # 等待进行完成
    if pkg.wait() != 0:
        print("There were some errors")
    # 处理数据，将结果中的包名取出，并去掉换行符，因返回数据只有一行所以读取时只读一行
    # 只使用readline
    path = str(pkg.stdout.readline(), "utf-8")
    pkg_path = path.split(':')[1].strip()
    print('Package path is :', pkg_path)
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
    # 等待进程退出
    # if pkg_list.wait() != 0:
    #     print("There were some errors")
    # 读取所有数据
    pkgs = get_pkg_info.stdout.readlines()
    # 定义一个空列表，将原始数据中的"package:"和换行符去除后放入此列表。
    pkg_list = []
    for name in pkgs:
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
    pull = subprocess.check_call(pull_cmd)


if __name__ == '__main__':
    print('Wait for device:')
    os.system('adb root')
    os.system('adb wait-for-device')
    print('Device is fond.')
    # 输入一个包名中可能的关键字，可以方便过滤一部分应用
    keyword = input('Enter a "keyword" for package name: ')
    pkg_list = get_pkg_list(keyword)

    for m, n in enumerate(pkg_list):
        print("{id} --- {pkgname}".format(id=m, pkgname=n))
    r = input('Enter a ID(number) for pakage: ')
    while not r.isdigit():
        print('You enter in is not a number.')
        r = input('Enter a ID(number) for pakage: ')
    r = int(r)
    if r < len(pkg_list):
        print(r, pkg_list[r])
    try:
        pull_apk(pkg_list[r])
    except Exception as e:
        print(Exception, e, 'Try again and enter a number.')
