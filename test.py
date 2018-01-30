from DBController import Controller
import Crawler
import time

start = time.time()
controller = Controller()
crawler = Crawler.Crawler()
url = controller.get_url()
# url = "http://product.dangdang.com/1120327072.html"
while not url is None:
    print("加载："+url)
    crawler.get_book(url)
    url = controller.get_url()
end = time.time()
print(end-start)
