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


# 创建数字按钮
keypadButtons = [
    ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
    ('C', 4, 0), ('0', 4, 1), ('←', 4, 2)
]
# 窗口根布局
root: tk.Tk
# 窗口根画布
canvasRoot: tk.Canvas
# 窗口宽高
windowWidth: int
windowHeight: int
# 当前活跃的Entry控件
active_entry: Optional[Entry] = None
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


def set_active_entry(entry_widget):
    global active_entry
    active_entry = entry_widget


def backspace_entry():  # 退格方法
    if active_entry and active_entry.winfo_exists():
        active_entry.delete(len(active_entry.get()) - 1, tk.END)


def insert_number(number):  # 输入数字方法
    if active_entry and active_entry.winfo_exists():
        active_entry.insert(tk.END, number)


def clear_entry():  # 清空方法
    if active_entry and active_entry.winfo_exists():
        active_entry.delete(0, tk.END)


def modalWindows(TopId):  # 使窗口模态
    TopId.grab_set()
    TopId.focus_set()  # 确保模态窗口获得焦点
    TopId.transient(root)  # 设置为主窗口的临时窗口


def bindFocusableWindow(window):
    def onClose():
        window.destroy()
        set_active_entry(None)

    window.protocol("WM_DELETE_WINDOW", onClose)


def createEntry(window, **args):
    entry = Entry(window, **args)
    entry.pack()
    entry.bind("<FocusIn>", lambda event: set_active_entry(entry))  # 跟踪当前活跃
    entry.bind("<FocusOut>", lambda event: set_active_entry(None))
    bindFocusableWindow(root)
    return entry


def createPasswordEntry(window):
    return createEntry(window, show="*")


def addNumericKeypad(window):
    frame = tk.Frame(window)
    frame.pack()
    for (text, row, col) in keypadButtons:
        if text == 'C':
            btn = tk.Button(frame, text=text, font=('Helvetica', 16), command=clear_entry)
        elif text == '←':
            btn = tk.Button(frame, text=text, font=('Helvetica', 16), command=backspace_entry)
        else:
            btn = tk.Button(frame, text=text, font=('Helvetica', 16), command=lambda t=text: insert_number(t))
        btn.grid(row=row, column=col, ipadx=10, ipady=10, padx=5, pady=5)


def onExit():  # 是否退出询问方框
    if messagebox.askyesno('退出系统', '您真的要退出白云银行管理系统吗？'):
        root.destroy()  # 关闭窗口


def getImage(file, width, height):
    """
            获取图片方法打开指定图片文件，缩放到指定尺寸
            :return: 返回图片文件
    """
    image = ImageTk.PhotoImage(Image.open(file).resize((width, height)))
    globalImages[file] = image
    return image


def processImageWithTransparency(file, width, height, bg, fg):
    image = Image.open(file).resize((width, height)).convert("RGBA")
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


def updateTime():  # 时间模块
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # time_text = canvasRoot.create_text(160, 570, text='', font=('宋体', 15, 'bold', 'italic'), fill='white')
    # canvasRoot.itemconfig(time_text, text=setTime)  # 更新文本内容
    # canvasRoot.after(1000,updateTime)
    label_time = tk.Label(root, text=currentTime, font=10, fg='#ffffff', bg='#454545')
    label_time.place(x=5, y=570)
    label_time.after(1000, updateTime)


