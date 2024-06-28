#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

' Baiyun University bank system '
__author__ = 'NgaiYeanCoi', 'canyie'

import tkinter as tk
from tkinter import messagebox,Toplevel,Button,Label,Entry
from PIL import Image, ImageTk
import time,re
from bank import bank, AccountLockedError

#clockImg = None


## GUI的部分
def callback(): #是否退出询问方框
    if messagebox.askyesno('退出系统', '您真的要退出白云银行管理系统吗？'):
        root.destroy() #关闭窗口

def getImage(file,width,height):
    """
            获取图片方法打开指定图片文件，缩放到指定尺寸
            :return: 返回图片文件
            """
    image = Image.open(file).resize((width,height))
    return ImageTk.PhotoImage(image)
def processImageWithTransparency(file, width, height, bg, fg):
    image = Image.open(file).resize((width,height)).convert("RGBA")
    newImage = Image.new("RGBA", image.size, bg + (255,))
    pixels = image.load()  # 读取原图像的像素数据
    newPixels = newImage.load()  # 读取新图像的像素数据
    # 遍历图像的每个像素
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            r, g, b, a = pixels[x, y]
            if a == 0:
                newPixels[x, y] = bg + (255,)
            else:
                newPixels[x, y] = fg + (255,)

    return ImageTk.PhotoImage(newImage)

def updateTime(): #时间模块
    setTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    # time_text = canvasRoot.create_text(160, 570, text='', font=('宋体', 15, 'bold', 'italic'), fill='white')
    # canvasRoot.itemconfig(time_text, text=setTime)  # 更新文本内容
    # canvasRoot.after(1000,updateTime)
    label_time=tk.Label(root,text=setTime,font=(10),fg='#ffffff', bg='#171717')
    label_time.place(x=28,y=570)
    label_time.after(1000,updateTime)
