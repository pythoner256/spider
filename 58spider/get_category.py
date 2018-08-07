import requests
from bs4 import BeautifulSoup


url = "http://sz.58.com/sale.shtml"


def get_category(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    links_parent = soup.select('ul.ym-mainmnu > li > span > a')  # 获取所有二手分类类目的a节点
    links_parent.pop()  # 最后一个分类没有a节点，剔除
    links_son = soup.select('ul.ym-submnu > li > b > a')  # 获取大分类里的小分类
    # print(links_son)
    links = links_parent+links_son
    pre_url = "http://cn.58.com"
    for link in links:
        last_ulr = link.get('href')
        full_url = pre_url + last_ulr
        # print(full_url)

# 所有类目的链接地址


category_list = """
http://sz.58.com/shouji/
http://sz.58.com/tongxunyw/
http://sz.58.com/danche/
http://sz.58.com/diandongche/
http://sz.58.com/diannao/
http://sz.58.com/shuma/
http://sz.58.com/jiadian/
http://sz.58.com/ershoujiaju/
http://sz.58.com/yingyou/
http://sz.58.com/fushi/
http://sz.58.com/meirong/
http://sz.58.com/yishu/
http://sz.58.com/tushu/
http://sz.58.com/wenti/
http://sz.58.com/kaquan/
http://sz.58.com/shebei.shtml
http://sz.58.com/chengren/
http://sz.58.com/shouji/
http://sz.58.com/tongxunyw/
http://sz.58.com/danche/
http://sz.58.com/diandongche/
http://sz.58.com/fzixingche/
http://sz.58.com/sanlunche/
http://sz.58.com/peijianzhuangbei/
http://sz.58.com/diannao/
http://sz.58.com/bijiben/
http://sz.58.com/pbdn/
http://sz.58.com/diannaopeijian/
http://sz.58.com/zhoubianshebei/
http://sz.58.com/shuma/
http://sz.58.com/shumaxiangji/
http://sz.58.com/mpsanmpsi/
http://sz.58.com/youxiji/
http://sz.58.com/ershoukongtiao/
http://sz.58.com/dianshiji/
http://sz.58.com/xiyiji/
http://sz.58.com/bingxiang/
http://sz.58.com/jiadian/
http://sz.58.com/binggui/
http://sz.58.com/chuang/
http://sz.58.com/ershoujiaju/
http://sz.58.com/yingyou/
http://sz.58.com/yingeryongpin/
http://sz.58.com/muyingweiyang/
http://sz.58.com/muyingtongchuang/
http://sz.58.com/yunfuyongpin/
http://sz.58.com/fushi/
http://sz.58.com/nanzhuang/
http://sz.58.com/fsxiemao/
http://sz.58.com/xiangbao/
http://sz.58.com/meirong/
http://sz.58.com/yishu/
http://sz.58.com/shufahuihua/
http://sz.58.com/zhubaoshipin/
http://sz.58.com/yuqi/
http://sz.58.com/tushu/
http://sz.58.com/tushubook/
http://sz.58.com/wenti/
http://sz.58.com/yundongfushi/
http://sz.58.com/jianshenqixie/
http://sz.58.com/huju/
http://sz.58.com/qiulei/
http://sz.58.com/yueqi/
http://sz.58.com/kaquan/
http://sz.58.com/bangongshebei/
http://sz.58.com/diannaohaocai/
http://sz.58.com/bangongjiaju/
http://sz.58.com/ershoushebei/
http://sz.58.com/chengren/
http://sz.58.com/nvyongpin/
http://sz.58.com/qinglvqingqu/
http://sz.58.com/qingquneiyi/
http://sz.58.com/chengren/
http://sz.58.com/xiaoyuan/
http://sz.58.com/ershouqiugou/
http://sz.58.com/tiaozao/
    """