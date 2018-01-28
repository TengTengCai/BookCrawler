from DBController import Controller
import LoadingUrl
import Crawler
import time
import _thread




# import re
# pattern = re.compile(u'^((http)?:\/\/product.dangdang.com)[^\s]+(.html)?')
# str = 'http://product.dangdang.com/23444350.html?rwesdfsd'
# print(pattern.search(str))

# LoadingUrl.LoadingUrl().init_url()


start = time.time()
controller = Controller()
crawler = Crawler.Crawler()
url = controller.get_url()
# url = "http://product.dangdang.com/1280042757.html"
while not url is None:
    print("加载："+url)
    crawler.get_book(url)
    url = controller.get_url()
end = time.time()
print(end-start)



# 为线程定义一个函数
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
#
# # 创建两个线程
# try:
#    _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print ("Error: 无法启动线程")
#
# while 1:
#    pass


# controller = Controller()
# url = controller.get_url()
# print(url)