def button(text, x, y, command, bg='#ffffff'):
    btn = tk.Button(root, text=text, width=20, height=5, bd=2, padx=10, bg=bg,
                    activebackground='#026dbd', font=('宋体', 15, 'bold'), overrelief='sunken',
                    command=command)
    btn.place(x=x, y=y)
    return btn


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
        top.destroy()
        set_active_entry(None)

    # def createClear():
    #     createAccountEntry1.delete(0, 'end')
    #     createAccountEntry2.delete(0, 'end')

    # 点击开户后窗口
    top = Toplevel(root)
    top.title('开户')
    # 计算窗口的宽度和高度
    width = 300
    height = 450
    # 计算窗口在屏幕上的位置
    centerX = int(windowWidth / 2 - width / 2)
    centerY = int(windowHeight / 2 - height / 2)
    top.resizable(width=False, height=False)  # 不允许改变窗口大小
    # 设置窗口的位置和大小
    top.geometry(f"{width}x{height}+{centerX}+{centerY}")
    top.iconbitmap('./images/favicon.ico')  # 设置窗口icon
    Label(top, text="请输入密码：").pack()
    createAccountEntry1 = createPasswordEntry(top)
    Label(top, text="请再次输入密码：").pack()
    createAccountEntry2 = createPasswordEntry(top)
    bindFocusableWindow(top)
    # 数字键盘
    # button_frame = tk.Frame(top)
    # button_frame.pack()
    # for (text, row, col) in buttons:
    #     if text == 'C':
    #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=clear_entry)
    #     elif text == '←':
    #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=backspace_entry)
    #     else:
    #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16),
    #                            command=lambda t=text: insert_number(t))
    #     button.grid(row=row, column=col, ipadx=10, ipady=10, padx=5, pady=5)
    addNumericKeypad(top)
    confirm_button = Button(top, text="确认", width=15, height=2, command=createCheckPasswords)  # 确认按钮
    confirm_button.pack()
    # confirm_button = Button(top, text="确认", command=createCheckPasswords) #确认按钮
    # confirm_button.place(x=100, y=100)
    # delete_button = Button(top, text="重置", command=createClear) #清除按钮
    # delete_button.place(x=150, y=100)
    modalWindows(top)


