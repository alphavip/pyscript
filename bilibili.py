'''
Author: alphachen
Date: 2023-11-28 18:07:47
LastEditTime: 2023-12-08 16:38:33
LastEditors: alphachen
Description: 
FilePath: /download/bilibili.py
版权声明
'''
# -*- coding: utf-8 -*-
import requests
import urllib
import time
import json
import random
import headers
import myutil
import os
import threading
from urllib.parse import urlparse

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory

#https://www.bilibili.com/video/BV1mc411Q71M/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=8f98cd6cbdf2557adc95f04f10484cbd


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


class WinGUI(Tk):

    def __init__(self):
        super().__init__()
        self.__win()

        self.path = StringVar()
        self.inputurl = StringVar()
        self.path.set('/Users/alphachen/Music')
        self.tk_button_dirselect = self.__tk_button_dirselect(self)
        self.tk_input_vid = self.__tk_input_vid(self)
        self.tk_button_download = self.__tk_button_download(self)
        self.tk_text_log = self.__tk_text_log(self)
        self.tk_input_path = self.__tk_input_path(self)
        self.inputurl.set("填写视频的url")

    def __win(self):
        self.title("下载B站音频")
        # 设置窗口大小、居中
        width = 943
        height = 536
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
                                    (screenheight - height) / 2)
        self.geometry(geometry)
        #self.iconbitmap('app.ico')

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)

        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw,
                   rely=y / ph,
                   relheight=h / ph,
                   anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw,
                   rely=(y + h) / ph,
                   relwidth=w / pw,
                   anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_button_dirselect(self, parent):
        btn = Button(
            parent,
            text="选择",
            takefocus=False,
        )
        btn.place(x=750, y=90, width=88, height=40)
        return btn

    def __tk_input_vid(self, parent):
        ipt = Entry(parent, textvariable=self.inputurl)
        ipt.place(x=50, y=150, width=690, height=40)
        return ipt

    def __tk_button_download(self, parent):
        btn = Button(
            parent,
            text="下载",
            takefocus=False,
        )
        btn.place(x=750, y=150, width=88, height=40)
        return btn

    def __tk_text_log(self, parent):
        text = Text(parent)
        text.place(x=50, y=200, width=795, height=260)
        self.create_bar(parent, text, True, False, 50, 200, 795, 260, 943, 536)
        return text

    def __tk_input_path(self, parent):
        ipt = Entry(parent, textvariable=self.path)
        ipt.place(x=50, y=90, width=690, height=40)
        return ipt


class Win(WinGUI):

    def __init__(self):
        super().__init__()
        self.__event_bind()
        self.threads = []

    def __dirSelect(self, evt):
        path_ = askdirectory()
        self.path.set(path_)

    def __startDownLoad(self, evt):
        bvid = self.inputurl.get()
        if len(bvid) == 0:
            self.tk_text_log.insert(END, "请输入视频url\n")
            return
        for thread1 in self.threads:
            thread1.join()
        thread = threading.Thread(target=self.__download, name="download")
        thread.start()
        self.threads.append(thread)

    def __startEditUrl(self, evt):
        self.inputurl.set("")

    def _onbvidhelp(self, evt):
        self.tk_text_log.insert(SEL_FIRST, "BV号是视频的id\n")

    def __event_bind(self):
        self.tk_button_dirselect.bind('<Button-1>', self.__dirSelect)
        self.tk_button_download.bind('<Button-1>', self.__startDownLoad)
        self.tk_input_vid.bind('<Button-1>', self.__startEditUrl)
        #self.tk_input_vid.bind('<Enter>', self._onbvidhelp)
        pass

    def __download(self):
        urlret = urlparse(self.tk_input_vid.get())
        paths = urlret.path.split('/')
        bvid = ""
        if len(paths) > 2:
            bvid = paths[2]
        else:
            self.tk_text_log.insert(END, "请输入正确的b站url\n")
            return
        self.tk_text_log.insert(END, "解析出来的bvid是:{}\n".format(bvid))
        vc = self.__getCidAndTitle(bvid)
        if len(vc.page_list) == 0:
            self.tk_text_log.insert(END, "视频不存在\n")
            return
        self.__getAudio(vc)

    def __getData(self, url):
        resp = requests.get(url, headers=headers)
        if resp.status_code >= 300:
            self.tk_text_log.insert(
                END, str.format("HTTP ERROR:{}\n", resp.status_code))
            return False
        jsonData = resp.json()
        if "data" not in jsonData:
            self.tk_text_log.insert(END, "找不到数据\n")
            return False
        return resp.json()['data']

    def __getCidAndTitle(self, bvid):
        url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
        data = self.__getData(url)
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

    def __getAudio(self, vc: VideoContent):
        if len(vc.title) == 0:
            self.tk_text_log.insert(END, "error bv")
            return
        baseUrl = 'http://api.bilibili.com/x/player/playurl?fnval=16&'
        self.tk_text_log.insert(
            END, str.format("{}一共{}页\n", vc.title, len(vc.page_list)))
        useTime = 0
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
                ('Referer',
                 'https://api.bilibili.com/x/web-interface/view?bvid=' +
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
                targetpath = myutil.mkdir(
                    os.path.join(self.path.get(), vc.title))
                filename = os.path.join(
                    targetpath, str.format('P{:0>3d}_{}', item.page,
                                           item.title))
                self.tk_text_log.insert(
                    END, str.format("start donwload:{}\n", item.title))
                urllib.request.urlretrieve(url=audioUrl,
                                           filename=filename + '.mp3')
            except Exception as e:
                self.tk_text_log.insert(END, "下载失败，因为：{}\n".format(e))
            ed = time.time()
            pageUse = round(ed - st, 2)
            useTime += pageUse
            self.tk_text_log.insert(
                END,
                str.format("{}s download finish:{}-{}\n", pageUse, title,
                           item.title))
            time.sleep(1)
        self.tk_text_log.insert(
            END, str.format("{}下载完了,用时{}s\n", vc.title, useTime))


if __name__ == "__main__":
    win = Win()
    win.mainloop()
