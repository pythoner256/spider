from multiprocessing import Pool
from get_category import category_list
from page_parse import get_goods_urls


def get_all_links(category):
    for num in range(1, 101):
        goods_urls = get_goods_urls(category, num)


if __name__ == "__main__":
    pool = Pool()
    pool.map(get_all_links, category_list.split())

