import urllib.request
import re


class DuanZi:
    def __init__(self):  # 初始化页面
         self.page = 2
         self.switch = True

    def load_txt(self):  # 发送http请求，接收html文件
        url = "http://www.neihan8.com/wenzi/index_"+str(self.page)+".html"
        headers = {"User-Agent":
                   'Mozilla/5.0 (Windows NT 6.1) \
                   AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/62.0.3202.94 Safari/537.36'}
        request = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(request).read()
        content_list = re.compile('<div\sclass="desc">(.*?)</div>', re.S).findall(html)
        self.handl_text(content_list)

    def handl_text(self, content_list):  # 处理无规则文件
        for item in content_list:
            item = item.replace('&amp;hellip', ' ')
            self.write_text(item)

    def write_text(self, item):  # 写入到本地
        with open('nei han duan zi.txt', 'a')as f:
            f.write(item)

    def control(self):  # 控制爬虫次数和开关
        while self.switch:
            command = input("如果要继续爬取，请按回车，如果退出请输入quit")
            if command == "quit":
                self.switch = False
            self.load_txt()
            self.page += 1
        print('谢谢使用')


if __name__ == "__main__":
    duan_zi = DuanZi()
    # duanzi.loadtxt()
    duan_zi.control()




