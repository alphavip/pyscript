"""
Author: alphachen
Date: 2024-07-15 16:37:55
LastEditTime: 2024-07-15 16:37:55
LastEditors: alphachen
Description: 
FilePath: /download/dwpic copy.py
版权声明
"""

import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
from easyget import dlpic
import re
from myutil import myrequest
from urllib.parse import urljoin

cachefile = ".novelcache.txt"


def loadcache():
    index = 0
    with open(cachefile, "r+") as f:
        try:
            index = int(f.readline())
        except:
            index = 0
    return index


def savecache(index):
    with open(cachefile, "w") as f:
        f.write(str(index))


def writef(chsoup, nf):
    for img in chsoup.find_all("p"):
        tmptxt = img.get_text()
        writef = True
        for notxt in invalidtxt:
            if re.search(pattern=notxt, string=tmptxt) is not None:
                writef = False
                break
        if writef:
            nf.write(tmptxt)


nowindex = loadcache()

save_dir = "庆余年"
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}


url = "https://199822.xyz/novel/8989"
useragent = UserAgent()
stragent = str(useragent.random)
print(stragent)
headers = {"User-Agent": stragent}
response = myrequest(url=url, headers=headers, proxies=proxies)
if response is None:
    exit(1)
soup = BeautifulSoup(response.text, "html.parser")

keytxt = "第*章"
invalidtxt = ["199822.xyz", "繁體版", "书友最值得收藏"]
allatags = soup.find_all(attrs={"id": "ul_all_chapters"})
index = 0
nf = open("庆余年秘史.txt", mode="w", encoding="utf-8")
for th in allatags:
    for litag in th.find_all("li"):
        thtxt = litag.get_text()
        reresult = re.search(pattern=keytxt, string=thtxt)
        if reresult is not None:
            chlink = litag.a.get("href")
            if chlink is None:
                continue
            reallink = urljoin("https://199822.xyz", chlink)
            index = index + 1
            if index <= nowindex:
                continue

            print(thtxt + ":" + reallink)

            chres = requests.get(url=reallink, headers=headers, proxies=proxies)
            chsoup = BeautifulSoup(chres.text, "html.parser")

            imglinks = []
            novelindex = ""
            if index != 1:
                nf.write("\n\n")
            nf.write(thtxt)
            nf.write("\n\n")
            writef(chsoup, nf)
            nexttag = chsoup.find_all(attrs={"id": "next_url"})
            if len(nexttag) > 0:
                chlink = nexttag[0].get("href")
                if chlink is None:
                    continue
                reallink = urljoin("https://199822.xyz", chlink)
                print(thtxt + ":" + reallink)

                chres = requests.get(url=reallink, headers=headers, proxies=proxies)
                chsoup = BeautifulSoup(chres.text, "html.parser")
                writef(chsoup, nf)

nf.close()
savecache(index)
print("over")
