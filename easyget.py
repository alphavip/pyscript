"""
Author: alphachen
Date: 2023-05-22 16:55:47
LastEditTime: 2023-11-08 12:08:44
LastEditors: alphachen
Description: 
FilePath: /pywork/pyscript/download/easyget.py
版权声明
"""

import os
import random
import time
import requests
import urllib3
from progress import progress
from fake_useragent import UserAgent

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}
useragent = UserAgent()
headers = {"user-agent": useragent.random}

urllib3.disable_warnings()


def dlpic(img_list, save_dir):
    if not os.path.exists(save_dir):  # 如果文件夹不存在，就创建
        os.makedirs(save_dir)
    total = len(img_list)
    index = 0
    for img_url in img_list:
        if img_url == None or img_url == "":
            index = index + 1
            progress(index * 100 // total)
            continue
        img_url = img_url.strip()
        while True:
            try:
                response_img = requests.get(url=img_url, headers=headers, proxies=proxies)
                # 获取图片名
                img_name = img_url.split("/")[-1]
            except:
                print("requests except error")
                print("re trying...{}".format(img_url))
                time.sleep(random.randint(1, 3))
            else:
                if response_img.status_code == 200:
                    # 保存图片
                    with open(f"{save_dir}/{img_name}", "wb") as f:
                        f.write(response_img.content)
                        index = index + 1
                        progress(index * 100 // total)
                    break
                else:
                    print("requests error:{0}|{1}".format(str(response_img.status_code), img_url))
                    break
            # time.sleep(random.randfloat(0, 1.0))
    print("")


# with open("link.txt") as f:
#     lines = f.read().splitlines()
#     dlpic(lines, "./picture")

# linkline = "http://175.178.173.16:5678/d/%E6%9C%89%E5%A3%B0%E4%B9%A6/%E6%9C%89%E5%A3%B0%E5%B0%8F%E8%AF%B4/%E5%86%B7%E6%A1%88%E9%87%8D%E5%90%AF/{:0>3d}.wma"
# links = []
# for i in range(1, 10):
#     links.append(linkline.format(i))
# dlpic(links, "./二号首长1")
