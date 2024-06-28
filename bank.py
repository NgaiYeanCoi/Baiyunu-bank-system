import re
from db import Database
from decimal import Decimal

# 存储格式：
# 账号(数字),密码(六位数字),余额(浮点数，精确到小数点后两位),账号是否锁定(布尔值)


class AccountLockedError(Exception):
    """
    账户已被锁定时尝试进行取款或转账业务，抛出此异常
    """
    def __init__(self, msg):
        super(Exception, self).__init__(msg)


class Account:
    """
    内部描述账户的数据结构类
    """
    def __init__(self, password, balance, locked):
        self.password = password
        self.balance = Decimal(balance)
        self.locked = locked

    @staticmethod
    def create(password):
        """
        通过密码创建新的 Account 对象，默认账户余额为 0 且未被锁定
        :param password: 密码
        :return: Account
        """
        return Account(password, "0", False)

    @staticmethod
    def deserialize(data):
        """
        将磁盘文件里存储的数据转换成 Account 对象
        :param data: 每行数据，列表或元组类型
        :return: Account
        """
        return Account(data[0], data[1], data[2] == 'True')

    def serialize(self):
        """
        将 Account 对象转换成 list，方便存储到到文件上
        :return: list
        """
        return [self.password, self.balance, self.locked]


class Bank:
    """
    模拟银行服务后端接口
    """
    def __init__(self):
        self.__db = Database("data.csv")
        self.__accounts = {}

        # 需要获取当前已分配出去的最大的账号，以免分配账号重复
        self.__currentMaxAccount = 4000000000000000
        for key in self.__db.keys():
            self.__currentMaxAccount = max(self.__currentMaxAccount, int(key))
            self.__accounts[key] = Account.deserialize(self.__db.get(key))

    def createAccount(self, password):
        """
        创建新账号
        :param password: 密码
        :return: 生成的账号
        """
        # if not re.match(r"^\d{6}$", password):
        #     raise ValueError(f"密码 {password} 必须是六位整数！")
        account = Account.create(password)
        self.__currentMaxAccount += 1
        accountNumber = str(self.__currentMaxAccount)
        self.__accounts[accountNumber] = account
        self.__db.set(accountNumber, account.serialize())
        return accountNumber

    def verify(self, accountNumber, password):
        """
        检查账号和密码是否匹配
        :param accountNumber: 账号
        :param password: 密码
        :return: True 如果匹配，False 不匹配或账号不存在
        """
        account = self.__accounts.get(accountNumber)
        return account and account.password == password

    def getBalance(self, account):
        """
        查询账户余额，账户不存在时产生 KeyError
        :param account: 账号
        :return:
        """
        return self.__convertAccount(account).balance

    def getLockState(self, account):
        """
        查询账户锁定状态，账户不存在时产生 KeyError
        :param account: 账号
        :return: 账号被锁定时返回 True，否则 False
        """
        return self.__convertAccount(account).locked

    def makeDeposit(self, accountNumber, amount):
        """
        存款，存款金额不合法时产生 ValueError
        :param accountNumber: 账号
        :param amount: 存款金额
        :return: 存款成功后账号当前余额
        """
        account = self.__convertAccount(accountNumber)
        account.balance += Bank.__convertAmount(amount)
        self.__db.set(accountNumber, account.serialize())
        return account.balance

    def withdrawal(self, accountNumber, amount):
        """
        取款，取款金额不合法或大于账号余额时产生 OverflowError，账号被锁定时产生 AccountLockedError
        :param accountNumber: 账号
        :param amount: 金额
        :return: 账户剩余余额
        """
        account = self.__convertAccount(accountNumber)
        amount = Bank.__convertAmount(amount)
        if account.locked:
            raise AccountLockedError(f"账号 {accountNumber} 已被锁定！")
        if amount > account.balance:
            raise OverflowError(f"取款金额 {amount} 大于当前账户余额 {account.balance}！")
        account.balance -= amount
        self.__db.set(accountNumber, account.serialize())
        return account.balance

    def transfer(self, source, dest, amount):
        """
        转账，目标账号不存在时产生 KeyError，金额不合法或大于源账号余额时产生 OverflowError，源账号被锁定时产生 AccountLockedError
        :param source: 源账户账号
        :param dest: 目标账户账号
        :param amount: 金额
        :return: 账户剩余余额
        """
        srcAccount = self.__convertAccount(source)
        destAccount = self.__convertAccount(dest)
        amount = Bank.__convertAmount(amount)
        if srcAccount.locked:
            raise AccountLockedError(f"账号 {source} 已被锁定！")
        if amount > srcAccount.balance:
            raise OverflowError(f"转账金额 {amount} 大于当前账户余额 {srcAccount.balance}！")
        srcAccount.balance -= amount
        destAccount.balance += amount
        self.__db.setNoSave(source, srcAccount.serialize())
        self.__db.set(dest, destAccount.serialize())
        return srcAccount.balance

    def setLocked(self, accountNumber, locked):
        """
        设置账户锁定状态
        :param accountNumber: 账户账号
        :param locked: 是否锁定，True 锁定，False 解锁
        """
        account = self.__convertAccount(accountNumber)
        account.locked = locked
        self.__db.set(accountNumber, account.serialize())

    def resetPassword(self, accountNumber, newPassword):
        """
        修改账户 密码
        :param accountNumber: 账户账号
        :param newPassword: 新的密码
        """
        account = self.__convertAccount(accountNumber)
        account.password = newPassword
        self.__db.set(accountNumber, account.serialize())

    def __convertAccount(self, accountNumber):
        """
        将数字账号转换成 Account 对象。找不到对应 Account 时抛出 KeyError。
        """
        account = self.__accounts.get(accountNumber)
        if not account:
            raise KeyError(f"账号 {accountNumber} 不存在！")
        return account

    @staticmethod
    def __convertAmount(amount):
        """
        检查金额 amount 的合法性，并返回高精度对象。校验不通过时抛出 ValueError。
        :param amount:
        :return: Decimal
        """
        if not re.match(r"^\d+(\.\d{1,2})?$", amount):
            raise ValueError(f"金额 {amount} 必须是大于 0 的整数或最多两位小数！")
        d = Decimal(amount)
        if d <= 0:
            raise ValueError(f"金额 {amount} 必须是正数！")
        return d


# 全局的 Bank 对象，可直接使用
bank = Bank()
