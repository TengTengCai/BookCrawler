from LoadingUrl import LoadingUrl
from DBController import MyDatabase, BookColl


# LoadingUrl().init_url()
HOST = '123.207.85.99'
PORT = '27017'
USERNAME = 'book'
PASSWORD = 'tianjun223.'
DB_NAME = 'book'


def main():
    my_database = MyDatabase().database
    book_coll = BookColl(my_database)
    result = book_coll.get_book_name()
    print(result)
    pass


if __name__ == '__main__':
    main()
