from random import randint

from ErrorLog import ErrorLog

from pymongo import MongoClient, errors

HOST = '123.207.85.99'
PORT = '27017'
USERNAME = 'book'
PASSWORD = 'tianjun223.'
DB_NAME = 'book'


class MyDatabase(object):
    def __init__(self, host, port, username, password, db_name):
        self._conn = MongoClient(host=host,
                                 port=port,
                                 username=username,
                                 password=password,
                                 authSource=db_name,
                                 authMechanism='SCRAM-SHA-1')
        self._database = self._conn.get_database(db_name)

    @property
    def database(self):
        return self.database


class BookColl(object):
    def __init__(self, my_database):
        self._error_log = ErrorLog()
        self._db = my_database
        self._books = self._db.book

    def insert_to_db(self, data):
        try:
            self._books.insert_one(data)
        except (errors, Exception) as e:
            self._error_log.write_error('BookColl插入错误' + e)


class UrlColl(object):
    def __init__(self, my_database):
        self._error_log = ErrorLog()
        self._db = my_database
        self._urls = self._db.url

    def add_url(self, url):
        try:
            if not self.is_exist_url(url):
                self._urls.insert_one({'url': url, 'isExist': 'false'})
        except (errors, Exception) as e:
            self._error_log.write_error('UrlColl添加错误' + e)

    def is_exist_url(self, url):
        try:
            result = self._urls.find_one({"url": url})
            if result is None:
                return False
            else:
                return True
        except (errors, Exception) as e:
            self._error_log.write_error('UrlColl查找错误' + e)

    def get_url(self):
        num = randint(1, 100)
        try:
            result = self._urls.find({'isExist': 'false'}).skip(num).limit(1)
            return result[0]['url']
        except (errors, Exception) as e:
            self._error_log.write_error('UrlColl获取url错误' + e)

    def update_url(self, url):
        try:
            self._urls.update({'url': url}, {'$set': {'isExist': 'true'}})
        except (errors, Exception) as e:
            self._error_log.write_error('UrlColl更新URl数据错误' + e)

