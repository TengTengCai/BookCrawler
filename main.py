from Crawler import Crawler
from DBController import MyDatabase, BookColl, UrlColl

HOST = '123.207.85.99'
PORT = 27017
USERNAME = 'book'
PASSWORD = 'tianjun223.'
DB_NAME = 'book'


def main():
    my_database = MyDatabase(HOST, PORT, USERNAME, PASSWORD, DB_NAME).database
    book_coll = BookColl(my_database)
    url_coll = UrlColl(my_database)
    crawler = Crawler(book_coll, url_coll)
    url = url_coll.get_url()
    while not url is None:
        print("加载：" + url)
        crawler.get_book(url)
        url = url_coll.get_url()


if __name__ == '__main__':
    main()
