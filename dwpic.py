import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
from easyget import dlpic

save_dir = "picture"
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}


url = "https://t66y.com/@欧比斯拉奇"
useragent = UserAgent()
stragent = str(useragent.random)
print(stragent)
headers = {"User-Agent": stragent}
response = requests.get(url=url, headers=headers, proxies=proxies)
soup = BeautifulSoup(response.text, "html.parser")

allatags = soup.find_all("a")
for th in allatags:
    if "库存" in th.get_text():
        chlink = th.get("href")
        reallink = os.path.join("https://t66y.com", chlink)
        print(th.get_text() + ":" + reallink)

        save_dir1 = os.path.join(save_dir, th.get_text())
        if os.path.exists(save_dir1):
            continue

        chres = requests.get(url=reallink, headers=headers, proxies=proxies, verify=False)
        chsoup = BeautifulSoup(chres.text, "html.parser")

        imglinks = []
        for img in chsoup.findAll("img"):
            imglink = img.get("ess-data")
            if imglink is None or imglink == "" or imglink[-3:] != "jpg":
                continue

            imglinks.append(imglink)

        dlpic(imglinks, save_dir1)

print("over")
