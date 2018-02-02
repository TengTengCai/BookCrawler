import random

from pymongo import *


class Controller(object):
    conn = MongoClient()
    books = None
    urls = None
    db = None

    def __init__(self):
        self.conn = MongoClient("123.207.85.99:27017")
        self.db = self.conn.get_database("book")
        self.books = self.db.book
        self.urls = self.db.urls

    def insert_to_db(self, data):
        try:
            self.books.insert_one(data)
            self.urls.update({"url": data["url"]}, {'$set': {"isExist": "true"}})
        except ConnectionError as e:
            print("插入数据失败："+e)

    def add_url(self, url):
        result = self.urls.find_one({"url": url})
        # print(result)
        if result is None:
            self.urls.insert_one({"url": url, "isExist": "false"})
            # print(url)

    def is_exist_url(self, url):
        result = self.urls.find_one({"url": url})
        if result is None:
            return False
        else:
            return True

    def get_url(self):
        temp = random.randint(1, 100)
        result = self.urls.find({"isExist": "false"}).skip(temp).limit(1)
        # result = self.urls.find_one({"isExist": "false"})
        return result[0]["url"]

    def delete_url(self, url):
        self.urls.update({"url": url}, {'$set': {"isExist": "true"}})