def createAccount():  # 开户函数
    def createCheckPasswords():
        if createAccountEntry1.get() != createAccountEntry2.get():
            messagebox.showwarning('错误', '你输入的密码不一致')
            top.destroy()
            createAccount()
        else:
            userPassword=createAccountEntry1.get()
            if not re.match(r"^\d{6}$", userPassword):
                messagebox.showwarning('错误',f'您输入的密码必须是六位整数！')
                top.destroy()
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
def login(userAccount):
    # 建立标题
    canvasRoot.create_text(550, 120, text='请选择业务', font=('宋体', 25, 'bold', 'bold'), fill='white')
    canvasRoot.create_text(550, 150, text='Please select next step', font=('宋体', 20, 'bold', 'italic'),fill='white')
    def goBack():
        loginExit=messagebox.askokcancel('登出账户','是否要退出？')
        if loginExit== True:
            root.destroy()
            mainWindow()
        else:
            return
    def changePassword():
        def changePasswordError():
            changePasswordTop.destroy()
            changePassword()
        def changePasswordFunc():
            userPasswordOld = changePasswordTopEntryPre.get()
            userPasswordNew = changePasswordTopEntryNew.get()
            userPasswordConfirm = changePasswordTopEntryConfirm.get()
            if not re.match(r"^\d{6}$", userPasswordConfirm):
                messagebox.showwarning('错误', f'您输入的密码必须是六位整数！')
                changePasswordError()
            elif userPasswordNew != userPasswordConfirm:
                messagebox.showwarning('错误', f'您输入的新密码不一致！')
                changePasswordError()
            elif userPasswordOld == userPasswordNew:
                messagebox.showwarning('错误', '新密码与旧密码相同')
                changePasswordError()
            elif bank.verify(userAccount, userPasswordOld):
                bank.resetPassword(userAccount, userPasswordNew)
                messagebox.showinfo('成功', f'您的账户：{userAccount}\n密码修改成功\n请务必记住新的密码记住！')
                # userPasswordConfirm=changePasswordTopEntryNew.get()
                changePasswordTop.destroy()  # 密码一致时关闭弹出窗口
            else:
                messagebox.showwarning('错误', '您输入的旧密码错误')
                changePasswordError()


        def changePasswordClear():
            changePasswordTopEntryPre.delete(0, 'end')
            changePasswordTopEntryNew.delete(0, 'end')
            changePasswordTopEntryConfirm.delete(0,'end')
        # 改密码窗口
        changePasswordTop = Toplevel(root)
        changePasswordTop.title("修改密码")
        width = 250
        height = 200
        centerX = int(window_width / 2 - width / 2)
        centerY = int(window_height / 2 - height / 2)
        changePasswordTop.resizable(width=False, height=False)  # 不允许改变窗口大小
        changePasswordTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
        changePasswordTopLabel1 = Label(changePasswordTop, text="请输入旧密码")
        changePasswordTopLabel1.pack()
        changePasswordTopEntryPre = Entry(changePasswordTop,show='*') #旧密码表单
        changePasswordTopEntryPre.pack()
        changePasswordTopLabel2 = Label(changePasswordTop, text="请输入新密码")
        changePasswordTopLabel2.pack()
        changePasswordTopEntryNew = Entry(changePasswordTop,show='*') #新密码表单
        changePasswordTopEntryNew.pack()
        changePasswordTopLabel3 = Label(changePasswordTop, text="请再次输入新密码")
        changePasswordTopLabel3.pack()
        changePasswordTopEntryConfirm = Entry(changePasswordTop,show='*') #确认密码表单
        changePasswordTopEntryConfirm.pack()
        confirm_button = Button(changePasswordTop, text="确认", width=5,command=changePasswordFunc)  # 确认按钮
        confirm_button.place(x=60, y=150)
        delete_button = Button(changePasswordTop, text="重置", width=5,command=changePasswordClear)  # 清除按钮
        delete_button.place(x=145, y=150)
    def transfer():
        def onConfirm():
            transferDesAccount=transferEntryDesAccount.get()
            transferAmount=transferEntryAmount.get()
            if userAccount == transferDesAccount:
                messagebox.showerror("错误", "不能自己给自己转账！")
                return
            try:
                bank.transfer(userAccount,transferDesAccount,transferAmount)
                messagebox.showinfo("转账",f"交易成功！\n您当前的余额为：{bank.getBalance(userAccount)}")
            except KeyError:
                messagebox.showerror("错误","目标账户不存在！")
                transferTop.destroy()
            except OverflowError:
                messagebox.showerror("错误","转账金额大于账户余额！")
                transferTop.destroy()
            except ValueError:
                messagebox.showwarning('错误', f'取款金额不合法请重新输入')
                transferTop.destroy()
            except AccountLockedError:
                messagebox.showwarning('错误', f'账户已被锁定！')
                transferTop.destroy()
        transferTop = Toplevel(root)
        transferTop.title("转账")
        width = 300
        height = 150
        centerX = int(window_width / 2 - width / 2)
        centerY = int(window_height / 2 - height / 2)
        transferTop.resizable(width=False, height=False)  # 不允许改变窗口大小
        transferTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
        transferLabel = Label(transferTop, text="目标账号：").pack()
        transferEntryDesAccount = Entry(transferTop)
        transferEntryDesAccount.pack()
        transferLabel2 = Label(transferTop, text="金额：").pack()
        transferEntryAmount = Entry(transferTop)
        transferEntryAmount.pack()
        confirm_button = Button(transferTop, text="确认", width=15, command=onConfirm)  # 确认按钮
        confirm_button.place(x=90, y=100)
    def deposit(): # 存款函数
        def depositFunc():
            # 获取交易前余额
            beforeBalance = bank.getBalance(userAccount)
            userAmount = depositTopEntryAmount.get()
            try:
                bank.makeDeposit(userAccount,userAmount)
                messagebox.showinfo('存款',f'交易成功！账户：{userAccount}\n交易前余额为：{beforeBalance}元\n您当前的余额为：{bank.getBalance(userAccount)}元')
                depositTop.destroy()
            except ValueError:
                messagebox.showwarning('错误', f'取款金额不合法请重新输入')
                depositTop.destroy()
        # 存款窗口
        depositTop = Toplevel(root)
        depositTop.title("存款")
        width = 250
        height = 100
        centerX = int(window_width / 2 - width / 2)
        centerY = int(window_height / 2 - height / 2)
        depositTop.resizable(width=False, height=False)  # 不允许改变窗口大小
        depositTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
        depositTopLabel1 = Label(depositTop, text="请输入存款金额")
        depositTopLabel1.pack()
        depositTopEntryAmount = Entry(depositTop)
        depositTopEntryAmount.pack()
        confirm_button = Button(depositTop, text="确认", width=15, command=depositFunc)  # 确认按钮
        confirm_button.place(x=68, y=58)
    def checkBalance():  # 查余额函数
        messagebox.showinfo('查询余额',f'您的账户{userAccount}'
                                          f'\n余额为：{bank.getBalance(userAccount)}元'
                                          f'\n您的用户状态：{"已锁定" if bank.getLockState(userAccount) else "未锁定"}')
    def withdrawal(): # 取款函数
        def withdrawalFunc():
            beforeBalance = bank.getBalance(userAccount) # 获取交易前余额
            userAmount=withdrawalEntryAmount.get()
            try:
                bank.withdrawal(userAccount,userAmount)
                messagebox.showinfo('取款', f'交易成功！账户：{userAccount}\n交易前余额为：{beforeBalance}元\n您当前的余额为：{bank.getBalance(userAccount)}元')
                withdrawalTop.destroy()
            except AccountLockedError:
                messagebox.showwarning('错误',f'账户{userAccount}\n已被锁定')
                withdrawalTop.destroy()
            except OverflowError:
                messagebox.showwarning('错误', f'取款金额不得大于账户余额\n账户：{userAccount}\n您的当前余额为{bank.getBalance(userAccount)}元')
                withdrawalTop.destroy()
            except ValueError:
                messagebox.showwarning('错误', f'取款金额不合法请重新输入')
                withdrawalTop.destroy()
        #取款窗口
        withdrawalTop = Toplevel(root)
        withdrawalTop.title("取款")
        width = 250
        height = 100
        centerX = int(window_width / 2 - width / 2)
        centerY = int(window_height / 2 - height / 2)
        withdrawalTop.resizable(width=False, height=False)  # 不允许改变窗口大小
        withdrawalTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
        withdrawalLabel1 = Label(withdrawalTop, text="请输入取款金额")
        withdrawalLabel1.pack()
        withdrawalEntryAmount = Entry(withdrawalTop)
        withdrawalEntryAmount.pack()
        confirm_button = Button(withdrawalTop, text="确认", width=15, command=withdrawalFunc)  # 确认按钮
        confirm_button.place(x=68, y=58)
    # 建立查余额按钮
    global checkBalanceBtn
    checkBalanceBtn = tk.Button(root,
                                 text="查询余额\nBalance inquiry",
                                 width=20,
                                 height=5,
                                 bd=2, padx=10,
                                 bg='#ffffff', activebackground='#026dbd',
                                 font=('宋体', 15, 'bold'),
                                 overrelief='sunken',
                                 command=checkBalance)
    checkBalanceBtn.place(x=100, y=380)  # 查询余额按钮加入视窗
    # 建立取款按钮
    global withdrawalBtn
    withdrawalBtn = tk.Button(root,
                               text="取款\nWithdrawal",
                               width=20,
                               height=5,
                               bd=2, padx=10,
                               bg='#ffffff', activebackground='#026dbd',
                               font=('宋体', 15, 'bold'),
                               overrelief='sunken',
                               command=withdrawal)
    withdrawalBtn.place(x=100, y=200)  # 取款按钮加入视窗
    # 建立存款按钮
    global depositBtn
    depositBtn = tk.Button(root,
                              text="存款\nDeposit",
                              width=20,
                              height=5,
                              bd=2, padx=10,
                              bg='#ffffff', activebackground='#026dbd',
                              font=('宋体', 15, 'bold'),
                              overrelief='sunken',
                              command=deposit)
    depositBtn.place(x=390, y=200)  # 存款按钮加入视窗
    # 建立退出按钮
    global goBackBtn
    goBackBtn = tk.Button(root,
                           text="登出\nLogout",
                           width=20,
                           height=5,
                           bd=2, padx=10,
                           bg='#026dbd', activebackground='#ffffff',
                           font=('宋体', 15, 'bold'),
                           overrelief='sunken',
                           command=goBack)
    goBackBtn.place(x=680, y=380)  # 退出按钮加视窗
    # 建立转账按钮
    global transferBtn
    transferBtn = tk.Button(root,
                           text="转账\nTransfer",
                           width=20,
                           height=5,
                           bd=2, padx=10,
                           bg='#ffffff', activebackground='#026dbd',
                           font=('宋体', 15, 'bold'),
                           overrelief='sunken',
                           command=transfer)
    transferBtn.place(x=680, y=200)  # 转账按钮加入视窗
    # 建立修改密码
    global changePasswordBtn
    transferBtn = tk.Button(root,
                            text="修改密码\nChange Password",
                            width=20,
                            height=5,
                            bd=2, padx=10,
                            bg='#ffffff', activebackground='#026dbd',
                            font=('宋体', 15, 'bold'),
                            overrelief='sunken',
                            command=changePassword)
    transferBtn.place(x=390, y=380)  # 转账按钮加入视窗


