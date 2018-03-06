from urllib.request import urlopen
from urllib import error
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import threading
import random
"""
爬虫，进行动态网页获取，解析数据，子线程 广度遍历URL

Author:藤藤菜
Version:1.0
Date:2018年2月7日
"""
# 写成一个类
from DBController import Controller


# noinspection PyCallingNonCallable

class Crawler:

    def get_book(self, url):
        book = {}
        controller = Controller()
        # req = Request(url)

        driver = webdriver.Firefox(executable_path='E:\DevelopTools\Python\geckodriver')
        # driver = webdriver.Ie(executable_path='E:\DevelopTools\Python\IEDriverServer')
        try:
            driver.set_page_load_timeout(60)
            driver.set_script_timeout(30)
            driver.get(url)
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            time.sleep(1)
            js = "var q=document.documentElement.scrollTop=0"
            driver.execute_script(js)
            time.sleep(2)
            js = "var q=document.documentElement.scrollTop=100000"
            time.sleep(1)
            driver.execute_script(js)
            soup = BeautifulSoup(driver.page_source, "lxml")
        except Exception as e:
            print(e)
            return
        finally:
            driver.close()
        # target = driver.find_element_by_id("footer")
        # driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去
        null_wrap = soup.find("div", {"class": "null_wrap"})
        if not null_wrap is None:
            controller.delete_url(url)
            return
        book['url'] = url
        book_name = soup.find("div", {"class": "name_info"})
        if book_name is None:
            controller.delete_url(url)
            return
        book['book_name'] = book_name.h1.get_text(strip=True)
        book['image_url'] = soup.find("div", {"class": "big_pic"}).img['src']
        book['book_type'] = soup.find("div", {"class": "breadcrumb"}).get_text(strip=True)
        book['introduction'] = soup.find("span", {"class": "head_title_name"}).get_text(strip=True)
        author = soup.find("span", {"id": "author"})
        if author is None:
            book['author'] = ""
        else:
            book['author'] = soup.find("span", {"id": "author"}).text
        messbox = soup.find("div", {"class": "messbox_info"})
        for item in messbox:
            if "出版社" in str(item):
                book['publishing'] = item.get_text(strip=True)
            elif "出版时间" in str(item):
                book['publishing_time'] = item.get_text(strip=True)
        book['price'] = soup.find("p", {"id": "dd-price"}).get_text(strip=True).split("¥")[1]
        editors_choice = soup.find("div", {"id": "abstract"})
        if editors_choice is None:
            book['editors_choice'] = ""
        else:
            book['editors_choice'] = editors_choice.contents[1].get_text()
        content_validity = soup.find("div", {"id": "content"})
        if content_validity is None:
            book['content_validity'] = ""
        else:
            book['content_validity'] = content_validity.contents[1].get_text()
        about_author = soup.find("div", {"id": "authorIntroduction"})
        if about_author is None:
            book['about_author'] = ""
        else:
            book['about_author'] = about_author.contents[1].get_text()
        catalog = soup.find("textarea", {"id": "catalog-textarea"})
        if catalog is None:
            catalog2 = soup.find("div", {"id": "catalog"})
            if catalog2 is None:
                book['catalog'] = ""
            else:
                book['catalog'] = catalog2.contents[1].get_text()
        else:
            book['catalog'] = catalog.get_text(strip=True)
        media_reviews = soup.find("div", {"id": "mediaFeedback"})
        if media_reviews is None:
            book['media_reviews'] = ""
        else:
            book['media_reviews'] = media_reviews.get_text()
        # print(soup)
        controller.insert_to_db(book)
        # print(book)
        print(url + "完成")
        try:
            thread_id = str(random.randint(1, 1000))
            thread = MyThread(soup, thread_id)
            thread.start()
        except:
            print("Error: 无法启动线程")

            # get_useful_url(soup)

            # new_url = controller.get_url()
            # if not new_url is None:
            #     self.get_book(new_url)


# 子线程
class MyThread(threading.Thread):
    def __init__(self, soup, thread_id):
        threading.Thread.__init__(self)
        self.soup = soup
        self.thread_id = thread_id

    def run(self):
        print(self.thread_id + "线程开始：")
        get_useful_url(self.soup, self.thread_id)
        print(self.thread_id + "线程退出：")


# 获取有用的URL
def get_useful_url(soup, thread_id):
    controller = Controller()
    url_list = []
    for link in soup.find_all('a', {"href": re.compile(u'^[\d](.html)?')}):
        href = str(link.get('href')).split("#")[0]
        href = href.replace("/", "")
        if len(href) < 30:
            if "javascript" not in href:
                url = "http://product.dangdang.com/" + href
                url_list.append(url)

    for link in soup.find_all('a', {"href": re.compile(u'^\/[\d](.html)?')}):
        href = str(link.get('href')).split("#")[0]
        url = "http://product.dangdang.com" + href
        url_list.append(url)

    url_list = set(url_list)
    for url in url_list:
        if not controller.is_exist_url(url):
            check_url(url)
            print(thread_id + "扫描：" + url)


# 检查URL是否已经被获取过了
def check_url(url):
    try:
        response = urlopen(url)
        html = response.read().decode("gbk")
        soup = BeautifulSoup(html, "lxml")
        breadcrumb = soup.find("div", {"id": "breadcrumb"}).get_text()
        controller = Controller()
        if "童书" in str(breadcrumb):
            controller.add_url(url)
            time.sleep(0.1)
    except (error.HTTPError, UnicodeDecodeError) as e:
        print(e.code)
