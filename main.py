from Crawler import Crawler
from DBController import MyDatabase, BookColl, UrlColl
from time import sleep
from ErrorLog import ErrorLog
from threading import Lock

HOST = '123.207.85.99'
PORT = 27017
USERNAME = 'book'
PASSWORD = 'tianjun223.'
DB_NAME = 'book'


class ThreadCount(object):
    def __init__(self):
        self._lock = Lock()
        self._total = 0

    def add_one(self):
        self._lock.acquire()
        self._total += 1
        self._lock.release()

    def remove_one(self):
        self._lock.acquire()
        self._total -= 1
        self._lock.release()

    @property
    def total(self):
        return self._total


def main():
    thread_count = ThreadCount()
    error_log = ErrorLog()
    error_log.clear_error_log()
    my_database = MyDatabase(HOST, PORT, USERNAME, PASSWORD, DB_NAME).database
    book_coll = BookColl(my_database)
    url_coll = UrlColl(my_database)
    crawler = Crawler(book_coll, url_coll, thread_count)
    url = url_coll.get_url()
    while not url is None:
        if thread_count.total < 5:
            print("加载：" + url)
            crawler.get_book(url)
            url = url_coll.get_url()
        else:
            sleep(10)


if __name__ == '__main__':
    main()
