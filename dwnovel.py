"""
Author: alphachen
Date: 2024-07-15 16:37:55
LastEditTime: 2024-07-15 16:37:55
LastEditors: alphachen
Description: 
FilePath: /download/dwpic copy.py
版权声明
"""

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
from easyget import dlpic
import re
from myutil import myrequest
from myutil import get_html_encoding
from urllib.parse import urljoin
from lxml import etree



save_dir = "仙逆"
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}


url = "http://www.fx57.cn/fx57/film/animation/2024-12-02/3659.html"
useragent = UserAgent()
stragent = str(useragent.random)
print(stragent)
headers = {"User-Agent": stragent}
response = myrequest(url=url, headers=headers, proxies=proxies)
if response is None:
    exit(1)
    
encodingcode = get_html_encoding(response)
soup = BeautifulSoup(response.text, "html.parser")

dom = etree.HTML(str(soup))

# 2. 执行 XPath 表达式（修正你的路径，去掉开头的 http://）
# 注意：XPath 路径需要以 // 开头（或绝对路径 /html/...）
xpath_path = "/html/body/article/div[1]/div[2]/div[3]/div[3]/ul/li"
target_uls = dom.xpath(xpath_path)

rearray = []

with open(save_dir + ".txt", "w", encoding="utf-8") as f:

    for li in target_uls:
        li_text = li.xpath('string(.)').strip()  # string(.)获取所有子节点文本，strip()去首尾空格
        
        # 过滤空文本（包含全空格的情况）
        if not li_text:  # 等价于 li_text == ""，更简洁
            continue
        
        # 处理编码并输出（如果网页编码本身是utf-8，这一步可省略）
        # 先按网页编码编码，再转回utf-8解码，确保输出无乱码
        try:
            output_text = li_text.encode(encodingcode).decode("utf-8")
        except UnicodeEncodeError:
            # 兜底处理编码异常
            print("li文本内容（编码异常）：", li_text)
        if output_text.find("2160p") >= 0:
            continue
        # 【补充】如果你需要获取li下a标签的href属性（常见需求）
        # 比如<li><a href="xxx.html">文本</a></li>
        href = li.xpath('.//a/@href')  # .// 表示在当前li节点下查找a标签
        if href:  # 存在href属性时输出
            f.write(output_text + " " + href[0] + "\n")
            rearray.append(href[0])
    for href in rearray:
        f.write(href + "\n")

