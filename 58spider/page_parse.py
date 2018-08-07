import requests
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient('localhost', 27017)  # 建立连接
ceshi = client['ceshi']  # 新建数据库
url_list = ceshi['url_list']  # 新建集合url_lsit存放商品链接
item_info = ceshi['item_info']  # 新建集合item_info存放商品信息

header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.94 Safari/537.36',
}


def get_goods_urls(category, pages, who_sells=0):
    goods_url_list = []
    """
    获取分类里所有商品的链接地址
    接收三个参数一个是分类，一个是页码，一个是属于个人还是商家，这里默认为个人
    """
    re = requests.get(category, headers=header)
    s = requests.session()
    s.keep_alive = False
    soup = BeautifulSoup(re.text, 'lxml')
    choice = soup.find('div', 'tab_bar')
    if choice:  # 一些类目没有分个人商家，这里做个判断
        list_view = '{}{}/pn{}'.format(category, str(who_sells), str(pages))
    else:
        list_view = '{}/pn{}'.format(category, str(pages))
    response = requests.get(list_view, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    item_a_list = soup.select('td.t > a.t')
    if soup.find('td', 't'):
        for link in item_a_list:
            item_url = link.get('href').split('?')[0]
            goods_url_list.append(item_url)
            url_list.insert_one({"url": item_url})
    else:
        pass
    return goods_url_list


def get_goods_info(url):
    data = requests.get(url, headers=header)
    soup = BeautifulSoup(data.text, 'lxml')

    condition = '404' in soup.find('script', type='text/javascript').get('src').split('/')
    """
    一些商品可能在抓取的过程中已经被交易,如果再去访问会出现404页面
    """
    if condition:
        pass
    else:
        title = soup.title.text.split()[1]
        price = soup.select('span.price.c_f50')[0].text
        date = soup.select('li.time')[0].text
        area = list(soup.select('span.c_25d a')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None
        """一些商品可能不包含地区信息，这里做一个判断"""
        item_info.insert_one({"title": title, "price": int(price), "date": date, "area": area})
        # print({"title": title, "price": price, "date": date, "area": area})




