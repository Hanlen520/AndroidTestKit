# Version log
* ### version 0.1.0 - 2018.06.14
    1. 改变了获取log的方式，避免在某种情况下因字符问题导致的log获取失败的问题
    2. 现在获取的apk会统一放到apk文件夹中
    
* ### version 0.0.4 - 2018.01.18

    #### Added
    * 增加获取adb root权限

    #### Changed
    * 无

    #### Fixed
    * 解决在Windows平台上运行时报错（UnicodeEncodeError）

    #### Removed
    * 无

* ### version 0.0.3 - 2018.01.16

    #### Added
    * 无

    #### Changed
    * 使用logcat的-d参数，替代使用时间戳的方式判断logcat结束标志

    #### Fixed
    * 无

    #### Removed
    * 无

* ### version 0.0.2 - 2018.01.11

    #### Added
    * 获取默认logcat(等同于“adb shell logcat”)

    #### Changed
    * 无

    #### Fixed
    * Android系统时间判断错误，导致main，radio等log只有一行

    #### Removed
    * 无

* ### version 0.0.1 - 2018.1.10

    #### Added
    * 第一个版本
