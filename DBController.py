import random

from pymongo import MongoClient


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
        self.books.insert_one(data)
        self.urls.update({"url": data["url"]}, {'$set': {"isExist": "true"}})

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
        return result[0]["url"]

