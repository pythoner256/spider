import requests
from requests.exceptions import RequestException
from lxml import etree
import time
import random
import json
import pymongo
from multiprocessing.dummy import Pool


def parse_index(url):
    """
    解析首页
    """
    try:
        response = requests.get(url, headers=headers)
        time.sleep(random.randint(1, 2))
        if response.status_code == 200:
            return response.text

        else:
            return None
    except RequestException:
        return None


def get_goods_url(response):
    """
    通过首页获取商品详情页url(只有一半的商品url，后半段是通过异步加载的方式加载)；获取商品sku，构造后半段商品url
    """
    pre_goods_url_list = []
    html = etree.HTML(response)
    goods_urls = html.xpath("//div[@class='gl-i-wrap']/div[@class='p-name']/a")
    if goods_urls:
        for each in goods_urls:
            good_url = each.get('href')
            if good_url.startswith("//item"):
                good_url = "https:" + good_url
                pre_goods_url_list.append(good_url)
            else:
                pre_goods_url_list.append(good_url)
    goods_sku_list = html.xpath("//li[@class='gl-item']")
    if goods_sku_list:
        goods_sku = [goods_sku.get('data-sku') for goods_sku in goods_sku_list]
        return goods_sku, pre_goods_url_list


def get_other_goods_url(sku, index_url):
    """
    获取网页中后半商品的url
    """
    page = int(index_url[-1])
    extend_goods_url_list = []
    extend_url = "https://search.jd.com/s_new.php?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=python&page={}&s=31&scrolling=y&log_id={}&tpl=2_M&show_items={}"
    sec_format = str(time.time() * 100)
    extend_url = extend_url.format(str(page+1), sec_format, ','.join(sku))
    header = {
        'referer': 'https://search.jd.com/Search?keyword=Python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=Python&page={}'.format(str(page)),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.94 Safari/537.36',
    }
    try:
        response = requests.get(extend_url, headers=header).text
        html = etree.HTML(response)
        goods_urls = html.xpath("//div[@class='gl-i-wrap']/div[@class='p-img']/a")
        if goods_urls:
            for each in goods_urls:
                good_url = each.get('href')
                if good_url.startswith("//item"):
                    good_url = "https:" + good_url
                    extend_goods_url_list.append(good_url)
                else:
                    extend_goods_url_list.append(good_url)
    except RequestException:
        pass
    # print("获取后半商品url成功")
    return extend_goods_url_list


def get_goods_info(goods_sku, goods_url_list):
    """
    获取商品详细信息
    """
    goods_name = []
    goods_info = []
    while True:
        response = requests.get(url=goods_url_list.pop(), headers=headers).text
        html = etree.HTML(response)
        name_list = html.xpath("//div[@id='name']/div[@class='sku-name']/text()")[0].strip()
        name = name_list.split('.')[0] if '.' in name_list else name_list  # 书本名包含.符号存入Mongo报错
        goods_name.append(name)
        goods_data = html.xpath("//ul[@id='parameter2']/li/@title")
        goods_info.append(goods_data)

        # pub = html.xpath("//ul[@id='parameter2']/li[1]/@title")[0]
        # bian_ma = html.xpath("//ul[@id='parameter2']/li[4]/@title")[0]
        # pub_time = html.xpath("//ul[@id='parameter2']/li[7]/@title")[0]
        # page = html.xpath("//ul[@id='parameter2']/li[9]/@title")[0]  # TODO 有的商品没有页码或者其他信息
        # print(name, pub, bian_ma, pub_time, page)

        try:
            # price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + str(goods_sku.pop())
            # 大量请求这个接口会返回{“error”:”pdos_captcha”}错误信息，加入pduid参数
            price_url = 'https://p.3.cn/prices/mgets?pduid=' + str(random.randint(100000, 999999)) + '&skuIds=J_' + str(goods_sku.pop())
            response = requests.get(url=price_url, headers=headers).text
            price = json.loads(response)[0]['p']
            goods_data.append(price)
        except Exception:
            pass
        if len(goods_url_list) == 0 and len(goods_sku) == 0:

            break
    return dict(zip(goods_name, goods_info))


def save_goods_info(data):
    """
    存入数据库
    """
    print("开始存入数据\n")
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['jd']
    coll = db['jd_goods']
    coll.insert(data)
    print('存入数据成功')


def main(index_url):
    response = parse_index(index_url)
    goods_sku, pre_goods_url_list = get_goods_url(response)
    extend_goods_url_list = get_other_goods_url(goods_sku, index_url)
    goods_url_list = pre_goods_url_list + extend_goods_url_list
    data = get_goods_info(goods_sku, goods_url_list)
    save_goods_info(data)


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.94 Safari/537.36',
    }
    url = "https://search.jd.com/Search?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=python&page={}"
    format_url = [url.format(str(i)) for i in range(1, 200, 2)]
    pool = Pool(3)
    pool.map(main, format_url)
    pool.close()
    pool.join()
    print("数据存入完毕")

