"""
Author: alphachen
Date: 2024-06-28 10:34:50
LastEditTime: 2024-06-28 10:34:51
LastEditors: alphachen
Description: 
FilePath: /download/dwpic_240628.py
版权声明
"""

import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from easyget import dlpic


url = "https://t66y.com/htm_data/2405/7/6307227.html"
save_dir = "picture"
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

ua = UserAgent()
headers = {
    "User-Agent": ua.random,
}

response = requests.get(url=url, headers=headers, proxies=proxies)
soup = BeautifulSoup(response.text, "html.parser")
alltagtmg = soup.find_all("img")

# with open("test.html", "w", encoding="utf-8") as f:
#     f.write(response.text)
# print(soup.title.string)

imglinklist = []
for imgtag in alltagtmg:
    taglink = imgtag.get("ess-data")
    if taglink is None or taglink == "":
        continue
    imglinklist.append(taglink)

# dlpic(imglinklist, "picture/清清库存，全是屁股。这波基本没漏B（四）[100P]")
print("over")