def signIn():
    def signInVerify():
        userPassword=signInEntryPassword.get()
        userAccount=signInEntryAccount.get()
        #login(userAccount)##########调试用
        if not re.match(r"^\d{6}$", userPassword):
            messagebox.showwarning('错误', '您的密码不足六位！')
            signIn()
        elif bank.verify(userAccount, userPassword):
            messagebox.showinfo('登入', f'账户：{userAccount}\n登入成功！\n请确保周边环境安全再进行操作！')
            signInTop.destroy()
            createAccountBtn.destroy()
            signInBtn.destroy()
            canvasRoot.delete(UnionPay_id)
            canvasRoot.delete(Visa_id)
            canvasRoot.delete(JCB_id)
            login(userAccount)
        else:
            messagebox.showwarning('错误', '您输入的账号不存在或密码错误！\n请重新输入')
            signIn()
    signInTop = Toplevel(root)
    signInTop.title("登入")
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
    confirm_button = Button(signInTop, text="登入",width=15, command=signInVerify) #确认按钮
    confirm_button.place(x=90, y=100)
def mainWindow(): # 主窗口部分
    global root
    root = tk.Tk()  # 建立Tkinter视窗
    root.resizable(width=False, height=False) #不允许改变窗口大小
    root.title('Baiyun University Bank System')  # 设置窗口标题
    root.iconbitmap('./images/favicon.ico')  # 设置窗口icon
    global window_width,window_height
    window_width = root.winfo_screenwidth()  # 取得屏幕宽度
    window_height = root.winfo_screenheight()  # 取得屏幕高度
    width = 1100  # 宽
    height = 600  # 高
    centerX = int((window_width - width) / 2)  # 计算左坐标
    centerY = int((window_height - height) / 2)  # 计算上坐标 以保证在中间显示
    root.geometry(f'{width}x{height}+{centerX}+{centerY}')  # 定义视窗大小
    root.protocol("WM_DELETE_WINDOW", callback)  # 嵌入是否退出窗口函数
    # 背景图片
    global backgroundImg
    global canvasRoot
    canvasRoot = tk.Canvas(root, width=width, height=height)
    backgroundImg = getImage('./images/bg.jpg', width=width, height=height)
    canvasRoot.create_image(550, 300, image=backgroundImg)
    canvasRoot.place(x=0, y=0)
    # 各发行图片
    # canvasBankUnionPay = tk.Canvas(root, width=200, height=200)
    # BankUnionPayImg = getImage('./images/UnionPay.png', width=196, height=125)
    # canvasBankUnionPay.create_image(100, 100, image=BankUnionPayImg)  # 居中显示银联图标
    # canvasBankUnionPay.place(x=0, y=0)
    # 建立标题
    canvasRoot.create_text(550, 50, text='白云学院银行管理系统', font=('宋体', 50, 'bold', 'italic'), fill='white')
    canvasRoot.create_text(550, 580, text='您的财富由我们掌控！', font=('宋体', 15, 'bold', 'italic'), fill='white')
    # 嵌入时间窗口
    updateTime()
    # 建立开户按钮
    global createAccountBtn
    createAccountBtn = tk.Button(root,
                                 text="开户注册\nCreate Account",
                                 width=20,
                                 height=5,
                                 bd=2, padx=10,
                                 bg='#ffffff',activebackground='#026dbd',
                                 font=('宋体',15, 'bold'),
                                 overrelief='sunken',
                                 command=createAccount)
    createAccountBtn.place(x=90, y=200)  # 开户按钮加入视窗
    # 时间图标---暂时弃用
    global clockImg
    clockImg=processImageWithTransparency('./images/clock-solid.png', 24, 24, (0, 0, 0), (255, 255, 255))
    labelClock = Label(root, image=clockImg)
    labelClock.place(x=0, y=568)
    global UnionPayImg,UnionPay_id,MasterCardImg,MasterCard_id,JCBImg,JCB_id,VisaImg,Visa_id
    # 插入银联图片
    UnionPayImg = getImage('./images/UnionPay.png',width=65, height=41)
    UnionPay_id=canvasRoot.create_image(730, 470,image=UnionPayImg)
    # 插入Visa图片
    VisaImg = getImage('./images/Visa.png', width=65, height=41)
    Visa_id = canvasRoot.create_image(810, 470, image=VisaImg)
    # 插入万事达图片
    MasterCardImg = getImage('./images/MasterCard.png', width=65, height=41)
    MasterCard_id = canvasRoot.create_image(890, 470, image=MasterCardImg)
    # 插入JCB图片
    JCBImg = getImage('./images/JCB.png', width=65, height=41)
    JCB_id = canvasRoot.create_image(970, 470, image=JCBImg)
    # 登录按钮
    global signInBtn
    signInBtn = tk.Button(root,
                       text="登入\nSign In",
                       width=20,
                          height=5,
                          bd=2,
                          padx=10,
                          bg='#ffffff',
                          activebackground='#026dbd',
                          font=('宋体',15, 'bold'),
                          overrelief='sunken',
                          command=signIn)
    signInBtn.place(x=90, y=380)
def main():
    #主窗口函数
    mainWindow()
    # 进入窗口消息循环
    root.mainloop()

if __name__ == '__main__':
    main()