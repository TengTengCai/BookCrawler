from Crawler import Crawler
from DBController import MyDatabase, BookColl, UrlColl
from time import sleep
from ErrorLog import ErrorLog
from threading import Lock

HOST = '123.207.85.99'  # 主机地址
PORT = 27017  # 主机端口号
USERNAME = 'book'  # 数据库用户名
PASSWORD = 'tianjun223.'  # 数据库密码
DB_NAME = 'book'  # 文档名称


class ThreadCount(object):
    """
    线程计数限制类
    """
    def __init__(self):
        """
        初始化方法
        """
        self._lock = Lock()  # 线程锁
        self._total = 0  # 初始化线程计数

    def add_one(self):
        """
        线程计数加一

        :return: None
        """
        self._lock.acquire()  # 加锁
        self._total += 1  # 计数加一
        self._lock.release()  # 释放锁

    def remove_one(self):
        """
        当线程结束后减一

        :return: None
        """
        self._lock.acquire()  # 进程锁
        self._total -= 1  # 计数减一
        self._lock.release()  # 释放锁

    @property
    def total(self):
        """
        获取计数的值

        :return: total对当前计数的数值
        """
        return self._total


def main():
    thread_count = ThreadCount()  # 创建线程计数对象
    error_log = ErrorLog()  # 创建错误日志记录对象
    error_log.clear_error_log()  # 如果没有文件新建文件，清空错误日志
    my_database = MyDatabase(HOST, PORT, USERNAME, PASSWORD, DB_NAME).database  # 初始化数据库对象，获取数据库对象
    book_coll = BookColl(my_database)  # 获取book集合
    url_coll = UrlColl(my_database)  # 获取URL集合
    crawler = Crawler(book_coll, url_coll, thread_count)  # 新建爬虫对象
    url = url_coll.get_url()  # 从URL集合中获取一条URL数据
    while not url is None:  # 判断是否为空
        if thread_count.total < 5:  # 判断当前线程数量是否超出
            print("加载：" + url)
            crawler.get_book(url)  # 让爬虫获取书籍页面
            url = url_coll.get_url()  # 获取新的URL数据
        else:  # 线程数量超出
            sleep(10)  # 休眠10秒等待，线程执行完成


if __name__ == '__main__':
    main()
