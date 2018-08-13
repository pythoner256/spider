import requests
from urllib.request import urlretrieve
import urllib.error
from bs4 import BeautifulSoup

import time
import random
import os
import socket

import threading


socket.setdefaulttimeout(20)  # 设置socket层超时时间为20秒
user_agent = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
header = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
        #               'AppleWebKit/537.36 (KHTML, like Gecko) '
        #               'Chrome/62.0.3202.94 Safari/537.36',
        'User-Agent': random.choice(user_agent)
}

proxy_list = [
    'http://14.112.76.71:3128',
    'http://61.157.136.105:808',
    'http://110.73.3.194:8123',
    ]

# proxy_ip = random.choice(proxy_list)
# proxies = {'http': proxy_ip}

url = "https://www.doutula.com/article/list/?page="
full_url = [url+str(i) for i in range(50)]  # 存放每一页的url
image_url_list = []  # 存放详情页里每张图片的url


def get_image_url(global_lock):  # 获取每一页的url
    while True:
        if len(full_url) > 0:
            global_lock.acquire()
            page_url = full_url.pop()
            global_lock.release()
            try:
                response = requests.get(page_url, headers=header)
                time.sleep(random.randint(2, 3))
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                image_list = soup.find_all('img', attrs={'class': 'lazy image_dtb img-responsive'})
                response.close()
                global_lock.acquire()
                for image_url in image_list:
                    image_url = image_url.get('data-original')
                    image_url_list.append(image_url)
                global_lock.release()
            except urllib.error.URLError as e:
                print(e)
        else:
            break


def download_image(global_lock):  # 下载详情页中的图片
    while True:
        global_lock.acquire()
        if len(image_url_list) == 0:
            global_lock.release()
            continue
        else:
            image_url = image_url_list.pop()
            global_lock.release()
            image_name = image_url.split('/')[-1]
            path = 'images'
            filename = os.path.join(path, image_name)
            urlretrieve(image_url, filename=filename)
            print("正在下载%s" % filename)


def main():
    global_lock = threading.Lock()
    for x in range(3):
        th = threading.Thread(target=get_image_url, args=(global_lock, ))
        th.start()

    for y in range(5):
        th = threading.Thread(target=download_image, args=(global_lock, ))
        th.start()


if __name__ == "__main__":
    main()