def login(userAccount):
    # 建立标题
    canvasRoot.create_text(550, 120, text='请选择业务', font=('宋体', 25, 'bold', 'bold'), fill='white')
    canvasRoot.create_text(550, 150, text='Please select next step', font=('宋体', 20, 'bold', 'italic'), fill='white')

    def goBack():
        if messagebox.askokcancel('登出账户', '是否要登出？'):
            root.destroy()
            mainWindow()

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
                messagebox.showinfo('成功', f'您的账户：{userAccount}\n密码修改成功\n请务必记住新的密码！')
                # userPasswordConfirm=changePasswordTopEntryNew.get()
                changePasswordTop.destroy()  # 密码一致时关闭弹出窗口
            else:
                messagebox.showwarning('错误', '您输入的旧密码错误')
                changePasswordError()
            set_active_entry(None)

        # def changePasswordClear():
        #     changePasswordTopEntryPre.delete(0, 'end')
        #     changePasswordTopEntryNew.delete(0, 'end')
        #     changePasswordTopEntryConfirm.delete(0, 'end')

        # 改密码窗口
        changePasswordTop = Toplevel(root)
        changePasswordTop.title("修改密码")
        width = 250
        height = 500
        centerX = int(windowWidth / 2 - width / 2)
        centerY = int(windowHeight / 2 - height / 2)
        changePasswordTop.resizable(width=False, height=False)  # 不允许改变窗口大小
        changePasswordTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
        changePasswordTop.iconbitmap('./images/favicon.ico')  # 设置窗口icon
        changePasswordTopLabel1 = Label(changePasswordTop, text="请输入旧密码")
        changePasswordTopLabel1.pack()
        changePasswordTopEntryPre = createPasswordEntry(changePasswordTop)  # 跟踪当前活跃
        changePasswordTopLabel2 = Label(changePasswordTop, text="请输入新密码")
        changePasswordTopLabel2.pack()
        changePasswordTopEntryNew = createPasswordEntry(changePasswordTop)
        changePasswordTopLabel3 = Label(changePasswordTop, text="请再次输入新密码")
        changePasswordTopLabel3.pack()
        changePasswordTopEntryConfirm = createPasswordEntry(changePasswordTop)
        # 数字键盘
        # button_frame = tk.Frame(changePasswordTop)
        # button_frame.pack()
        # for (text, row, col) in keypadButtons:
        #     if text == 'C':
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=clear_entry)
        #     elif text == '←':
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=backspace_entry)
        #     else:
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16),
        #                            command=lambda t=text: insert_number(t))
        #     button.grid(row=row, column=col, ipadx=10, ipady=10, padx=5, pady=5)
        addNumericKeypad(changePasswordTop)
        confirm_button = Button(changePasswordTop, text="确认", width=15, height=2, command=changePasswordFunc)  # 确认按钮
        confirm_button.pack()
        modalWindows(changePasswordTop)

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
            transferTop.destroy()
            set_active_entry(None)

        transferTop = Toplevel(root)
        transferTop.title("转账")
        width = 300
        height = 450
        centerX = int(windowWidth / 2 - width / 2)
        centerY = int(windowHeight / 2 - height / 2)
        transferTop.resizable(width=False, height=False)  # 不允许改变窗口大小
        transferTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
        transferTop.iconbitmap('./images/favicon.ico')  # 设置窗口icon
        Label(transferTop, text="目标账号：").pack()
        transferEntryDesAccount = createEntry(transferTop)
        Label(transferTop, text="金额：").pack()
        transferEntryAmount = createEntry(transferTop)
        # 数字键盘
        # button_frame = tk.Frame(transferTop)
        # button_frame.pack()
        # for (text, row, col) in keypadButtons:
        #     if text == 'C':
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=clear_entry)
        #     elif text == '←':
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=backspace_entry)
        #     else:
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16),
        #                            command=lambda t=text: insert_number(t))
        #     button.grid(row=row, column=col, ipadx=10, ipady=10, padx=5, pady=5)
        addNumericKeypad(transferTop)
        confirm_button = Button(transferTop, text="确认", width=15, height=2, command=onConfirm)  # 确认按钮
        confirm_button.pack()
        modalWindows(transferTop)

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
            depositTop.destroy()
            set_active_entry(None)

        # 存款窗口
        depositTop = Toplevel(root)
        depositTop.title("存款")
        width = 250
        height = 400
        centerX = int(windowWidth / 2 - width / 2)
        centerY = int(windowHeight / 2 - height / 2)
        depositTop.resizable(width=False, height=False)  # 不允许改变窗口大小
        depositTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
        depositTop.iconbitmap('./images/favicon.ico')  # 设置窗口icon
        depositTopLabel1 = Label(depositTop, text="请输入存款金额")
        depositTopLabel1.pack()
        global depositAmountEntry
        depositAmountEntry = createEntry(depositTop)
        # 数字键盘
        # button_frame = tk.Frame(depositTop)
        # button_frame.pack()
        # for (text, row, col) in keypadButtons:
        #     if text == 'C':
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=clear_entry)
        #     elif text == '←':
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=backspace_entry)
        #     else:
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16),
        #                            command=lambda t=text: insert_number(t))
        #     button.grid(row=row, column=col, ipadx=10, ipady=10, padx=5, pady=5)
        addNumericKeypad(depositTop)
        confirm_button = Button(depositTop, text="确认", width=15, height=2, command=depositFunc)  # 确认按钮
        confirm_button.pack()
        modalWindows(depositTop)

    def checkBalance():  # 查余额函数
        locked = bank.getLockState(userAccount)
        msg = f'您的账户{userAccount}\n余额为：{bank.getBalance(userAccount)}元\n您的用户状态：{"已锁定" if locked else "未锁定"}'
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
            withdrawalTop.destroy()
            set_active_entry(None)

        # 取款窗口
        withdrawalTop = Toplevel(root)
        withdrawalTop.title("取款")
        width = 250
        height = 400
        centerX = int(windowWidth / 2 - width / 2)
        centerY = int(windowHeight / 2 - height / 2)
        withdrawalTop.resizable(width=False, height=False)  # 不允许改变窗口大小
        withdrawalTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
        withdrawalTop.iconbitmap('./images/favicon.ico')  # 设置窗口icon
        withdrawalLabel1 = Label(withdrawalTop, text="请输入取款金额")
        withdrawalLabel1.pack()
        withdrawalEntryAmount = createEntry(withdrawalTop)
        # 数字键盘
        # button_frame = tk.Frame(withdrawalTop)
        # button_frame.pack()
        # for (text, row, col) in keypadButtons:
        #     if text == 'C':
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=clear_entry)
        #     elif text == '←':
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=backspace_entry)
        #     else:
        #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16),
        #                            command=lambda t=text: insert_number(t))
        #     button.grid(row=row, column=col, ipadx=10, ipady=10, padx=5, pady=5)
        addNumericKeypad(withdrawalTop)
        confirm_button = Button(withdrawalTop, text="确认", width=15, height=2, command=withdrawalFunc)  # 确认按钮
        confirm_button.pack()
        modalWindows(withdrawalTop)
        # 数字键盘

    # 建立查余额按钮
    # global checkBalanceBtn
    # checkBalanceBtn = tk.Button(root,
    #                             text="查询余额\nBalance inquiry",
    #                             width=20,
    #                             height=5,
    #                             bd=2, padx=10,
    #                             bg='#ffffff', activebackground='#026dbd',
    #                             font=('宋体', 15, 'bold'),
    #                             overrelief='sunken',
    #                             command=checkBalance)
    # checkBalanceBtn.place(x=100, y=380)  # 查询余额按钮加入视窗
    button("查询余额\nBalance Inquiry", 100, 380, checkBalance)
    # 建立取款按钮
    # global withdrawalBtn
    # withdrawalBtn = tk.Button(root,
    #                           text="取款\nWithdrawal",
    #                           width=20,
    #                           height=5,
    #                           bd=2, padx=10,
    #                           bg='#ffffff', activebackground='#026dbd',
    #                           font=('宋体', 15, 'bold'),
    #                           overrelief='sunken',
    #                           command=withdrawal)
    # withdrawalBtn.place(x=100, y=200)  # 取款按钮加入视窗
    button("取款\nWithdrawal", 100, 200, withdrawal)
    # 建立存款按钮
    # global depositBtn
    # depositBtn = tk.Button(root,
    #                        text="存款\nDeposit",
    #                        width=20,
    #                        height=5,
    #                        bd=2, padx=10,
    #                        bg='#ffffff', activebackground='#026dbd',
    #                        font=('宋体', 15, 'bold'),
    #                        overrelief='sunken',
    #                        command=deposit)
    # depositBtn.place(x=390, y=200)  # 存款按钮加入视窗
    button("存款\nDeposit", 390, 200, deposit)
    # 建立退出按钮
    # global goBackBtn
    # goBackBtn = tk.Button(root,
    #                       text="登出\nLogout",
    #                       width=20,
    #                       height=5,
    #                       bd=2, padx=10,
    #                       bg='#026dbd', activebackground='#ffffff',
    #                       font=('宋体', 15, 'bold'),
    #                       overrelief='sunken',
    #                       command=goBack)
    # goBackBtn.place(x=680, y=380)  # 退出按钮加视窗
    button("登出\nLogout", 680, 380, goBack, '#026dbd')
    # 建立转账按钮
    # global transferBtn
    # transferBtn = tk.Button(root,
    #                         text="转账\nTransfer",
    #                         width=20,
    #                         height=5,
    #                         bd=2, padx=10,
    #                         bg='#ffffff', activebackground='#026dbd',
    #                         font=('宋体', 15, 'bold'),
    #                         overrelief='sunken',
    #                         command=transfer)
    # transferBtn.place(x=680, y=200)  # 转账按钮加入视窗
    button("转账\nTransfer", 680, 200, transfer)
    # 建立修改密码
    # global changePasswordBtn
    # transferBtn = tk.Button(root,
    #                         text="修改密码\nChange Password",
    #                         width=20,
    #                         height=5,
    #                         bd=2, padx=10,
    #                         bg='#ffffff', activebackground='#026dbd',
    #                         font=('宋体', 15, 'bold'),
    #                         overrelief='sunken',
    #                         command=changePassword)
    # transferBtn.place(x=390, y=380)  # 转账按钮加入视窗
    button("修改密码\nChange Password", 390, 380, changePassword)


