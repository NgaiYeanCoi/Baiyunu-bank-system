#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" Baiyun University bank system """
__author__ = 'NgaiYeanCoi', 'canyie'

import re
import time
import tkinter as tk
from typing import Optional
from PIL import Image, ImageTk
from bank import bank, AccountLockedError
from tkinter import messagebox, Toplevel, Button, Label, Entry

# GUI的部分
# 数字键盘按钮数据
keypadButtons = [
    ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
    ('C', 4, 0), ('0', 4, 1), ('←', 4, 2),
    ('.', 5, 0)
]
NoPointKeypadButtons = [
    ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
    ('C', 4, 0), ('0', 4, 1), ('←', 4, 2),
]
def addNoPointicKeypad(window):
    frame = tk.Frame(window)
    frame.pack()
    for (text, row, col) in NoPointKeypadButtons:
        if text == 'C':
            btn = tk.Button(frame, text=text, font=('Helvetica', 16), command=clearEntry)
        elif text == '←':
            btn = tk.Button(frame, text=text, font=('Helvetica', 16), command=backspaceEntry)
        else:
            btn = tk.Button(frame, text=text, font=('Helvetica', 16), command=lambda t=text: insertNumber(t))
        btn.grid(row=row, column=col, ipadx=10, ipady=10, padx=5, pady=5)
# 窗口根布局
root: tk.Tk
# 窗口根画布
canvasRoot: tk.Canvas
# 窗口宽高
windowWidth: int
windowHeight: int
# 当前活跃的Entry控件
activeEntry: Optional[Entry] = None
# 主窗口的开户按钮
createAccountBtn: Button
# 主窗口的登录按钮
signInBtn: Button
# 存款对话框中金额的输入框
depositAmountEntry: Entry

# 必须持有所有 PhotoImage 对象的引用，防止其被销毁
globalImages = {}
# 登录成功后，canvas 需要手动删除的所有 ID（发卡组织图片等）
canvasIdsToDelete = []


def setActiveEntry(entry_widget):
    global activeEntry
    activeEntry = entry_widget


def backspaceEntry():  # 退格方法
    if activeEntry and activeEntry.winfo_exists():
        activeEntry.delete(len(activeEntry.get()) - 1, tk.END)


def insertNumber(number):  # 输入数字方法
    if activeEntry and activeEntry.winfo_exists():
        activeEntry.insert(tk.END, number)


def clearEntry():  # 清空方法
    if activeEntry and activeEntry.winfo_exists():
        activeEntry.delete(0, tk.END)


def bindFocusableWindow(window):
    def onClose():
        window.destroy()
        setActiveEntry(None)

    window.protocol("WM_DELETE_WINDOW", onClose)


def createEntry(window, **args):
    entry = Entry(window, **args)
    entry.pack()
    entry.bind("<FocusIn>", lambda event: setActiveEntry(entry))  # 跟踪当前活跃
    entry.bind("<FocusOut>", lambda event: setActiveEntry(None))
    bindFocusableWindow(root)
    return entry


def createPasswordEntry(window):
    return createEntry(window, show="*")


def addNumericKeypad(window):
    frame = tk.Frame(window)
    frame.pack()
    for (text, row, col) in keypadButtons:
        if text == 'C':
            btn = tk.Button(frame, text=text, font=('Helvetica', 16), command=clearEntry)
        elif text == '←':
            btn = tk.Button(frame, text=text, font=('Helvetica', 16), command=backspaceEntry)
        else:
            btn = tk.Button(frame, text=text, font=('Helvetica', 16), command=lambda t=text: insertNumber(t))
        btn.grid(row=row, column=col, ipadx=10, ipady=10, padx=5, pady=5)


def getImage(file, width, height):
    """
            获取图片方法打开指定图片文件，缩放到指定尺寸
            :return: 返回图片文件
    """
    image = ImageTk.PhotoImage(Image.open(file).resize((width, height)))
    globalImages[file] = image
    return image


def updateTime():  # 时间模块
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    label_time = tk.Label(root, text=currentTime, font=10, fg='#ffffff', bg='#454545')
    label_time.place(x=5, y=570)
    label_time.after(1000, updateTime)


