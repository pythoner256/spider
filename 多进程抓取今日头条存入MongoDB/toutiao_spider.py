import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import re
import os
import pymongo
from config import *
from hashlib import md5
from multiprocessing import Pool

client = pymongo.MongoClient(mongo_host)  # connect=False
db = client[mongo_db]

header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.94 Safari/537.36',
}


def get_page_url(offset, keyword):  # 获取首页响应
    """
    获取今日头条街拍图集url,ajax请求，利用F12开发者工具获取请求链接和请求参数
    """
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3,
        'from': 'gallery'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        print("请求出错")
        return None


def parse_page(html):  # 解析首页响应，获取每个图集的url
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            gallery_url = item.get('article_url')
            yield gallery_url


def get_page_detail(url):  # 解析图集url获取图集的详情页
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        print("请求详情页出错", url)
        return None


def parse_page_detail(gallery_html, each_gallery_url):  # 解析图集的详情页获取每张图片的url
    soup = BeautifulSoup(gallery_html, 'lxml')
    title = soup.select('title')[0].get_text()
    # print(title)
    pattern = re.compile('\sgallery:\sJSON.parse(.*?),\s', re.S)
    result = re.search(pattern, gallery_html)
    image_url_list = result.group(1)[1:-1]  # 取出的json字符串外层还有一层括号，用切片的方式去除括号
    # print(json.loads(result_list))
    image_data = json.loads(image_url_list)
    data = json.loads(image_data)
    # print(isinstance(data, dict))
    if data and 'sub_images' in data.keys():
        sub_images = data.get('sub_images')
        images = [item.get('url') for item in sub_images]  # 获取图集每张图片的url
        for image_url in images:
            download(image_url)
            return {
                'title': title,
                'images': images,
                'url': each_gallery_url
            }


def save_to_mongo(data):  # 将数据存入MongoDB中
    if db[mongo_coll].insert(data):
        print("存入成功")
    return False


def download(image_url):  # 请求图片地址
    print("正在下载", image_url)
    try:
        response = requests.get(image_url, headers=header)
        if response.status_code == 200:
            download_image(response.content)
            return response.text
        else:
            return None
    except RequestException:
        print("请求图片出错", image_url)
        return None


def download_image(content):  # 将图片存入本地
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offest):
    index_html = get_page_url(offest, KEYWORD)
    for each_gallery_url in parse_page(index_html):  # 这里将parse_page作为一个生成器，返回的是每个图集的url
        gallery_html = get_page_detail(each_gallery_url)
        if gallery_html:
            data = parse_page_detail(gallery_html, each_gallery_url)
            # print(data)
            save_to_mongo(data)


if __name__ == "__main__":
    groups = [x*20 for x in (group_start, group_end+1)]
    pool = Pool()
    pool.map(main, groups)




