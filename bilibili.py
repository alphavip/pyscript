"""
Author: alphachen
Date: 2023-11-28 18:07:47
LastEditTime: 2023-12-27 20:48:51
LastEditors: alphachen
Description: 
FilePath: /download/bilibili.py
版权声明
"""

# -*- coding: utf-8 -*-

import json
import os
import random
import threading
import time
import urllib
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.ttk import *
from urllib.parse import urlparse

import requests

import headers
import myutil

# https://www.bilibili.com/video/BV1mc411Q71M/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=8f98cd6cbdf2557adc95f04f10484cbd


class PageContent(object):
    def __init__(self):
        self.cid = 0
        self.title = ""
        self.page = 0


class VideoContent(object):
    def __init__(self):
        self.title = ""
        self.page_list = []
        self.bvid = ""


headers = {"user-agent": random.choice(headers.user_agent)}


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()

        self.path = StringVar()
        self.inputurl = StringVar()
        self.inputpgae = StringVar()
        self.progress = IntVar(value=0)
        myhome = myutil.myhomedir()
        self.path.set(os.path.join(myhome, "Music"))
        self.tk_button_dirselect = self.__tk_button_dirselect(self)
        self.tk_input_vid = self.__tk_input_vid(self)
        self.tk_input_page = self.__tk_input_page(self)
        # self.tk_label_page = self.__tk_label_page(self)
        self.tk_button_download = self.__tk_button_download(self)
        self.tk_text_log = self.__tk_text_log(self)
        self.tk_input_path = self.__tk_input_path(self)
        self.tk_progressbar_lqnndtsc = self.__tk_progressbar_lqnndtsc(self)

        self.inputurl.set("填写视频的url")
        self.inputpgae.set("第几页")
        self.tk_text_log.insert(END, "欢迎使用B站音频下载器\n填写视频的url\n如果需要指定页,填上第几页\n")

    def __win(self):
        self.title("下载B站音频")
        # 设置窗口大小、居中
        width = 900
        height = 536
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = "%dx%d+%d+%d" % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        # self.iconbitmap('app.ico')

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar:
                vbar.lift(widget)
            if hbar:
                hbar.lift(widget)

        def hide():
            if vbar:
                vbar.lower(widget)
            if hbar:
                hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar:
            vbar.bind("<Enter>", lambda e: show())
        if vbar:
            vbar.bind("<Leave>", lambda e: hide())
        if hbar:
            hbar.bind("<Enter>", lambda e: show())
        if hbar:
            hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor="ne")

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor="sw")

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
        ipt.place(x=50, y=150, width=600, height=40)
        return ipt

    def __tk_input_page(self, parent):
        ipt = Entry(parent, textvariable=self.inputpgae)
        ipt.place(x=660, y=150, width=80, height=40)
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
        self.create_bar(parent, text, True, False, 50, 200, 795, 260, 900, 536)
        return text

    def __tk_input_path(self, parent):
        ipt = Entry(parent, textvariable=self.path)
        ipt.place(x=50, y=90, width=690, height=40)
        return ipt

    def __tk_progressbar_lqnndtsc(self, parent):
        progressbar = Progressbar(parent, orient=HORIZONTAL, variable=self.progress)
        progressbar.place(x=0, y=530, width=900, height=6)
        return progressbar


