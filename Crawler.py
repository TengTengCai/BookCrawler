from urllib.request import urlopen
from urllib import error
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import threading
import random

# 写成一个类
from DBController import Controller


# noinspection PyCallingNonCallable

class Crawler:
    def get_book(self, url):
        book = {}

        # req = Request(url)

        driver = webdriver.Firefox(executable_path='E:\DevelopTools\Python\geckodriver')
        # driver = webdriver.Ie(executable_path='E:\DevelopTools\Python\IEDriverServer')
        try:
            driver.set_page_load_timeout(30)
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

        book['url'] = url
        book['book_name'] = soup.find("div", {"class": "name_info"}).h1.get_text(strip=True)
        book['image_url'] = soup.find("div", {"class": "big_pic"}).img['src']
        book['book_type'] = soup.find("div", {"class": "breadcrumb"}).get_text(strip=True)
        book['introduction'] = soup.find("span", {"class": "head_title_name"}).get_text(strip=True)
        book['author'] = soup.find("span", {"id": "author"}).text
        messbox = soup.find("div", {"class": "messbox_info"})
        if messbox is None:
            book['publishing'] = None
            book['publishing_time'] = None
        else:
            if len(messbox.contents) < 3:
                book['publishing'] = None
            elif len(messbox.contents) < 4:
                book['publishing_time'] = None
            else:
                book['publishing'] = messbox.contents[2].a.text
                book['publishing_time'] = messbox.contents[3].get_text(strip=True)
        book['price'] = soup.find("p", {"id": "dd-price"}).get_text(strip=True).split("¥")[1]
        editors_choice = soup.find("div", {"id": "abstract"})
        if editors_choice is None:
            book['editors_choice'] = None
        else:
            book['editors_choice'] = editors_choice.contents[1].get_text()
        content_validity = soup.find("div", {"id": "content"})
        if content_validity is None:
            book['content_validity'] = None
        else:
            book['content_validity'] = content_validity.contents[1].get_text()
        about_author = soup.find("div", {"id": "authorIntroduction"})
        if about_author is None:
            book['about_author'] = None
        else:
            book['about_author'] = about_author.contents[1].get_text()
        catalog = soup.find("textarea", {"id": "catalog-textarea"})
        if catalog is None:
            catalog2 = soup.find("div", {"id": "catalog"})
            if catalog2 is None:
                book['catalog'] = None
            else:
                book['catalog'] = catalog2.contents[1].get_text()
        else:
            book['catalog'] = catalog.get_text(strip=True)
        media_reviews = soup.find("div", {"id": "mediaFeedback"})
        if media_reviews is None:
            book['media_reviews'] = None
        else:
            book['media_reviews'] = media_reviews.get_text()
        # print(soup)

        controller = Controller()
        controller.insert_to_db(book)

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


class MyThread(threading.Thread):
    def __init__(self, soup, thread_id):
        threading.Thread.__init__(self)
        self.soup = soup
        self.thread_id = thread_id

    def run(self):
        print(self.thread_id + "线程开始：")
        get_useful_url(self.soup, self.thread_id)
        print(self.thread_id + "线程退出：")


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


def check_url(url):
    try:
        response = urlopen(url)
        html = response.read().decode("gbk")
        soup = BeautifulSoup(html, "lxml")
        breadcrumb = soup.find("div", {"id": "breadcrumb"}).get_text()
        controller = Controller()
        if "童书" in str(breadcrumb):
            controller.add_url(url)
            time.sleep(0.01)
    except error.HTTPError as e:
        print(e.code)