def newWindow(title, width, height):
    window = Toplevel(root)
    window.title(title)
    centerX = int(windowWidth / 2 - width / 2)
    centerY = int(windowHeight / 2 - height / 2)
    window.resizable(width=False, height=False)  # 不允许改变窗口大小
    window.geometry(f"{width}x{height}+{centerX}+{centerY}")
    window.iconbitmap('./images/favicon.ico')  # 设置窗口 icon
    window.grab_set()  # 使窗口模态
    window.focus_set()  # 确保模态窗口获得焦点
    window.transient(root)  # 设置为主窗口的临时窗口
    return window


def mainButton(text, x, y, command, bg='#ffffff',activebackground='#026dbd'):
    btn = tk.Button(root, text=text, width=20, height=5, bd=2, padx=10, bg=bg,
                    activebackground=activebackground, font=('宋体', 15, 'bold'), overrelief='sunken',
                    command=command)
    btn.place(x=x, y=y)
    return btn


def onExit():  # 是否退出询问方框
    if messagebox.askyesno('退出系统', '您真的要退出白云银行管理系统吗？'):
        root.destroy()  # 关闭窗口


def createAccount():  # 开户函数
    def createCheckPasswords():
        userPassword = createAccountEntry1.get()
        if userPassword != createAccountEntry2.get():
            messagebox.showwarning('错误', '你输入的密码不一致')
            createAccount()
        elif not re.match(r"^\d{6}$", userPassword):
            messagebox.showwarning('错误', f'您输入的密码必须是六位整数！')
            createAccount()
        else:
            account = bank.createAccount(userPassword)
            messagebox.showinfo('成功', f'密码输入一致，开户成功，你的银行账号是：{account}\n请务必记住！')
        window.destroy()
        setActiveEntry(None)

    # 点击开户后窗口
    window = newWindow("开户", 300, 450)
    Label(window, text="请输入密码：").pack()
    createAccountEntry1 = createPasswordEntry(window)
    Label(window, text="请再次输入密码：").pack()
    createAccountEntry2 = createPasswordEntry(window)
    bindFocusableWindow(window)
    addNoPointicKeypad(window)
    Button(window, text="确认", width=15, height=2, command=createCheckPasswords).pack()  # 确认按钮


