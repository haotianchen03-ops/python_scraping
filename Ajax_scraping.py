import requests  # 爬取
import logging  # 输出信息,用于记录日志
import re
import pymongo
from pyquery import PyQuery as pq
from urllib.parse import urljoin  # 网站拼接
import multiprocessing
import certifi
from requests.auth import HTTPBasicAuth
from multiprocessing import Manager
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LIMIT = 10
TOTAL_PAGES = 11


def scrape_api(url):  # 专门处理json接口
    # logging.info(f'Scraping {url}')
    try:
        response = requests.get(url, verify=certifi.where())
        if response.status_code == 200:
            return response.json()  # 转化为json字符串

        logging.error(f'Scraping {url} failed,{response.status_code}')

    except requests.exceptions.RequestException:
        logging.error(f'error occurred while scraping {url}, {response.status_code}', exc_info=True)


Index_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'
'''
用Index_URL.format(limit=10, offset=10)改变{}内容
'''


def scrape_index(page):  # 用于构造列表页 API 请求地址，并获取对应页的数据
    index_url = Index_URL.format(limit=LIMIT, offset=LIMIT*(page-1))
    return scrape_api(index_url)


detail_url = 'https://spa1.scrape.center/api/movie/{id}'  # 注意要看检查中的"请求URL"，而不是网页上的！会不一样！


def scrape_detail(id):  # 根据电影 ID 构造详情页 URL，获取详情页的 HTML 或数据。
    url = detail_url.format(id=id)
    return scrape_api(url)


client = pymongo.MongoClient('localhost', 27017)
db = client['test']
collection = db['Ajax']


def save_data(data):
    collection.update_one({'name': data.get('name')}, {'$set': data}, upsert=True)


def main(page):
    index_data = scrape_index(page)  # 通过api接口遍历1-11每页
    for item in index_data.get('results'):
        id = item.get('id')
        detail_data = scrape_detail(id)  # 获取详情页数据,type = dict
        logging.info(detail_data)
        save_data(detail_data)


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGES+1)
    pool.map(main, pages)
    pool.close()
    pool.join()


