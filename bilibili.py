'''
Author: alphachen
Date: 2023-11-28 18:07:47
LastEditTime: 2023-11-30 21:03:12
LastEditors: alphachen
Description: 
FilePath: /pywork/pyscript/download/bilibili.py
版权声明
'''
# -*- coding: utf-8 -*-
import requests
import urllib
import time
import argparse
import json
import random
import headers
import myutil
import os
import csv

downloaddir = '/Users/alphachen/Music/'


class PageContent(object):

    def __init__(self):
        self.cid = 0
        self.title = ''
        self.page = 0


class VideoContent(object):

    def __init__(self):
        self.title = ''
        self.page_list = []
        self.bvid = ''


headers = {'user-agent': random.choice(headers.user_agent)}


def getData(url):
    resp = requests.get(url, headers=headers)
    if resp.status_code >= 300:
        print("HTTP ERROR:", resp.status_code)
        return False
    jsonData = resp.json()
    if "data" not in jsonData:
        print("找不到数据")
        return False
    return resp.json()['data']


def getCidAndTitle(bvid):
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
    data = getData(url)
    vc = VideoContent()
    vc.bvid = bvid
    if data != False:
        vc.title = data['title']
        pagelen = len(data['pages'])
        for i in range(0, pagelen):
            page = PageContent()
            page.page = i + 1
            page.cid = data['pages'][i]['cid']
            page.title = data['pages'][i]['part']
            vc.page_list.append(page)

    return vc


def getAudio(vc: VideoContent):
    if len(vc.title) == 0:
        print("error bv")
        return
    baseUrl = 'http://api.bilibili.com/x/player/playurl?fnval=16&'

    for item in vc.page_list:
        st = time.time()
        bvid, cid, title = vc.bvid, item.cid, vc.title
        url = baseUrl + 'bvid=' + bvid + '&cid=' + str(cid)

        res = requests.get(url, headers=headers)
        resjson = json.loads(res.text)
        audioUrl = resjson['data']['dash']['audio'][0]['baseUrl']

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent',
             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'
             ),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            ('Referer', 'https://api.bilibili.com/x/web-interface/view?bvid=' +
             bvid),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        if "/" in title:
            title = " ".join(title.split("/"))
        if '\\' in title:
            title = " ".join(title.split("\\"))
        try:
            #curdir = os.path.split(os.path.realpath(__file__))[0]
            targetpath = myutil.mkdir(os.path.join(downloaddir, vc.title))
            filename = os.path.join(
                targetpath, str.format('P{:0>3d}_{}', item.page, item.title))
            urllib.request.urlretrieve(url=audioUrl,
                                       filename=filename + '.mp3')
        except Exception as e:
            print("下载失败，因为：", e)
        ed = time.time()
        print(str(round(ed - st, 2)) + 's download finish:', title, item.title)
        time.sleep(1)


def getBVList(arg, extra_args):
    BVList = []
    if arg.f:
        with open(extra_args[0], 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                BVList.append(line[0])
    elif arg.c:
        BVList = [i for i in extra_args]

    else:
        raise 'Please select an input method.'

    return BVList


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store_true')
    parser.add_argument('-c', action='store_true')
    args, extra_args = parser.parse_known_args()
    BVList = getBVList(args, extra_args)

    print(f'Downloader Start! {BVList}')
    st = time.time()
    for bv in BVList:
        getAudio(getCidAndTitle(bv))
    ed = time.time()
    print('Download Finish All! Time consuming:',
          str(round(ed - st, 2)) + ' seconds')
