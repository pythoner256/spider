# 分析目标：我要拿哪些数据：地区（广州，深圳，杭州，上海）；公司名字；公司地址；职位名称；薪水；对应岗位职责。
# 数据写入表格。
# ajax加载方式。
# 整体框架：

import re
import requests
import pandas as pd
import time
import random


def main():
    for i in range(0, 17):
        data = {'firs': 'false', 'pn': str(i), 'kd': 'python'}
        header = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Length': '25',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'www.lagou.com',
                'Origin': 'https://www.lagou.com',
                'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/62.0.3202.94 Safari/537.36',
                'X-Anit-Forge-Code': '0',
                'X-Anit-Forge-Token': 'None',
                'X-Requested-With': 'XMLHttpRequest'
        }
        html = requests.post(url, data=data, headers=header)
        time.sleep(random.randint(2, 5))

        data_list = re.findall(
            '.*?"positionName":"(.*?)".*?"city":"(.*?)","salary":"(.*?)".*?"district":"(.*?)".*?"companyFullName":"(.*?)"',
            html.text
        )
        # print (data_list)
        new_data = pd.DataFrame(data_list)
        new_data.to_csv(
            'D:\\py_project\\practice\\spider crawl project\\lagou\\pythonfile.csv',
            header=False, index=False, mode='a+', encoding='utf-8'
        )


if __name__ == "__main()":
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
    main()
