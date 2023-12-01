'''
Author: alphachen
Date: 2023-11-28 18:57:11
LastEditTime: 2023-11-28 20:31:30
LastEditors: alphachen
Description: 
FilePath: /pywork/pyscript/download/myutil.py
版权声明
'''
# -*- coding: utf-8 -*-

import os


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
