#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

' Baiyunu bank system '
__author__ = 'NgaiYeancoi','canyie'

import tkinter as tk
from tkinter import messagebox,Toplevel,Button,Label,Entry
from PIL import Image, ImageTk
import time,re
from bank import Bank

bank = Bank()
clockImg = None

## GUI的部分
def callback(): #是否退出询问方框
    windowExit=messagebox.askyesno('BaiyunUniversity bank system','是否要退出？')
    if windowExit ==True:
        root.destroy() #关闭窗口
    else:
        return
def getImage(file,width,height):
    """
            获取图片方法打开指定图片文件，缩放到指定尺寸
            :return: 返回图片文件
            """
    image = Image.open(file).resize((width,height))
    return ImageTk.PhotoImage(image)
def updateTime(): #时间模块
    setTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    time_text = canvasRoot.create_text(160, 570, text='', font=('宋体', 15, 'bold', 'italic'), fill='white')
    canvasRoot.itemconfig(time_text, text=setTime)  # 更新文本内容
    canvasRoot.after(1000,updateTime)
    # label_time=tk.Label(root,text=setTime,font=(10),fg='#ffffff')
    # label_time.place(x=28,y=570)
    # label_time.after(1000,updateTime)
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
                account = bank.createAccount(userPassword)
                messagebox.showinfo('成功', f'密码输入一致，开户成功，你的银行账号是：{account}\n请务必记住！')
                top.destroy()  # 密码一致时关闭弹出窗口
    def createClear():
        createAccountEntry1.delete(0,'end')
        createAccountEntry2.delete(0, 'end')
    #点击开户后窗口
    top=Toplevel(root)
    top.title('开户')
    # 计算窗口的宽度和高度
    width = 300
    height = 150
    # 计算窗口在屏幕上的位置
    centerX = int(window_width / 2 - width / 2)
    centerY = int(window_height / 2 - height / 2)
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

def signIn():
    def signInVerify():
        userPassword=signInEntryPassword.get()
        userAccount=signInEntryAccount.get()
        if not re.match(r"^\d{6}$", userPassword):
            messagebox.showwarning('错误', '您的密码不足六位！')
            signIn()
        elif bank.verify(userAccount, userPassword)==False:
            messagebox.showwarning('错误', '您输入的账号不存在或密码错误！\n请重新输入')
            signIn()
        elif bank.verify(userAccount, userPassword)==True:
            messagebox.showwarning('登入', f'{userAccount}用户登入成功！')

        pass
    signInTop = Toplevel(root)
    signInTop.title("登录")
    width = 300
    height = 150
    centerX = int(window_width / 2 - width / 2)
    centerY = int(window_height / 2 - height / 2)
    signInTop.resizable(width=False, height=False)  # 不允许改变窗口大小
    signInTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
    signInLabel1 = Label(signInTop,text="请输入账号：").pack()
    signInEntryAccount = Entry(signInTop)
    signInEntryAccount.pack()
    signInLabel2 = Label(signInTop, text="请输入密码：").pack()
    signInEntryPassword=Entry(signInTop,show='*')
    signInEntryPassword.pack()
    confirm_button = Button(signInTop, text="登录",width=15, command=signInVerify) #确认按钮
    confirm_button.place(x=90, y=100)


def mainWindow():
    global root
    # 主窗口部分
    root = tk.Tk()  # 建立Tkinter视窗
    root.resizable(width=False, height=False) #不允许改变窗口大小
    root.title('BaiyunUniversity Bank System')  # 设置窗口标题
    root.iconbitmap('./images/favicon.ico')  # 设置窗口icon
    global window_width,window_height
    window_width = root.winfo_screenwidth()  # 取得屏幕宽度
    window_height = root.winfo_screenheight()  # 取得屏幕高度
    width = 1100  # 宽
    height = 600  # 高
    left = int((window_width - width) / 2)  # 计算左坐标
    top = int((window_height - height) / 2)  # 计算上坐标 以保证在中间显示
    root.geometry(f'{width}x{height}+{left}+{top}')  # 定义视窗大小
    root.protocol("WM_DELETE_WINDOW", callback)  # 嵌入是否退出窗口函数
    # 背景图片
    global backgroundImg
    global canvasRoot
    canvasRoot = tk.Canvas(root, width=width, height=height)
    backgroundImg = getImage('./images/bg.jpg', width=width, height=height)
    canvasRoot.create_image(550, 300, image=backgroundImg)
    canvasRoot.place(x=0, y=0)
    # 建立标题
    canvasRoot.create_text(550, 50, text='白云学院银行管理系统', font=('宋体', 50, 'bold', 'italic'), fill='white')
    # 嵌入时间窗口
    updateTime()
    # 建立开户按钮
    createAccountBtn = tk.Button(root,
                                 text="开户注册\nCreate Account",
                                 width=20,
                                 height=5,
                                 bd=2, padx=10,
                                 bg='#ffffff',activebackground='#026dbd',font=('宋体',15, 'bold'),
                                 command=createAccount)
    createAccountBtn.place(x=90, y=200)  # 开户按钮加入视窗
    # 时间图标---暂时弃用
    # global clockImg
    # clockImg=getImage('./images/clock-solid.png', 24, 24)
    # labelClock = Label(root, image=clockImg)
    # labelClock.place(x=0, y=568)
    # 登录按钮
    signInBtn = tk.Button(root,
                       text="登录\nSign In",
                       width=20, height=5,bd=2,
                        padx=10,bg='#ffffff',activebackground='#026dbd',font=('宋体',15, 'bold'),
                          command=signIn)
    signInBtn.place(x=90, y=380)



def main():
    #主窗口函数
    mainWindow()
    # 进入窗口消息循环
    root.mainloop()

if __name__ == '__main__':
    main()