def signIn():
    def signInVerify():
        userPassword = signInEntryPassword.get()
        userAccount = signInEntryAccount.get()
        # login(userAccount)##########调试用
        if not re.match(r"^\d{6}$", userPassword):
            messagebox.showwarning('错误', '您的密码不足六位！')
            signIn()
        elif bank.verify(userAccount, userPassword):
            messagebox.showinfo('登入', f'账户：{userAccount}\n登入成功！\n请确保周边环境安全再进行操作！')
            createAccountBtn.destroy()
            signInBtn.destroy()
            # canvasRoot.delete(UnionPay_id, Visa_id, JCB_id, BaiyunId, txtId1, txtId2)
            canvasRoot.delete(*canvasIdsToDelete)
            canvasIdsToDelete.clear()
            login(userAccount)
        else:
            messagebox.showwarning('错误', '您输入的账号不存在或密码错误！\n请重新输入')
            signIn()
        signInTop.destroy()
        set_active_entry(None)

    signInTop = Toplevel(root)
    signInTop.title("登入")
    width = 300
    height = 450
    centerX = int(windowWidth / 2 - width / 2)
    centerY = int(windowHeight / 2 - height / 2)
    signInTop.resizable(width=False, height=False)  # 不允许改变窗口大小
    signInTop.geometry(f"{width}x{height}+{centerX}+{centerY}")
    signInTop.iconbitmap('./images/favicon.ico')  # 设置窗口icon
    Label(signInTop, text="请输入账号：").pack()
    signInEntryAccount = createEntry(signInTop)
    Label(signInTop, text="请输入密码：").pack()
    signInEntryPassword = createPasswordEntry(signInTop)
    # 数字键盘
    # button_frame = tk.Frame(signInTop)
    # button_frame.pack()
    # for (text, row, col) in keypadButtons:
    #     if text == 'C':
    #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=clear_entry)
    #     elif text == '←':
    #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16), command=backspace_entry)
    #     else:
    #         button = tk.Button(button_frame, text=text, font=('Helvetica', 16),
    #                            command=lambda t=text: insert_number(t))
    #     button.grid(row=row, column=col, ipadx=10, ipady=10, padx=5, pady=5)
    addNumericKeypad(signInTop)
    confirm_button = Button(signInTop, text="登入", width=15, height=2, command=signInVerify)  # 确认按钮
    confirm_button.pack()
    # 使窗口模态化
    modalWindows(signInTop)