def login(userAccount):
    """
    登入成功后显示的次级页面
    :param userAccount: 账号
    """
    # 建立标题
    canvasRoot.create_text(550, 120, text='请选择业务', font=('宋体', 25, 'bold', 'bold'), fill='white')
    canvasRoot.create_text(550, 150, text='Please select next step', font=('宋体', 20, 'bold', 'italic'), fill='white')

    def goBack():
        if messagebox.askokcancel('登出账户', '是否要登出？'):
            root.destroy()
            mainWindow()

    def changePassword():
        def changePasswordFunc():
            userPasswordOld = changePasswordTopEntryPre.get()
            userPasswordNew = changePasswordTopEntryNew.get()
            userPasswordConfirm = changePasswordTopEntryConfirm.get()
            if not re.match(r"^\d{6}$", userPasswordConfirm):
                messagebox.showwarning('错误', f'您输入的密码必须是六位整数！')
                changePassword()
            elif userPasswordNew != userPasswordConfirm:
                messagebox.showwarning('错误', f'您输入的新密码不一致！')
                changePassword()
            elif userPasswordOld == userPasswordNew:
                messagebox.showwarning('错误', '新密码与旧密码相同')
                changePassword()
            elif bank.verify(userAccount, userPasswordOld):
                bank.resetPassword(userAccount, userPasswordNew)
                messagebox.showinfo('成功', f'您的账户：{userAccount}\n密码修改成功\n请务必记住新的密码！')
            else:
                messagebox.showwarning('错误', '您输入的旧密码错误')
                changePassword()
            window.destroy()
            setActiveEntry(None)

        # 改密码窗口
        window = newWindow("修改密码", 280, 480)
        Label(window, text="请输入旧密码").pack()
        changePasswordTopEntryPre = createPasswordEntry(window)
        Label(window, text="请输入新密码").pack()
        changePasswordTopEntryNew = createPasswordEntry(window)
        Label(window, text="请再次输入新密码").pack()
        changePasswordTopEntryConfirm = createPasswordEntry(window)
        # 数字键盘
        addNoPointicKeypad(window)
        Button(window, text="确认", width=15, height=2, command=changePasswordFunc).pack()  # 确认按钮

    def transfer():
        def onConfirm():
            transferDesAccount = transferEntryDesAccount.get()
            transferAmount = transferEntryAmount.get()
            if userAccount == transferDesAccount:
                messagebox.showerror("错误", "不能自己给自己转账！")
                return
            try:
                bank.transfer(userAccount, transferDesAccount, transferAmount)
                messagebox.showinfo("转账", f"交易成功！\n您当前的余额为：{bank.getBalance(userAccount)}")
            except KeyError:
                messagebox.showerror("错误", "目标账户不存在！")
            except OverflowError:
                messagebox.showerror("错误", "转账金额大于账户余额！")
            except ValueError:
                messagebox.showwarning('错误', f'取款金额不合法请重新输入')
            except AccountLockedError:
                messagebox.showwarning('错误', f'账户已被锁定！')
            window.destroy()
            setActiveEntry(None)

        window = newWindow("转账", 300, 480)
        Label(window, text="目标账号：").pack()
        transferEntryDesAccount = createEntry(window)
        Label(window, text="金额：").pack()
        transferEntryAmount = createEntry(window)
        # 数字键盘
        addNumericKeypad(window)
        Button(window, text="确认", width=16, height=3, command=onConfirm).place(x=120, y=380)  # 确认按钮

    def deposit():  # 存款函数
        def depositFunc():
            # 获取交易前余额
            beforeBalance = bank.getBalance(userAccount)
            userAmount = depositAmountEntry.get()
            try:
                bank.makeDeposit(userAccount, userAmount)
                msg = f'交易成功！账户：{userAccount}\n交易前余额为：{beforeBalance}元\n您当前的余额为：{bank.getBalance(userAccount)}元'
                messagebox.showinfo('存款', msg)
            except ValueError:
                messagebox.showwarning('错误', f'取款金额不合法请重新输入')
            window.destroy()
            setActiveEntry(None)

        # 存款窗口
        window = newWindow("存款", 300, 430)
        Label(window, text="请输入存款金额").pack()
        global depositAmountEntry
        depositAmountEntry = createEntry(window)
        # 数字键盘
        addNumericKeypad(window)
        Button(window, text="确认", width=16, height=3, command=depositFunc).place(x=120, y=335)  # 确认按钮

    def checkBalance():  # 查余额函数
        locked = "已锁定" if bank.getLockState(userAccount) else "未锁定"
        msg = f'您的账户{userAccount}\n余额为：{bank.getBalance(userAccount)}元\n您的用户状态：{locked}'
        messagebox.showinfo('查询余额', msg)

    def withdrawal():  # 取款函数
        def withdrawalFunc():
            beforeBalance = bank.getBalance(userAccount)  # 获取交易前余额
            userAmount = withdrawalEntryAmount.get()
            try:
                bank.withdrawal(userAccount, userAmount)
                balance = bank.getBalance(userAccount)
                messagebox.showinfo('取款', f'交易成功！账户：{userAccount}\n交易前余额为：{beforeBalance}元\n您当前的余额为：{balance}元')
            except AccountLockedError:
                messagebox.showwarning('错误', f'账户{userAccount}\n已被锁定')
            except OverflowError:
                messagebox.showwarning('错误', f'取款金额不得大于账户余额\n账户：{userAccount}\n您的当前余额为{beforeBalance}元')
            except ValueError:
                messagebox.showwarning('错误', f'取款金额不合法请重新输入')
            window.destroy()
            setActiveEntry(None)

        # 取款窗口
        window = newWindow("取款", 300, 430)
        Label(window, text="请输入取款金额").pack()
        withdrawalEntryAmount = createEntry(window)
        # 数字键盘
        addNumericKeypad(window)
        Button(window, text="确认", width=16, height=3, command=withdrawalFunc).place(x=120,y=335)  # 确认按钮

    #建立登入后的按钮
    mainButton("查询余额\nBalance Inquiry", 125, 380, checkBalance)  # 建立查余额按钮
    mainButton("取款\nWithdrawal", 125, 200, withdrawal)  # 建立取款按钮
    mainButton("存款\nDeposit", 415, 200, deposit)  # 建立存款按钮
    mainButton("登出\nLogout", 705, 380, goBack, '#026dbd','#ffffff')  # 建立登出按钮
    mainButton("转账\nTransfer", 705, 200, transfer)  # 建立转账按钮
    mainButton("修改密码\nChange Password", 415, 380, changePassword)  # 建立修改密码


