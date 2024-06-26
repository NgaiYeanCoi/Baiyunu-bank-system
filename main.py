#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

' Baiyunu bank system '

__author__ = 'NgaiYeancoi','canyie'

import tkinter as tk
from tkinter import messagebox,Toplevel,Button,Label,Entry
import time

## GUI的部分
def callback(): #是否退出询问方框
    windowExit=messagebox.askyesno('BaiyunUniversity bank system','是否要退出？')
    if windowExit ==True:
        root.destroy() #关闭窗口
    else:
        return
def updateTime(): #时间
    setTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    label_time=tk.Label(root,text=setTime,font=(10))
    label_time.place(x=800,y=570)
    label_time.after(1000,updateTime)




def createAccount():  # 开户函数
    def createCheckPasswords():
        if createAccountEntry1.get() != createAccountEntry2.get():
            messagebox.showwarning('错误', '你输入的密码不一致')
        else:
            messagebox.showinfo('成功', '密码输入一致，开户成功')
            top.destroy()  # 密码一致时关闭弹出窗口
    global top
    top=Toplevel(root)
    top.title('开户')
    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # 计算窗口的宽度和高度
    width = 300
    height = 150
    # 计算窗口在屏幕上的位置
    centerX = int(screen_width / 2 - width / 2)
    centerY = int(screen_height / 2 - height / 2)
    # 设置窗口的位置和大小
    top.geometry(f"{width}x{height}+{centerX}+{centerY}")
    createAccountLabel1 = Label(top, text="请输入密码：").pack()
    createAccountEntry1 = Entry(top, show="*")
    createAccountEntry1.pack()
    createAccountLabel2 = Label(top, text="请再次输入密码：").pack()
    createAccountEntry2 = Entry(top, show="*")
    createAccountEntry2.pack()
    confirm_button = Button(top, text="确认", command=createCheckPasswords)
    confirm_button.pack(side='bottom')




def mainWindow():
    global root
    # 主窗口部分
    root = tk.Tk()  # 建立Tkinter视窗
    root.resizable(width=False, height=False)
    root.title('BaiyunUniversity Bank System')  # 设置窗口标题
    root.iconbitmap('./images/favicon.ico')  # 设置窗口icon
    window_width = root.winfo_screenwidth()  # 取得屏幕宽度
    window_height = root.winfo_screenheight()  # 取得屏幕高度
    width = 1000  # 宽
    height = 600  # 高
    left = int((window_width - width) / 2)  # 计算左坐标
    top = int((window_height - height) / 2)  # 计算上坐标 以保证在中间显示
    root.geometry(f'{width}x{height}+{left}+{top}')  # 定义视窗大小
    root.protocol("WM_DELETE_WINDOW", callback)  # 嵌入是否退出窗口函数
    label_top = tk.Label(root, text='白云学院银行管理系统', font=('宋体', 50, 'bold', 'italic'))  # 建立标题标签
    label_top.pack(side='top')  # 标题定位到顶部
    updateTime()  # 嵌入时间窗口
    createAccountBtn = tk.Button(root,  # 建立开户按钮
                                 text="开户",
                                 width=20,
                                 height=5,
                                 bd=2, padx=10,
                                 command=createAccount)
    createAccountBtn.place(x=20, y=200)  # 开户按钮加入视窗


def main():
    mainWindow()
    root.mainloop()  # 进入窗口消息循环

if __name__ == '__main__':
    main()
