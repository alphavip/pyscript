'''
Author: alphachen
Date: 2023-08-15 15:31:22
LastEditTime: 2023-08-18 15:13:04
LastEditors: alphachen
Description: 
FilePath: /pywork/pyscript/download/autosign.py
版权声明
'''
import os
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random

fuliba_COOKIE = 'X_CACHE_KEY=45358fd2fde51ef5f608b03faa37f020; S5r8_2132_lastvisit=1689850740; S5r8_2132_lastcheckfeed=78965%7C1689854350; S5r8_2132_nofavfid=1; S5r8_2132_atarget=1; S5r8_2132_smile=1D1; S5r8_2132_visitedfid=2D62D40; S5r8_2132_ulastactivity=48c996SbC6Wtvf8dU5Af88IgqiAubySxX4LmtbiWdRXB8dF0M4bo; S5r8_2132_st_p=78965%7C1692340369%7C42fa37e536053e2ed7c24077f7c5be60; S5r8_2132_viewid=tid_217505; S5r8_2132_sid=pW9l7V; S5r8_2132_lip=50.7.250.114%2C1692340655; S5r8_2132_st_t=78965%7C1692342641%7Cfcd310f4f13ccfc4a4c8672d6adab96a; S5r8_2132_forum_lastvisit=D_2_1692342641; S5r8_2132_sendmail=1; S5r8_2132_lastact=1692342642%09misc.php%09patch'

# 从环境变量中获取Cookie
cookie_string = fuliba_COOKIE
# 将从环境变量中读取的Cookie字符串转换为字典格式
cookies1 = {
    cookie.split('=')[0]: cookie.split('=')[1]
    for cookie in cookie_string.split('; ')
}

url = "https://www.wnflb2023.com/forum.php?mod=forumdisplay&fid=2&filter=author&orderby=dateline"

# User-Agent，模拟浏览器发送请求
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

headers = {'user-agent': random.choice(user_agent)}

# 发送GET请求，获取网页内容
response = requests.get(url, headers=headers, cookies=cookies1)
# ccraper = cfscrape.create_scraper()
# response = ccraper.get(url)
print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')

# 从网页内容中解析出formhash的值
formhash = soup.find('a', {
    'href': lambda x: x and 'formhash' in x
}).get('href').split('formhash=')[-1]

# 解析网页内容，寻找表示签到状态的元素
sign_status = soup.find(id="fx_checkin_b")

# 判断是否已经签到
ok = []
if sign_status and '已签到' in sign_status.get('alt', ''):
    print("已经签到过了")
    ok.append("已经签到过了")
else:
    # 如果没有签到，执行签到操作

    print("检测到还未签到，现在开始签到")
    time.sleep(1.5)
    print("开始签到")

    sign_in_url = f"https://www.wnflb2023.com/plugin.php?id=fx_checkin:checkin&formhash={formhash}"
    response = requests.get(sign_in_url, headers=headers, cookies=cookies1)
    # 根据返回状态码判断签到是否成功
    if response.status_code == 200:
        print("签到成功")
        ok.append("签到成功")
    else:
        print("签到失败")
        ok.append("签到失败")

# 不论是否签到，都获取并显示签到信息
info_url = "https://www.wnflb2023.com/plugin.php?id=fx_checkin:list"
response = requests.get(info_url, headers=headers, cookies=cookies1)
soup = BeautifulSoup(response.text, 'html.parser')

# 获取签到信息
outer_div = soup.find('div', class_='fx_225')
if outer_div is not None:
    user_info_ul = outer_div.find('ul', class_='fx_user-info')
    if user_info_ul is not None:
        # 获取所有的li元素
        user_info_list = user_info_ul.find_all('li')

        # 从每个li元素中获取文本
        user_info = [li.get_text(strip=True) for li in user_info_list]

        # 移除最后一个元素的最后三个字符（即 "-5"）
        user_info[-1] = user_info[-1][:-3]

        # 打印用户信息
        print("签到信息：")
        for info in user_info:
            print(info)
    else:
        print("未找到签到信息")
else:
    print("未找到外层div")

# 访问另一页面获取用户资产信息
assets_url = "https://www.wnflb2023.com/home.php?mod=spacecp&ac=credit&showcredit=1"
response = requests.get(assets_url, headers=headers, cookies=cookies1)
soup = BeautifulSoup(response.text, 'html.parser')

# 获取用户资产信息
assets_ul = soup.find('ul', class_='creditl mtm bbda cl')
if assets_ul is not None:
    # 获取所有的li元素
    assets_list = assets_ul.find_all('li')

    # 从每个li元素中获取文本，并移除不需要的部分
    assets_info = []
    for li in assets_list:
        text = li.get_text(strip=True)
        if '立即充值' in text:
            text = text.split('立即充值')[0]
        assets_info.append(text)

    # 打印用户资产信息
    print("我的资产：")
    for info in assets_info:
        print(info)
else:
    print("未找到资产信息")


# 发送邮件通知
def send_email(subject, content):
    # QQ邮箱SMTP服务器地址
    mail_host = 'smtp.qq.com'
    # QQ邮箱SMTP服务器端口
    mail_port = 465

    # 发件人邮箱
    mail_sender = os.getenv("fuliba_fa")
    # 邮箱授权码
    mail_license = os.getenv("fuliba_ma")

    # 收件人邮箱，可以是QQ邮箱
    mail_receivers = [os.getenv("fuliba_shou")]

    mm = MIMEText(content, _subtype='plain', _charset='utf-8')
    mm['Subject'] = Header(subject, 'utf-8')
    mm['From'] = mail_sender  # 发件人邮箱
    mm['To'] = ';'.join(mail_receivers)  # 收件人邮箱列表，用分号隔开

    try:
        smtp_obj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtp_obj.login(mail_sender, mail_license)
        smtp_obj.sendmail(mail_sender, mail_receivers, mm.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("邮件发送失败", e)


# 在签到成功或失败后，调用这个函数发送邮件
# 在签到成功或失败后，调用这个函数发送邮件
if response.status_code == 200:
    user_info_str = "\n".join(user_info)
    assets_info_str = "\n".join(assets_info)
    email_content = f"{ok[0]}\n\n用户信息:\n{user_info_str}\n\n资产信息:\n{assets_info_str}"
    print('签到通知', email_content)
else:
    print('签到通知', '签到失败')
