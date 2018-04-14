from DBController1 import MyDatabase, BookColl, UrlColl

HOST = '123.207.85.99'
PORT = 27017
USERNAME = 'book'
PASSWORD = 'tianjun223.'
DB_NAME = 'book'


def main():
    my_database = MyDatabase(HOST, PORT, USERNAME, PASSWORD, DB_NAME).database
    book_coll = BookColl(my_database)
    url_coll = UrlColl(my_database)
    url_str = url_coll.get_url()
    print(url_str)
    pass


if __name__ == '__main__':
    main()
