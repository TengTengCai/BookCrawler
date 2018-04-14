from DBController_old import Controller
import Crawler_old
import time

"""
爬虫启动程序

Author:藤藤菜
Version:1.0
Date:2018年2月8日
"""


def main():
    start = time.time()
    controller = Controller()
    crawler = Crawler_old.Crawler()
    url = controller.get_url()
    # url = "http://product.dangdang.com/1120327072.html"
    while not url is None:
        print("加载：" + url)
        crawler.get_book(url)
        url = controller.get_url()
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()
