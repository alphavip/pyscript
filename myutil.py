"""
Author: alphachen
Date: 2023-11-28 18:57:11
LastEditTime: 2023-11-28 20:31:30
LastEditors: alphachen
Description: 
FilePath: /pywork/pyscript/download/myutil.py
版权声明
"""

# -*- coding: utf-8 -*-

import datetime
import os
import requests
import time
import random


def curdir():
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
