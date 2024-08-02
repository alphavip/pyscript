"""
Author: alphachen
Date: 2023-11-28 18:57:11
LastEditTime: 2023-11-28 20:31:30
LastEditors: alphachen
Description: 一些常用封装
FilePath: /pywork/pyscript/download/myutil.py
版权声明
"""

# -*- coding: utf-8 -*-

import datetime
import os
import requests
import time
import random


# 打印进度条
# 此函数用于在命令行中打印一个进度条，以直观地显示任务的完成情况
# 参数:
#   percent: 当前完成的百分比，整数类型
#   width: 进度条的宽度，整数类型，可选，默认为50
def progress(percent, width=50):
    # 确保percent不超过100，避免进度条显示不正确
    if percent >= 100:
        percent = 100
    # 构造进度条字符串，根据percent计算出相应数量的'#'字符
    show_str = ("[%%-%ds]" % width) % ((width * percent // 100) * "#")
    # 打印进度条，使用回车符和清除到行尾实现在同一行内更新进度
    print("\r%s %d%%" % (show_str, percent), end="")


def curdir():
    """
    获取当前工作目录。

    返回:
        当前工作目录的路径。

    """
    return os.getcwd()


def realdir():
    print(__file__)
    return os.path.split(os.path.realpath(__file__))[0]


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    return path


def return_last_month_fl_day():
    today = datetime.date.today()
    first_day = today.replace(day=1)
    last_month_last_day = first_day - datetime.timedelta(days=1)
    last_month_first_day = last_month_last_day.replace(day=1)
    return last_month_first_day, last_month_last_day


def myhomedir():
    return os.path.expanduser("~")


def myrequest(url: str, headers, proxies):
    while True:
        try:
            response = requests.get(url=url, headers=headers, proxies=proxies)
        except:
            print("requests except error")
            print("re trying...{}".format(url))
            time.sleep(random.randint(1, 3))
        else:
            if response.status_code == 200:
                return response
            else:
                print("requests error:{0}|{1}".format(str(response.status_code), url))
                return None


# print(os.environ["HOME"])
# print(os.path.expandvars("$HOME"))
# print(os.path.expanduser("~"))
