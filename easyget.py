'''
Author: alphachen
Date: 2023-05-22 16:55:47
LastEditTime: 2023-11-08 12:08:44
LastEditors: alphachen
Description: 
FilePath: /pywork/pyscript/download/easyget.py
版权声明
'''
import requests
import os
from progress import progress
import random

user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

headers = {'user-agent': random.choice(user_agent)}


def dlpic(img_list, save_dir):
    if not os.path.exists(save_dir):  # 如果文件夹不存在，就创建
        os.makedirs(save_dir)
    total = len(img_list)
    index = 0
    for img_url in img_list:
        img_url = img_url.strip()
        try:
            response_img = requests.get(url=img_url,
                                        headers=headers,
                                        proxies=proxies)
            # 获取图片名
            img_name = img_url.split('/')[-1]
        except Exception as error:
            print("requests except error:" + error)
        else:
            if response_img.status_code == 200:
                # 保存图片
                with open(f'{save_dir}/{img_name}', 'wb') as f:
                    f.write(response_img.content)
                    index = index + 1
                    progress(index * 100 // total)
            else:
                print("requests error:" + str(response_img.status_code))


# with open("link.txt") as f:
#     lines = f.read().splitlines()
#     dlpic(lines, "./picture")

linkline = "http://175.178.173.16:5678/d/%E6%9C%89%E5%A3%B0%E4%B9%A6/%E6%9C%89%E5%A3%B0%E5%B0%8F%E8%AF%B4/%E5%86%B7%E6%A1%88%E9%87%8D%E5%90%AF/{:0>3d}.wma"
links = []
for i in range(1, 10):
    links.append(linkline.format(i))
dlpic(links, "./二号首长1")
