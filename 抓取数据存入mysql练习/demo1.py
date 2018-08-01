import requests
from bs4 import BeautifulSoup
import MySQLdb


conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='password', db='test2'，charset='utf8')
print(">>>已连接")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS COLOR")
sql_sentence = "create table COLOR (id int auto_increment primary key,color char(20) not null, rgb char(10),\
               Style char(50))"
cur.execute(sql_sentence)


def craw_practice(url, header):
    re = requests.get(url, headers=header).content
    s = BeautifulSoup(re, 'lxml')
    tr_list = s.find_all('tr')
    for tr in tr_list:
        style_list = tr.get('style')  # 获取所有tr标签里的style属性
        td = [x for x in tr]
        name = td[1].text.strip()  # 获取名字
        co_rgb = td[2].text.strip()  # 获取颜色RGB
        insert_color = "INSERT INTO COLOR(color,rgb,Style) VALUES(%s,%s,%s)"
        data_color = (name, co_rgb, style_list)
        cur.execute(insert_color, data_color)
        conn.commit()
    print(">>>存储完毕")


if __name__ == "__main__":
    url = "http://html-color-codes.info/color-names/"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.94 Safari/537.36',
        }
    craw_practice(url, header)
