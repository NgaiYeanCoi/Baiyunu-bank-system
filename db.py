import os


class Database:
    """
    数据存储模块，使用 csv 格式进行存储
    格式：key,value1,value2,value3...
    """
    def __init__(self, filename):
        """
        创建对象并加载 filename 对应的文件的数据
        :param filename: 文件名/路径
        """
        self.__filename = filename
        self.__table = {}
        if not os.path.exists(filename):
            return
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.read().split('\n')
            for line in lines:
                if line.find(',') == -1:
                    continue
                split = line.split(",")
                self.readItem(split)

    def readItem(self, split):
        self.__table[split[0]] = split[1:len(split)]

    def get(self, key):
        """根据 key 获取对应的 list"""
        return self.__table.get(key)

    def keys(self):
        """获取当前所有的 key"""
        return self.__table.keys()

    def set(self, key, item):
        """插入或修改 key 对应的数据，并同步到文件"""
        self.setInMemory(key, item)
        self.save()

    def setInMemory(self, key, item):
        """插入或修改 key 对应的数据，但不同步到文件"""
        self.__table[key] = item

    def save(self):
        """将内存中的数据同步到磁盘文件"""
        with open(self.__filename, "w", encoding="utf-8") as f:
            for key, value in self.__table.items():
                self.writeItem(f, key, value)

    def writeItem(self, f, key, value):
        f.write(str(key))
        for item in value:
            f.write(",")
            f.write(str(item))
        f.write('\n')


class ListDatabase:
    """
    数据存储模块，使用 csv 格式进行存储
    格式：key,value1,value2,value3...
    """
    def __init__(self, filename):
        """
        创建对象并加载 filename 对应的文件的数据
        :param filename: 文件名/路径
        """
        self.__filename = filename
        self.__table = []
        if not os.path.exists(filename):
            return
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.read().split('\n')
            for line in lines:
                if line.find(',') == -1:
                    continue
                self.__table.append(line.split(","))

    def items(self):
        """获取所有项"""
        return self.__table

    def insert(self, item):
        """插入新项"""
        self.__table.append(item)
        self.save()

    def save(self):
        """将内存中的数据同步到磁盘文件"""
        with open(self.__filename, "w", encoding="utf-8") as f:
            for items in self.__table:
                isFirst = True
                for item in items:
                    if isFirst:
                        isFirst = False
                    else:
                        f.write(',')
                    f.write(str(item))
                f.write('\n')