def mainWindow():  # 主窗口部分
    global root
    root = tk.Tk()  # 建立Tkinter视窗
    root.resizable(width=False, height=False)  # 不允许改变窗口大小
    root.title('Baiyun University Bank System')  # 设置窗口标题
    root.iconbitmap('./images/favicon.ico')  # 设置窗口icon
    global windowWidth, windowHeight
    windowWidth = root.winfo_screenwidth()  # 取得屏幕宽度
    windowHeight = root.winfo_screenheight()  # 取得屏幕高度
    width = 1100  # 宽
    height = 600  # 高
    centerX = int((windowWidth - width) / 2)  # 计算左坐标
    centerY = int((windowHeight - height) / 2)  # 计算上坐标 以保证在中间显示
    root.geometry(f'{width}x{height}+{centerX}+{centerY}')  # 定义视窗大小
    root.protocol("WM_DELETE_WINDOW", onExit)  # 嵌入是否退出窗口函数
    # 背景图片
    # global backgroundImg
    global canvasRoot
    canvasRoot = tk.Canvas(root, width=width, height=height)
    backgroundImg = getImage('./images/bg.png', width=width, height=height)
    canvasRoot.create_image(550, 300, image=backgroundImg)
    canvasRoot.place(x=0, y=0)
    # 各发行图片
    # canvasBankUnionPay = tk.Canvas(root, width=200, height=200)
    # BankUnionPayImg = getImage('./images/UnionPay.png', width=196, height=125)
    # canvasBankUnionPay.create_image(100, 100, image=BankUnionPayImg)  # 居中显示银联图标
    # canvasBankUnionPay.place(x=0, y=0)
    # 建立标题
    # canvasRoot.create_text(550, 50, text='白云学院银行管理系统', font=('宋体', 50, 'bold', 'italic'), fill='white')
    canvasRoot.create_text(550, 580, text='您的财富由我们掌控！', font=('宋体', 15, 'bold', 'italic'), fill='white')
    # global txtId1, txtId2
    txtId1 = canvasRoot.create_text(600, 345, text='请插入\n您的卡片\n', font=('黑体', 20, 'bold'), fill='white')
    txtId2 = canvasRoot.create_text(585, 385, text='Insert\nyour card', font=('黑体', 10, 'bold'), fill='white')
    canvasIdsToDelete.append(txtId1)
    canvasIdsToDelete.append(txtId2)
    # 嵌入时间窗口
    updateTime()
    # 建立开户按钮
    global createAccountBtn
    # createAccountBtn = tk.Button(root,
    #                              text="开户注册\nCreate Account",
    #                              width=20,
    #                              height=5,
    #                              bd=2, padx=10,
    #                              bg='#ffffff', activebackground='#026dbd',
    #                              font=('宋体', 15, 'bold'),
    #                              overrelief='sunken',
    #                              command=createAccount)
    # createAccountBtn.place(x=90, y=200)  # 开户按钮加入视窗
    createAccountBtn = button("开户注册\nCreate Account", 90, 200, createAccount)
    # 时间图标---暂时弃用
    # global clockImg
    # clockImg=processImageWithTransparency('./images/clock-solid.png', 24, 24, (0, 0, 0), (255, 255, 255))
    # labelClock = Label(root, image=clockImg)
    # labelClock.place(x=0, y=568)
    # global UnionPayImg, UnionPay_id, MasterCardImg, MasterCard_id, JCBImg, JCB_id, VisaImg, Visa_id, TopBgImg, BaiyunCardImg, BaiyunId

    def addCardImage(file, x):
        image = getImage(file, 65, 41)
        # globalImages[file] = image
        elementId = canvasRoot.create_image(x, 470, image=image)
        canvasIdsToDelete.append(elementId)

    # 插入白云卡
    BaiyunCardImg = getImage('./images/BaiyunBank.png', width=320, height=219)
    BaiyunId = canvasRoot.create_image(850, 300, image=BaiyunCardImg)
    canvasIdsToDelete.append(BaiyunId)
    # 插入Top图片
    TopBgImg = getImage('./images/Top.png', width=1100, height=95)
    canvasRoot.create_image(550, 48, image=TopBgImg)
    # 插入银联图片
    # UnionPayImg = getImage('./images/UnionPay.png', width=65, height=41)
    # UnionPay_id = canvasRoot.create_image(730, 470, image=UnionPayImg)
    addCardImage('./images/UnionPay.png', 730)
    # 插入Visa图片
    # VisaImg = getImage('./images/Visa.png', width=65, height=41)
    # Visa_id = canvasRoot.create_image(810, 470, image=VisaImg)
    addCardImage('./images/Visa.png', 810)
    # 插入万事达图片
    # MasterCardImg = getImage('./images/MasterCard.png', width=65, height=41)
    # MasterCard_id = canvasRoot.create_image(890, 470, image=MasterCardImg)
    addCardImage('./images/MasterCard.png', 890)
    # 插入JCB图片
    # JCBImg = getImage('./images/JCB.png', width=65, height=41)
    addCardImage('./images/JCB.png', 970)
    # JCB_id = canvasRoot.create_image(970, 470, image=JCBImg)
    # 登录按钮
    global signInBtn
    # signInBtn = tk.Button(root,
    #                       text="登入\nSign In",
    #                       width=20,
    #                       height=5,
    #                       bd=2,
    #                       padx=10,
    #                       bg='#ffffff',
    #                       activebackground='#026dbd',
    #                       font=('宋体', 15, 'bold'),
    #                       overrelief='sunken',
    #                       command=signIn)
    # signInBtn.place(x=90, y=380)
    signInBtn = button("登入\nSign In", 90, 380, signIn)


def main():
    # 主窗口函数
    mainWindow()
    # 进入窗口消息循环
    root.mainloop()


if __name__ == '__main__':
    main()
