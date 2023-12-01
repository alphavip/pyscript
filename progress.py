'''
Author: alphachen
Date: 2023-05-22 18:48:15
LastEditTime: 2023-05-22 18:57:16
LastEditors: alphachen
Description: 
FilePath: /download/progress.py
版权声明
'''


def progress(percent, width=50):
    if percent >= 100:
        percent = 100
    show_str = ('[%%-%ds]' % width) % ((width * percent // 100) * '#')
    print('\r%s %d%%' % (show_str, percent), end='')
