# 爬虫项目说明
- [多进程抓取58同城](https://github.com/pythoner256/spider/tree/master/58spider)
## 58demo思路
1.分析抓取目标，抓取深圳58同城二手市场下所有类目下的商品信息，包括商品名称，价格，地区和发布时间；

2.目标数据分析，通过多个页面观察发现这些信息都可以在商品详情页提取，商品详情页包含所有、个人和商家三个类目，不同的类目url也是跟着变化的，这里只抓取所有商家的商品；

3.通过抓包发现58网站请求是get请求，目标数据都在源码中，所以直接发送get请求返回源码进行解析；

4.设计思路：先获得所有二手类目的url，然后分别发送请求获取类目下所有商品的详情页url，再请求商品详情url解析获取数据

5.为了提升抓取效率采用多进程的方式抓取


### 需要注意的点是
1.部分商品不含地区；

2.在抓取的过程中商品可能已经被交易了；

3.一些类目没有分个人和商家需要区别对待；

4.58的反爬，会有ip限制；




- [线程池抓取京东商品](https://github.com/pythoner256/spider/tree/master/jd_spider)
- [scrapy抓取Amazon家居类所有商品信息](https://github.com/pythoner256/spider/tree/master/amazon_spider)
- [scrapy抓取腾讯深圳社招所有信息](https://github.com/pythoner256/spider/tree/master/tentcent_scrapy)
- [scrapy抓取ITcast所有教师信息](https://github.com/pythoner256/spider/tree/master/itcast_scrapy)
- [scrapy抓取豆瓣电影信息](https://github.com/pythoner256/spider/tree/master/scrapy_douban_movie)
- [selenium处理js加载分页网站；模拟登陆](https://github.com/pythoner256/spider/tree/master/Selenium%2BPhantomJS)
- [知乎用户爬虫](https://github.com/pythoner256/spider/tree/master/zhihuuser)
 - [一些爬虫总结，一些是用jupyter notebook写的html文件,可以下载用浏览器打开，一些是用xmind写的总结](https://github.com/pythoner256/spider/tree/master/%E7%88%AC%E8%99%AB%E6%80%BB%E7%BB%93)


