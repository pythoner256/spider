import requests
from requests.exceptions import RequestException
import json

url = 'https://m.weibo.cn/api/container/getIndex?containerid=1076032329184531'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.94 Safari/537.36',
    'Referer': 'https://m.weibo.cn/p/1005052329184531',
    'Host': 'm.weibo.cn',
    'MWeibo-Pwa': '1'
}


def get_html():
    """
    获取首页数据
    """
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException as e:
        print("Error", e.args)


def parse_index(html):
    """
    解析首页数据，获取page,作为下一页url参数
    """
    data = json.loads(html)
    if data and 'data' in data.keys():
        page = data['data']['cardlistInfo']['page']
        mblog = data['data']['cards']
        for item in mblog:
            weibo_time = item['mblog'].get('created_at')  # 微博发表时间
            weibo_source = item['mblog'].get('source')  # 微博来源
            weibo_text = item['mblog'].get('raw_text')  # 微博文本
            download({'微博时间': weibo_time, '微博来源': weibo_source, '微博文本': weibo_text})
        print('第一页数据保存完毕')
        return page


def parse_next(page):
    """
    将上一页获取到的page值作为参数放到下一页url中，解析并获取微博数据
    """
    next_link = url + "&page=" + str(page)
    try:
        response = requests.get(next_link, headers=headers).text
        weibo_data = json.loads(response)
        if weibo_data and 'data' in weibo_data.keys():
            next_page = weibo_data['data']['cardlistInfo'].get('page')
            mblog = weibo_data['data']['cards']
            for item in mblog:
                weibo_time = item['mblog'].get('created_at')  # 微博发表时间
                weibo_source = item['mblog'].get('source')  # 微博来源
                weibo_text = item['mblog'].get('raw_text')  # 微博主题
                download({'微博时间': weibo_time, '微博来源': weibo_source, '微博文本': weibo_text})
            if next_page:
                print('第%d页数据保存完毕' % next_page)
                print('开始解析下一页')
                parse_next(next_page)
            else:
                print('微博全部抓取完毕')
    except RequestException as e:
        print('Error', e.args)


def download(content):
    """
    保存到本地
    """
    data = json.dumps(content, ensure_ascii=False)
    with open('weibo.txt', 'a', encoding='utf-8') as f:
        f.write(data)


def main():
    html = get_html()
    page = parse_index(html)
    parse_next(page)


if __name__ == "__main__":
    main()
