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
            response = requests.get(url=url, headers=headers, proxies=proxies, verify=False)
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
import requests
from bs4 import BeautifulSoup
import chardet

def get_html_encoding(response):
    # 步骤1：优先从响应头获取
    if response.encoding:
        return response.encoding
    
    # 步骤2：从 meta 标签获取
    soup = BeautifulSoup(response.content, "lxml")
    # 匹配 <meta charset="xxx">
    meta_charset = soup.find("meta", attrs={"charset": True})
    if meta_charset:
        return meta_charset["charset"].upper()  # 统一转为大写（如 utf-8 → UTF-8）
    # 匹配旧版 <meta http-equiv="Content-Type" content="text/html; charset=xxx">
    meta_http = soup.find("meta", attrs={"http-equiv": lambda x: x and x.lower() == "content-type"})
    if meta_http and "content" in meta_http.attrs:
        content = meta_http["content"].lower()
        if "charset=" in content:
            return content.split("charset=")[1].strip().upper()
    
    # 步骤3：自动检测
    detect_result = chardet.detect(response.content)
    return detect_result["encoding"] or "UTF-8"

# 测试使用
# if __name__ == "__main__":
#     target_url = "https://www.baidu.com"  # 替换为你的目标网页
#     encoding = get_html_encoding(target_url)
#     print(f"最终确定的编码：{encoding}")
    
#     # 用正确编码解析网页
#     response = requests.get(target_url)
#     html_text = response.content.decode(encoding, errors="ignore")
#     soup = BeautifulSoup(html_text, "lxml")
#     # 后续即可正常解析节点
#     print("网页标题：", soup.title.text)

# print(os.environ["HOME"])
# print(os.path.expandvars("$HOME"))
# print(os.path.expanduser("~"))