def signIn():
    def signInVerify():
        userPassword = signInEntryPassword.get()
        userAccount = signInEntryAccount.get()
        #login('1') ####前端调试用 不删
        if not re.match(r"^\d{6}$", userPassword):
            messagebox.showwarning('错误', '您的密码不是六位！')
            signIn()
        elif bank.verify(userAccount, userPassword):
            messagebox.showinfo('登入', f'账户：{userAccount}\n登入成功！\n请确保周边环境安全再进行操作！')
            createAccountBtn.destroy()
            signInBtn.destroy()
            canvasRoot.delete(*canvasIdsToDelete)
            canvasIdsToDelete.clear()
            login(userAccount)
        else:
            messagebox.showwarning('错误', '您输入的账号不存在或密码错误！\n请重新输入')
            signIn()
        window.destroy()
        setActiveEntry(None)

    window = newWindow("登入", 300, 460)
    Label(window, text="请输入账号：").pack()
    signInEntryAccount = createEntry(window)
    Label(window, text="请输入密码：").pack()
    signInEntryPassword = createPasswordEntry(window)
    # 数字键盘
    addNumericKeypad(window)
    Button(window, text="登入", width=16, height=3, command=signInVerify).place(x=120,y=380)  # 确认按钮


def mainWindow():  # 主窗口部分
    global root, windowWidth, windowHeight, canvasRoot, createAccountBtn, signInBtn
    root = tk.Tk()  # 建立Tkinter视窗
    windowWidth = root.winfo_screenwidth()  # 取得屏幕宽度
    windowHeight = root.winfo_screenheight()  # 取得屏幕高度
    root.resizable(width=False, height=False)  # 不允许改变窗口大小
    root.title('Baiyun University Bank System')  # 设置窗口标题
    root.iconbitmap('./images/favicon.ico')  # 设置窗口icon
    width = 1100  # 宽
    height = 600  # 高
    centerX = int((windowWidth - width) / 2)  # 计算左坐标
    centerY = int((windowHeight - height) / 2)  # 计算上坐标 以保证在中间显示
    root.geometry(f'{width}x{height}+{centerX}+{centerY}')  # 定义视窗大小
    root.protocol("WM_DELETE_WINDOW", onExit)
    canvasRoot = tk.Canvas(root, width=width, height=height)
    backgroundImg = getImage('./images/bg.png', width=width, height=height)
    canvasRoot.create_image(550, 300, image=backgroundImg)
    canvasRoot.place(x=0, y=0)
    canvasRoot.create_text(550, 580, text='您的财富由我们掌控！', font=('宋体', 15, 'bold', 'italic'), fill='white')
    txtId1 = canvasRoot.create_text(600, 345, text='请插入\n您的卡片\n', font=('黑体', 20, 'bold'), fill='white')
    txtId2 = canvasRoot.create_text(585, 385, text='Insert\nyour card', font=('黑体', 10, 'bold'), fill='white')
    canvasIdsToDelete.append(txtId1)
    canvasIdsToDelete.append(txtId2)
    updateTime()  # 嵌入时间窗口
    createAccountBtn = mainButton("开户注册\nCreate Account", 90, 200, createAccount)  # 建立开户按钮
    signInBtn = mainButton("登入\nSign In", 90, 380, signIn)  # 登录按钮

    def addCardImage(file, x):
        image = getImage(file, 65, 41)
        elementId = canvasRoot.create_image(x, 470, image=image)
        canvasIdsToDelete.append(elementId)

    # 插入白云卡
    baiyunCardImage = getImage('./images/BaiyunBank.png', width=320, height=219)
    canvasIdsToDelete.append(canvasRoot.create_image(850, 300, image=baiyunCardImage))
    # 插入Top图片
    topBarImage = getImage('./images/Top.png', width=1100, height=95)
    canvasRoot.create_image(550, 48, image=topBarImage)
    # 插入银联图片
    addCardImage('./images/UnionPay.png', 730)
    # 插入Visa图片
    addCardImage('./images/Visa.png', 810)
    # 插入万事达图片
    addCardImage('./images/MasterCard.png', 890)
    # 插入JCB图片
    addCardImage('./images/JCB.png', 970)


def main():
    # 主窗口函数
    mainWindow()
    # 进入窗口消息循环
    root.mainloop()


if __name__ == '__main__':
    main()
