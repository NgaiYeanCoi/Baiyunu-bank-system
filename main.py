#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

' Baiyunu bank system '

__author__ = 'NgaiYeancoi','canyie'

import tkinter as tk
## GUI的部分
root= tk.Tk() #建立Tkinter视窗
root.title('Baiyunu Bank System') #设置窗口标题
root.iconbitmap('./images/favicon.ico') #设置窗口icon
window_width = root.winfo_screenwidth() #取得屏幕宽度
window_height = root.winfo_screenheight() #取得屏幕高度
width = 1000 #宽
height = 600 #高
left = int((window_width-width)/2) #计算左坐标
top = int((window_height-height)/2) #计算上坐标 以保证在中间显示
root.geometry(f'{width}x{height}+{left}+{top}')  #定义视窗大小


root.mainloop()  # 进入消息循环

def main():
    pass
if __name__ == '__main__':
    main()