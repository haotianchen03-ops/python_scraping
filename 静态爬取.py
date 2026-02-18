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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
BASE_URL = 'https://ssr3.scrape.center/'
TOTAL_PAGE = 10


def scrape_page(url):
    # logging.info(f'Scraping {url}')  # 表示你程序正在尝试抓取这个网页，用于追踪程序流程。
    try:
        response = requests.get(url,auth=HTTPBasicAuth('admin','admin'), verify=certifi.where())
        if response.status_code == 200:
            return response.text
        logging.error(f'Failed to scrape {url},invalid status code {response.status_code}')  # 表示错误级别日志，用于输出错误或异常信息

    except requests.exceptions.RequestException as e:
        logging.error(f'error occurred while scraping {url}',exc_info=True)  # exc_info=True 会附带完整的异常 traceback信息，方便调试定位错误


def scrape_index(page):  # 列表页爬取(列表页页码)
    index_url = f'{BASE_URL}/page/{page}'  # 不同页拼接
    return scrape_page(index_url)


def parse_html(html):  # 进入 详情页
    doc = pq(html)
    links = doc('.el-card__body .name')
    for link in links.items():
        href = link.attr('href')
        detail_url = urljoin(BASE_URL, href)
        # logging.info(f'获得 {detail_url}')
        yield detail_url  # 逐页抓取


def scrape_detail(detail_url):  # 爬取详情页，方便以后加功能
    return scrape_page(detail_url)


def parse_detail(detail_url):
    doc = pq(detail_url)
    cover = doc('img.cover').attr('src')  # 获取封面，注意img和cover在同一层，所以img.cover没有空格
    name = doc('a > h2').text()  # 选择a标签内、直接作为子元素 的h2标签,的纯文本
    category = ','.join([item.text() for item in doc('.categories > button > span').items()])
    time = doc('.info:contains(上映)').text()
    match = re.search(r'(\d+-\d+-\d+).*', time)
    time = match.group(1) if match else None  # 没找到就设置为None,否则会自动停止
    drama = doc('.drama p').text()
    score = float(doc('p.score').text())

    return {
        'name': name,
        'category': category,
        'time': time,
        'drama': drama,
        'score': score
    }


client = pymongo.MongoClient('localhost', 27017)
db = client['test']
collection = db['movies']


def save_data(data):
    collection.update_one(
        {'name': data.get('name')},
        {'$set': data},
        upsert=True  # 存在即更新，不存在即插入，防止重名
    )


def main(page, counter):
    index_html = scrape_index(page)  # 获得每个列表页的html
    detail_urls = list(parse_html(index_html))
    counter.append(len(detail_urls))  # 把数量添加到共享列表
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info(f'{data}')
        save_data(data)


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    counter = manager.list()

    pool = multiprocessing.Pool()
    for page in range(1, TOTAL_PAGE + 1):
        pool.apply_async(main, args=(page, counter))
    pool.close()
    pool.join()

    print(f'Total URLs scraped: {sum(counter)}')  # 最终输出总数



