#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

' Baiyunu bank system '
__author__ = 'NgaiYeancoi','canyie'

import tkinter as tk
from tkinter import messagebox,Toplevel,Button,Label,Entry
from PIL import Image, ImageTk
import time,re
from bank import Bank

bank=Bank()

## GUI的部分
def callback(): #是否退出询问方框
    windowExit=messagebox.askyesno('BaiyunUniversity bank system','是否要退出？')
    if windowExit ==True:
        root.destroy() #关闭窗口
    else:
        return
def updateTime(): #时间模块
    setTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    label_time=tk.Label(root,text=setTime,font=(10))
    label_time.place(x=28,y=570)
    label_time.after(1000,updateTime)
def createAccount():  # 开户函数
    def createCheckPasswords():
        if createAccountEntry1.get() != createAccountEntry2.get():
            messagebox.showwarning('错误', '你输入的密码不一致')
            createAccount()
        else:
            userPassword=createAccountEntry1.get()
            if not re.match(r"^\d{6}$", userPassword):
                messagebox.showwarning('错误',f'{userPassword}必须是六位整数！')
                createAccount()
            else:
                messagebox.showinfo('成功', '密码输入一致，开户成功')
                top.destroy()  # 密码一致时关闭弹出窗口
    def createClear():
        createAccountEntry1.delete(0,'end')
        createAccountEntry2.delete(0, 'end')
    #点击开户后窗口
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
    top.resizable(width=False, height=False) #不允许改变窗口大小
    # 设置窗口的位置和大小
    top.geometry(f"{width}x{height}+{centerX}+{centerY}")
    createAccountLabel1 = Label(top, text="请输入密码：").pack()
    createAccountEntry1 = Entry(top, show="*")
    createAccountEntry1.pack()
    createAccountLabel2 = Label(top, text="请再次输入密码：").pack()
    createAccountEntry2 = Entry(top, show="*")
    createAccountEntry2.pack()
    confirm_button = Button(top, text="确认", command=createCheckPasswords) #确认按钮
    confirm_button.place(x=100, y=100)
    delete_button = Button(top, text="重置", command=createClear) #清除按钮
    delete_button.place(x=150, y=100)

def mainWindow():
    global root
    # 主窗口部分
    root = tk.Tk()  # 建立Tkinter视窗
    root.resizable(width=False, height=False) #不允许改变窗口大小
    root.title('BaiyunUniversity Bank System')  # 设置窗口标题
    root.iconbitmap('./images/favicon.ico')  # 设置窗口icon
    window_width = root.winfo_screenwidth()  # 取得屏幕宽度
    window_height = root.winfo_screenheight()  # 取得屏幕高度
    width = 1100  # 宽
    height = 600  # 高
    left = int((window_width - width) / 2)  # 计算左坐标
    top = int((window_height - height) / 2)  # 计算上坐标 以保证在中间显示
    root.geometry(f'{width}x{height}+{left}+{top}')  # 定义视窗大小
    root.protocol("WM_DELETE_WINDOW", callback)  # 嵌入是否退出窗口函数
    label_top = tk.Label(root, text='白云学院银行管理系统', font=('宋体', 50, 'bold', 'italic'))  # 建立标题标签
    label_top.pack(side='top')  # 标题定位到顶部
    updateTime() # 嵌入时间窗口
    createAccountBtn = tk.Button(root,  # 建立开户按钮
                                 text="开户注册\nCreate Account",
                                 width=20,
                                 height=5,
                                 bd=2, padx=10,
                                 command=createAccount)
    createAccountBtn.place(x=20, y=200)  # 开户按钮加入视窗


def main():
    #主窗口函数
    mainWindow()
    #时间图标 图片必须要放主函数否则就会出问题
    img1 = Image.open('./images/clock-solid.png')
    img1 = img1.resize((24, 24))
    clockImg = ImageTk.PhotoImage(img1)
    labelClock = Label(root, image=clockImg)
    labelClock.place(x=0, y=568)
    # 进入窗口消息循环
    root.mainloop()

if __name__ == '__main__':
    main()