class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()
        self.threads = []

    def __dirSelect(self, evt):
        path_ = askdirectory()
        self.path.set(path_)

    def __startDownLoad(self, evt):
        for thread1 in self.threads:
            thread1.join()
        burl = self.inputurl.get()
        if len(burl) == 0:
            self.__insertToLTextEnd("请输入视频url\n")
            return
        urlret = urlparse(burl)
        paths = urlret.path.split("/")
        bvid = ""
        if len(paths) > 2 and paths[2][0:3] == "BV1":
            bvid = paths[2]
        else:
            self.__insertToLTextEnd("请输入正确的b站url\n")
            return

        self.__insertToLTextEnd("解析出来的bvid是:{}\n".format(bvid))

        thread = threading.Thread(target=self.__download, name="download", args=(bvid,))
        thread.start()
        self.threads.append(thread)

    def __startEditUrl(self, evt):
        istr = self.inputurl.get()
        if istr == "填写视频的url":
            self.__clearUrlStr()

    def __leaveUrlInput(self, evt):
        preStr = self.inputurl.get()
        if len(preStr) == 0:
            self.__resetUrlStr()

    # def __testF3(self, evt):
    #     self.__insertToLTextEnd("test f3\n")

    def _onbvidhelp(self, evt):
        self.tk_text_log.insert(SEL_FIRST, "BV号是视频的id\n")

    def __event_bind(self):
        self.tk_button_dirselect.bind("<Button-1>", self.__dirSelect)
        self.tk_button_download.bind("<Button-1>", self.__startDownLoad)
        self.tk_input_vid.bind("<Button-1>", self.__startEditUrl)
        self.tk_input_page.bind("<Button-1>", self.__startEditUrl)
        self.tk_input_vid.bind("<Leave>", self.__leaveUrlInput)
        self.tk_input_page.bind("<Leave>", self.__leaveUrlInput)
        # self.tk_input_vid.bind('<F3>', self.__testF3)
        # self.tk_input_vid.bind('<Enter>', self._onbvidhelp)
        pass

    def __download(self, bvid: str):
        vc = self.__getCidAndTitle(bvid)
        if len(vc.page_list) == 0:
            self.__insertToLTextEnd("视频不存在\n")
            return
        self.__getAudio(vc)

    def __getData(self, url):
        resp = requests.get(url, headers=headers)
        if resp.status_code >= 300:
            self.__insertToLTextEnd(str.format("HTTP ERROR:{}\n", resp.status_code))
            return False
        jsonData = resp.json()
        if "data" not in jsonData:
            self.__insertToLTextEnd("找不到数据\n")
            return False
        return resp.json()["data"]

    def __insertToLTextEnd(self, text: str):
        self.tk_text_log.insert(END, text)
        self.tk_text_log.see(END)

    def __clearUrlStr(self):
        self.inputurl.set("")
        self.inputpgae.set("")

    def __resetUrlStr(self):
        self.inputurl.set("填写视频的url")
        self.inputpgae.set("第几页")

    def __dlpage(self, item: PageContent, vc: VideoContent):
        st = time.time()
        pagesnum = len(vc.page_list)
        baseUrl = "http://api.bilibili.com/x/player/playurl?fnval=16&"
        bvid, cid, title = vc.bvid, item.cid, vc.title
        url = baseUrl + "bvid=" + bvid + "&cid=" + str(cid)

        res = requests.get(url, headers=headers)
        resjson = json.loads(res.text)
        audioUrl = resjson["data"]["dash"]["audio"][0]["baseUrl"]

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0"),
            ("Accept", "*/*"),
            ("Accept-Language", "en-US,en;q=0.5"),
            ("Accept-Encoding", "gzip, deflate, br"),
            ("Range", "bytes=0-"),
            ("Referer", "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid),  # 注意修改referer,必须要加的!
            ("Origin", "https://www.bilibili.com"),
            ("Connection", "keep-alive"),
        ]
        urllib.request.install_opener(opener)
        if "/" in title:
            title = " ".join(title.split("/"))
        if "\\" in title:
            title = " ".join(title.split("\\"))

        def __report(a, b, c):
            self.progress.set(int(100 * a * b / c))

        for i in range(1, 5):
            try:
                # curdir = os.path.split(os.path.realpath(__file__))[0]
                targetpath = myutil.mkdir(os.path.join(self.path.get(), vc.title))
                filename = os.path.join(targetpath, str.format("P{:0>3d}_{}", item.page, item.title))
                self.__insertToLTextEnd(str.format("第{}次尝试下载:第{:0>3d}/{:0>3d}页:《{}》\n", i, item.page, pagesnum, item.title))
                urllib.request.urlretrieve(url=audioUrl, filename=filename + ".mp3", reporthook=__report)
                break
            except Exception as e:
                self.__insertToLTextEnd("下载失败，因为：{}\n".format(e))
        ed = time.time()
        pageUse = round(ed - st, 2)
        self.__insertToLTextEnd(str.format("{}s download finish:第{:0>3d}页:{}-{}\n", pageUse, item.page, vc.title, item.title))
        time.sleep(1)
        return pageUse

    def __getCidAndTitle(self, bvid):
        url = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
        data = self.__getData(url)
        vc = VideoContent()
        vc.bvid = bvid
        if data != False:
            vc.title = data["title"]
            pagelen = len(data["pages"])
            for i in range(0, pagelen):
                page = PageContent()
                page.page = i + 1
                page.cid = data["pages"][i]["cid"]
                page.title = data["pages"][i]["part"]
                vc.page_list.append(page)

        return vc

    def __getAudio(self, vc: VideoContent):
        if len(vc.title) == 0:
            self.__insertToLTextEnd("error bv\n")
            return
        page = self.inputpgae.get()
        self.__insertToLTextEnd(str.format("{} 一共{}页,\n", vc.title, len(vc.page_list)))
        useTime = 0

        if len(page) > 0:
            page = int(page)
            if page > 0 and page <= len(vc.page_list):
                self.__insertToLTextEnd("指定下载{}页\n".format(page))
                useTime += self.__dlpage(vc.page_list[page - 1], vc)
        else:
            for item in vc.page_list:
                useTime += self.__dlpage(item, vc)
        self.__insertToLTextEnd(str.format("{}下载完了,用时{}s\n", vc.title, round(useTime, 2)))


if __name__ == "__main__":
    win = Win()
    win.mainloop()
