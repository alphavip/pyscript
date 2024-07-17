import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
from easyget import dlpic
import re
from myutil import myrequest


def loadcache():
    index = 0
    with open(".cache.txt", "r") as f:
        try:
            index = int(f.readline())
        except:
            index = 0
    return index


def savecache(index):
    with open(".cache.txt", "w") as f:
        f.write(str(index))


nowindex = loadcache()

save_dir = "picture"
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}


url = "https://t66y.com/@www1120"
useragent = UserAgent()
stragent = str(useragent.random)
print(stragent)
headers = {"User-Agent": stragent}
response = myrequest(url=url, headers=headers, proxies=proxies)
if response is None:
    exit(1)
soup = BeautifulSoup(response.text, "html.parser")

keytxt = "部都是适合后入的肥臀"
maxindex = nowindex

allatags = soup.find_all("a")
for th in allatags:
    thtxt = th.get_text()
    if keytxt in thtxt:
        chlink = th.get("href")
        reallink = os.path.join("https://t66y.com", chlink)

        index = 0
        reResult = re.search(pattern="\\d+\[", string=thtxt)
        if reResult == None:
            continue

        index = int(reResult.group(0)[:-1])

        if index <= nowindex:
            break
        if index > maxindex:
            maxindex = index
        print(thtxt + ":" + reallink)
        save_dir1 = os.path.join(save_dir, thtxt)
        if os.path.exists(save_dir1):
            continue

        chres = requests.get(url=reallink, headers=headers, proxies=proxies)
        chsoup = BeautifulSoup(chres.text, "html.parser")

        imglinks = []
        for img in chsoup.findAll("img"):
            imglink = img.get("ess-data")
            if imglink is None or imglink == "" or imglink[-3:] != "jpg":
                continue

            imglinks.append(imglink)

        dlpic(imglinks, save_dir1)
savecache(maxindex)
print("over")
