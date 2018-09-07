import csv

with open("practice.csv", 'a', encoding='utf-8') as f:
    # 定义表头字段信息
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    # 先写入表头字段
    writer.writeheader()
    # 单个数据写入
    writer.writerow({'id': 1, 'name':'小明','age':18})
    # 多个数据写入,多个数据是以列表的形式
    writer.writerows([{'id': 2, 'name':'小张','age':18},{'id': 3, 'name':'小红','age':18}])