import re
import urllib.request
from bs4 import BeautifulSoup
import lxml


def load_image(full_url):
    request = urllib.request.Request(full_url)
    response = urllib.request.urlopen(request)
    return response.read()


def hand_url(html):
    soup = BeautifulSoup(html, 'lxml')
    url_list = soup.find_all('img', src=re.compile(r'.jpg'))
    for new_url in url_list:
        image_url = 'http://qq.yh31.com'+new_url['src']
        write_image(image_url)


def write_image(image_url):
    new_request = urllib.request.Request(image_url)
    image = urllib.request.urlopen(new_request).read()
    filename = image_url[-9:]
    with open(filename, 'wb')as f:
        f.write(image)


if __name__ == "__main__":
    url = 'http://qq.yh31.com/zjbq/0551964'
    for page in range(0, 5):
        if page == 0:
            full_url = url+'.html'
        else:
            full_url = url+'_'+str(page)+'.html'
        html = load_image(full_url)
        hand_url(html)
