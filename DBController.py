from random import randint

from ErrorLog import ErrorLog

from pymongo import MongoClient, errors

HOST = '123.207.85.99'
PORT = 27017
USERNAME = 'book'
PASSWORD = 'tianjun223.'
DB_NAME = 'book'


class MyDatabase(object):
    """
    数据库对象
    """
    def __init__(self, host=HOST, port=PORT, username=USERNAME, password=PASSWORD, db_name=DB_NAME):
        """
        初始化数据库对象

        :param host: 数据库主机IP地址
        :param port: 对应端口号
        :param username: 用户名
        :param password: 密码
        :param db_name: 数据库名称或文档名称
        """
        # 连接数据库，获取连接对象
        self._conn = MongoClient(host=host,
                                 port=port,
                                 username=username,
                                 password=password,
                                 authSource=db_name,
                                 authMechanism='SCRAM-SHA-1')
        # 选择数据库
        self._database = self._conn.get_database(db_name)

    @property
    def database(self):
        """
        数据库对象的get方法

        :return:数据库对象
        """
        return self._database

    def close_conn(self):
        self._conn.close()


class BookColl(object):
    """
    书籍集合对象
    """
    def __init__(self, my_database):
        """
        书籍集合对象初始化

        :param my_database:
        """
        self._error_log = ErrorLog()  # 创建错误日志输出对象
        self._db = my_database  # 数据库对象
        self._books = self._db.book  # 获取book集合

    def insert_to_db(self, data):
        """
        插入数据到数据库

        :type data dict
        :param data: 需要插入的字典数据
        :return: None
        """
        try:
            self._books.insert_one(data)  # 插入数据
        except (errors, Exception) as e:
            self._error_log.write_error('BookColl插入错误' + e)  # 错误日志记录

    def get_book_name(self):
        """
        获取书籍名称
        :return:
        """
        # for result in self._books.find({'book_name': {'$regex': '\w'}}):
        for result in self._books.find():
            print(result['book_name'])
            with open('book_name.txt', 'a', encoding='utf-8') as f:
                f.write(result['book_name'] + '\n')


class UrlColl(object):
    """
    URL集合对象
    """
    def __init__(self, my_database):
        """
        URL集合对象

        :param my_database:
        """
        self._error_log = ErrorLog()  # 新建错误日志对象
        self._db = my_database  # 数据库对象
        self._urls = self._db.urls  # URL集合

    def add_url(self, url):
        """
        添加URL数据到集合中

        :param url:  URL数据
        :return: None
        """
        try:
            if not self.is_exist_url(url):  # 判断是否存在
                self._urls.insert_one({'url': url, 'isExist': 'false'})  # 插入
        except (errors, Exception) as e:
            self._error_log.write_error('UrlColl添加错误' + e)  # 错误日志写入

    def is_exist_url(self, url):
        """
        判读是否已经存在相对应的数据

        :param url: URL地址
        :return: boolean 存在返回True不存在返回False
        """
        try:
            result = self._urls.find_one({"url": url})  # 获取查询结果
            if result is None:
                return False  # 返回False
            else:
                return True  # 返回True
        except (errors, Exception) as e:
            self._error_log.write_error('UrlColl查找错误' + e)  # 错误日志写入

    def get_url(self):
        """
        从数据库中随机获取一条数据

        :return: URL地址字符串
        """
        num = randint(1, 100)  # 随机数
        try:
            result = self._urls.find({'isExist': 'false'}).skip(num).limit(1)  # 跳跃式获取数据
            return result[0]['url']  # 返回对应的URL地址
        except (errors, Exception) as e:
            self._error_log.write_error('UrlColl获取url错误' + e)  # 错误日志写入

    def update_url(self, url):
        """
        更新URL数据

        :param url: 需要更新的URL数据
        :return: None
        """
        try:
            self._urls.update({'url': url}, {'$set': {'isExist': 'true'}})  # 更新URL的状态为True表示已经爬取过了
        except (errors, Exception) as e:
            self._error_log.write_error('UrlColl更新URl数据错误' + e)  # 错误日志写入

