import requests
from requests.exceptions import RequestException
import re
import json
import time


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None


def parse(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src='
                         + '"(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)'
                         + '</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)'
                         + '</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    info = re.findall(pattern, html)
    for item in info:
        yield {
            'movie_rank': item[0],
            'movie_img': item[1],
            'movie_name': item[2],
            'movie_star': item[3].strip(),
            'movie_releasetime': item[4],
            'movie_score': item[5] + item[6],
        }


def dowmload(item):
    with open('maoyan_movie.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://maoyan.com/board/4?offset=0' + str(offset)
    html = get_html(url)
    for content in parse(html):
        dowmload(content)


if __name__ == "__main__":
    for i in range(10):
        offset = i*10
        main(offset)
        time.sleep(1)


