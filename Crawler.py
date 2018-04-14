from urllib.request import urlopen
from urllib import error
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from threading import Thread
from random import randint
from ErrorLog import ErrorLog


class Crawler(object):
    def __init__(self, book_coll, url_coll, thread_count):
        self._book_coll = book_coll
        self._url_coll = url_coll
        self._thread_count = thread_count
        self._error_log = ErrorLog()

    def get_book(self, url):
        book = {}
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
            self._error_log.write_error(e)
            return
        finally:
            driver.close()
        # target = driver.find_element_by_id("footer")
        # driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去
        null_wrap = soup.find("div", {"class": "null_wrap"})
        if not null_wrap is None:
            self._url_coll.update_url(url)
            return
        book['url'] = url
        book_name = soup.find("div", {"class": "name_info"})
        if book_name is None:
            self._url_coll.update_url(url)
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
        self._book_coll.insert_to_db(book)
        # print(book)
        print(url + "完成")
        try:
            self._thread_count.add_one()
            thread = MyThread(soup, self._url_coll, self._thread_count)
            thread.start()
        except Exception as e:
            self._error_log.write_error(e)
            print("Error: 无法启动线程" + e)


# 子线程
class MyThread(Thread):
    def __init__(self, soup, url_coll, thread_count):
        super().__init__()
        self._soup = soup
        self._url_coll = url_coll
        self._thread_count = thread_count
        self._thread_id = str(randint(100, 1000))

    def run(self):
        print(self._thread_id + "线程开始：")
        get_useful_url(self._soup, self._thread_id, self._url_coll)
        self._thread_count.remove_one()
        print(self._thread_id + "线程退出：")


# 获取有用的URL
def get_useful_url(soup, thread_id, url_coll):
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
        if not url_coll.is_exist_url(url):
            check_url(url, url_coll)
            print(thread_id + "扫描：" + url)


# 检查URL是否符合要求
def check_url(url, url_coll):
    try:
        response = urlopen(url)
        html = response.read().decode("gbk")
        soup = BeautifulSoup(html, "lxml")
        breadcrumb = soup.find("div", {"id": "breadcrumb"}).get_text()
        if "童书" in str(breadcrumb):
            url_coll.add_url(url)
            time.sleep(0.1)
    except (error.HTTPError, UnicodeDecodeError,
            TimeoutError, error.URLError) as e:
        print(e.code)
