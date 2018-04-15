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
        """
        初始化爬虫对象

        :param book_coll: book集合对象
        :param url_coll: URL集合对象
        :param thread_count: 线程数量统计对象
        """
        self._book_coll = book_coll  # 初始化对象
        self._url_coll = url_coll
        self._thread_count = thread_count
        self._error_log = ErrorLog()  # 新建错误日志输出记录对象

    def get_book(self, url):
        """
        获取书籍数据

        :param url: 获取书籍的URL地址
        :return: None
        """
        book = {}  # 初始化字典 用于保存数据
        # 初始化浏览器驱动程序，获得浏览器驱动对象
        driver = webdriver.Firefox(executable_path='E:\DevelopTools\Python\geckodriver')
        # driver = webdriver.Ie(executable_path='E:\DevelopTools\Python\IEDriverServer')
        try:
            driver.set_page_load_timeout(60)  # 设置页面加载超时时间
            driver.set_script_timeout(30)  # 设置页面脚本响应超时时间
            driver.get(url)  # 设置浏览器获取页面的地址
            js = "var q=document.documentElement.scrollTop=100000"  # 浏览器执行的js代码 向下滑动100000xp
            driver.execute_script(js)  # 运行脚本
            time.sleep(1)  # 休眠等待浏览器执行
            js = "var q=document.documentElement.scrollTop=0"  # 浏览器js代码 回到顶部
            driver.execute_script(js)  # 运行脚本
            time.sleep(2)  # 休眠等待浏览器执行
            js = "var q=document.documentElement.scrollTop=100000"  # 浏览器js代码， 回到底部
            driver.execute_script(js)  # 运行脚本
            time.sleep(1)  # 休眠等待浏览器执行， 模拟浏览器滑动完成
            soup = BeautifulSoup(driver.page_source, "lxml")  # 传递页面数据， 初始化bs4对象
        except Exception as e:
            print(e)  # 输出错误信息
            self._error_log.write_error(e)  # 记录错误信息
            return  # 返回空
        finally:
            driver.close()  # 关闭浏览器
        # target = driver.find_element_by_id("footer")
        # driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去

        # 下面是相关标签的数据获取
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
        # 数据获取成功，插入book集合
        self._book_coll.insert_to_db(book)
        print(url + "完成")
        try:
            self._thread_count.add_one()  # 线程计数加一
            thread = MyThread(soup, self._url_coll, self._thread_count)  # 创建线程对象
            thread.start()  # 开启线程
        except Exception as e:
            self._error_log.write_error(e)  # 写入错误日志
            print("Error: 无法启动线程" + e)


class MyThread(Thread):
    """扫描有效URL子线程"""
    def __init__(self, soup, url_coll, thread_count):
        """
        子线程初始化方法

        :param soup: html 页面资源
        :param url_coll: url集合对象
        :param thread_count: 线程计数对象
        """
        super().__init__()  # 父类构造方法
        self._soup = soup  # 初始化参数和对象
        self._url_coll = url_coll
        self._thread_count = thread_count
        self._thread_id = str(randint(100, 1000))

    def run(self):
        """
        线程开启后执行的行为

        :return: None
        """
        print(self._thread_id + "线程开始：")
        # 调用方法获取有效URL
        get_useful_url(self._soup, self._thread_id, self._url_coll)
        self._thread_count.remove_one()
        print(self._thread_id + "线程退出：")


def get_useful_url(soup, thread_id, url_coll):
    """
    获取有效的URL

    :param soup: html 资源对象
    :param thread_id:  线程ID
    :param url_coll:  URL集合对象
    :return: None
    """
    url_list = []  # 初始化URL列表对象

    # 通过正则表达式进行第一次筛选，选出有书籍ID的URL
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

    # 消除列表中重复的URL
    url_list = set(url_list)
    for url in url_list:
        # 向数据库进行查询，是否存在URL
        if not url_coll.is_exist_url(url):  # 如果不存在
            check_url(url, url_coll)  # 进行第二次筛选
            print(thread_id + "扫描：" + url)


def check_url(url, url_coll):
    """
    对URL进行第二次筛选

    :param url: URL地址
    :param url_coll: URL集合对象
    :return: None
    """
    try:
        response = urlopen(url)  # 打开页面，获取相应对象
        html = response.read().decode("gbk")  # 以GBK编码对页面进行解析
        soup = BeautifulSoup(html, "lxml")  # 解析页面获取html对象
        breadcrumb = soup.find("div", {"id": "breadcrumb"}).get_text()  # 获取标签数据
        if "童书" in str(breadcrumb):  # 判断是否是属于童书
            url_coll.add_url(url)  # 是就添加到URL集合中
            time.sleep(0.1)
    except (error.HTTPError, UnicodeDecodeError,
            TimeoutError, error.URLError) as e:
        print(e)  # 输出错误提示
