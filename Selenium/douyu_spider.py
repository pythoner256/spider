# -*- coding:utf-8 -*-

import unittest
from selenium import webdriver
from bs4 import BeautifulSoup as bs


class DouYu(unittest.TestCase):
    # 初始化方法，必须是setUp()
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.num = 0
        self.count = 0

    # 测试方法必须有test字样开头
    def testDouyu(self):
        self.driver.get("https://www.douyu.com/directory/all")

        while True:
            soup = bs(self.driver.page_source, "lxml")
            names = soup.find_all("h3", {"class" : "ellipsis"})
            numbers = soup.find_all("span", {"class" :"dy-num fr"})

            for name, number in zip(names, numbers):
                print(u"观众人数: -" + number.get_text().strip() + u"-\t房间名: " + name.get_text().strip())
                self.num += 1

            if self.driver.page_source.find("shark-pager-disable-next") != -1:
                    break
            self.driver.find_element_by_class_name("shark-pager-next").click()

    # 测试结束执行的方法
    def tearDown(self):
        # 退出PhantomJS()浏览器
        print("当前网站直播人数" + str(self.num))
        print("当前网站观众人数" + str(self.count))
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
