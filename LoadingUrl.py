from urllib.request import urlopen
from bs4 import BeautifulSoup
from DBController_old import Controller
import time

"""
通过搜索规则获取URL列表

Author:藤藤菜
Version:1.0
Date:2018年2月3日
"""


class LoadingUrl(object):

    def get_soup(self, url):
        response = urlopen(url)
        html = response.read().decode("gbk")
        soup = BeautifulSoup(html, "lxml")
        return soup

    def init_url(self):
        url = "http://category.dangdang.com/"
        for i in range(100):
            for j in range(70):
                if i < 10:
                    temp1 = "0" + str(i)
                else:
                    temp1 = "" + str(i)
                if j < 10:
                    temp2 = "0" + str(j)
                else:
                    temp2 = "" + str(j)
                urls = url + "cp01.41." + temp1 + "." + temp2 + ".00.00.html"
                soup = self.get_soup(urls)
                result = soup.find("div", {"class": "no_result"})
                if result is None:
                    print(urls)
                    soup = self.get_soup(urls)
                    num = soup.find("div", {"class": "data"}).text
                    num = str(num).split("/")[1]
                    num = int(num)
                    print(num)
                    for k in range(1, num):
                        print("当前页数：" + str(k))
                        urls = url + "pg" + str(k) + "-cp01.41." + temp1 + "." + temp2 + ".00.00.html"
                        self.search_url(urls)

    def search_url(self, url):
        soup = self.get_soup(url)
        ul = soup.find("ul", {"class": "bigimg"})
        lis = ul.find_all("li")
        for li in lis:
            href = li.find("a", {"class": "pic"})["href"]
            Controller().add_url(href)
            time.sleep(0.01)
            # print(href)
