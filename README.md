# About AndroidTestKit

## Introduction

AndroidTestKit is a test script collection, usage to Android test, and it can works on Python2.x/Python3.x. For more information please refer to [CHANGELOG.md](https://github.com/kevin-zsj/AndroidTestKit/blob/master/CHANGELOG.md)

## Basic Usage

```text
git clone git@github.com:kevin-zsj/AndroidTestKit.git
cd AndroidTestKit
python xxx.py
```
#### Get Apks
Run script:
```commandline
python ./get_apk.py
```
Enter a number:
```text
2018-10-18 16:48:18,344 GETAPK INFO 1. Pull apk of RECENT;
2018-10-18 16:48:18,345 GETAPK INFO 2. Pull apks all of the third party;
Enter a ID(number) :
```

#### Get Logs
Run script:
```commandline
python ./get_log.py
```

#### Auto Install

Set apks path, like as:
```python
apksPath = '/Users/test/apks/'
```
Run script:
```commandline
python ./autoInstallApk.py
```

## Author

AndroidTestKit is developed and maintained by Kevin.Zhang ([testcn@vip.qq.com](testcn@vip.qq.com))

## License

AndroidTestKit is released under the MIT License. See LICENSE for more information.