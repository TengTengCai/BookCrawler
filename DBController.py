import random

from pymongo import *

"""
pymongo 数据库控制文件，控制数据库的基本行为封装

Author:藤藤菜
Version:1.0
Date:2018年2月8日
"""


class Controller(object):
    conn = MongoClient()
    books = None
    urls = None
    db = None

    # 初始化构造方法，对数据库的地址数据库名称进行初始化
    def __init__(self):
        self.conn = MongoClient("123.207.85.99:27017")
        self.db = self.conn.get_database("book")
        self.books = self.db.book
        self.urls = self.db.urls

    # 插入书籍数据，同时，更新URL列表信息
    def insert_to_db(self, data):
        try:
            self.books.insert_one(data)
            self.urls.update({"url": data["url"]}, {'$set': {"isExist": "true"}})
        except ConnectionError as e:
            print("插入数据失败：" + e)

    # 添加URL
    def add_url(self, url):
        result = self.urls.find_one({"url": url})
        # print(result)
        if result is None:
            self.urls.insert_one({"url": url, "isExist": "false"})
            # print(url)

    # 数据库中是否已经存在相同的URL
    def is_exist_url(self, url):
        result = self.urls.find_one({"url": url})
        if result is None:
            return False
        else:
            return True

    # 随机跳跃获取一条URL，防止多个爬虫同时爬取一个页面
    def get_url(self):
        temp = random.randint(1, 100)
        result = self.urls.find({"isExist": "false"}).skip(temp).limit(1)
        # result = self.urls.find_one({"isExist": "false"})
        return result[0]["url"]

    # 将抓取过的URL设置标识
    def delete_url(self, url):
        self.urls.update({"url": url}, {'$set': {"isExist": "true"}})
