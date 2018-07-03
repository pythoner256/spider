import requests
import lxml
from bs4 import BeautifulSoup


def loadfile(url):
    html = requests.get(url).text
    return html


def tiezifile(html):
    soup = BeautifulSoup(html, 'lxml')
    tieziurl_list = soup.find_all('a', attrs={'class': 'j_th_tit '})
    for tieziurl in tieziurl_list:
        tiezifull_url = 'https://tieba.baidu.com'+tieziurl['href']
        image_html = requests.get(tiezifull_url)
        image(image_html)


def image(image_html):
    soup = BeautifulSoup(image_html.text, 'lxml')
    image_list_url = soup.find_all('img', attrs={'class': 'BDE_Image'})
    for image_url in image_list_url:
        all_image_url = image_url['src']

        res = requests.get(all_image_url).content
        write(res, all_image_url)


def write(res, all_image_url):
    for all_image in all_image_url:
        filename = all_image[-9:]
        # print (filename)
        with open(filename, 'wb')as f:
            f.write(res)


if __name__ == "__main__":
    url = 'https://tieba.baidu.com/f?kw=%C3%C0%C5%AE&fr=ala0&tpl=5'
    html = loadfile(url)
    tiezifile(html)
