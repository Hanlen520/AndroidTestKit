# Version log

## version 2.0.0 - 2018.10.18

    1. 支持一次性提取所有第三方安装的apk（非系统内置）
    2. 支持提取最近使用过的apk
    3. 对提取出的apk进行命名，不再只显示包名（如：Quora_2.7.23_com.quora.android.apk）
    4. 新增autoInstallApk脚本，在脚本指定路径后，可遍历安装所有目录下的apk（不含子目录）
    5. 注释掉anr和tombstones的获取，因为在导出Bugreport时已经包含
    6. 其它稳定性优化
    
## version 1.1.1 - 2018.07.25

    1. 增加抓取log后截图
    2. 优化代码面向对象

## version 0.1.0 - 2018.06.14

    1. 改变了获取log的方式，避免在某种情况下因字符问题导致的log获取失败的问题
    2. 现在获取的apk会统一放到apk文件夹中

## version 0.0.5 - 2018.04.10

    1. get log和get apk都已兼容Python2、Python3
    2. 使用logging代替print输出控制流
    3. 获取apk脚本在关键字没有任何匹配时可以循环输入，不必重新运行脚本

## version 0.0.4 - 2018.01.18

> Added
* 增加获取adb root权限

> Fixed
* 解决在Windows平台上运行时报错（UnicodeEncodeError）

## version 0.0.3 - 2018.01.16

> Changed
* 使用logcat的-d参数，替代使用时间戳的方式判断logcat结束标志

## version 0.0.2 - 2018.01.11

> Added
* 获取默认logcat(等同于“adb shell logcat”)

> Fixed
* Android系统时间判断错误，导致main，radio等log只有一行

## version 0.0.1 - 2018.1.10

> Added
* 第一个版本
