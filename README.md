# spider
一些爬虫小项目
## 多进程抓取58同城项目说明
### 所需安装包
- Pyhthon3.6
- requests
- pymongo
- bs4解析库
使用pip install 命令安装
- count.py为计数，在跑爬虫程序的时候运行此程序统计存入MongoDB中的数据量
- 注意爬虫文件需要在同一个目录下
---
## 多线程抓取斗图吧说明
### 所需安装包
- Python3.6
- requests
使用pip install 命令安装
抓取过程因为请求量很大，需要用到代理，可能在请求的过程中服务端会主动关闭连接，让程序适当睡几秒，并关闭response，调用socket设置默认超时时长。
---
## 数据存入mysql练习说明
### 所需安装包
- Python3.6
- mysql驱动MySQLdb
- bs4解析库
使用 pip install 命令安装所需库


