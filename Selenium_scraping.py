from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from selenium import webdriver
import logging
import pymongo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
INDEX_URL = 'https://spa2.scrape.center/page/{page}'
TOTAL_PAGE = 10


option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=option)
browser.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument',
    {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    }
)
wait = WebDriverWait(browser, 7)


def scrape_page(url, condition, locator):
    try:
        browser.get(url)
        wait.until(condition(locator))

    except TimeoutException:
        logging.error(f'TimeoutException while scraping {url}', exc_info=True)


def scrape_index(page):  # 进入不同页
    url = INDEX_URL.format(page=page)
    #  所有节点加载成功
    scrape_page(url, condition=EC.presence_of_all_elements_located,
                locator=(By.CSS_SELECTOR, 'a.name'))


detail_url = 'https://spa2.scrape.center/detail/'


def parse_index():  # 拼接出详情页的url
    elements = browser.find_elements(By.CSS_SELECTOR, 'a.name')
    for element in elements:
        href = element.get_attribute('href')
        yield urljoin(detail_url, href)


def scrape_detail(url):  # 进入详情页
    scrape_page(url, condition=EC.presence_of_element_located, locator=(By.TAG_NAME, 'h2'))


def parse_detail():  # 获取详情页的信息
    url = browser.current_url
    name = browser.find_element(By.CSS_SELECTOR, 'h2.m-b-sm').text
    category = ','.join(element.text for element in browser.find_elements(By.CSS_SELECTOR,
                                                                        '.categories button span'))
    info = browser.find_elements(By.CSS_SELECTOR, '.m-v-sm.info')
    region = info[0].find_elements(By.TAG_NAME, 'span')[0].text
    duration = info[0].find_elements(By.TAG_NAME, 'span')[2].text
    date = info[1].find_element(By.TAG_NAME,'span').text.split()[0]
    drama = browser.find_element(By.CSS_SELECTOR, '.drama p').text

    return{
        'url': url,
        'name': name,
        'category': category,
        'region': region,
        'duration': duration,
        'date': date,
        'drama': drama
    }


client = pymongo.MongoClient('localhost', 27017)
db = client['test']
collection = db['Selenium']


def save_data(data):
    collection.update_one({'name': data.get('name')}, {'$set': data}, upsert=True)


def main():
    try:
        for page in range(1, TOTAL_PAGE + 1):
            scrape_index(page)
            detail_urls = parse_index()
            for url in list(detail_urls):
                scrape_detail(url)
                logging.info(parse_detail())
                save_data(parse_detail())

    finally:
        browser.close()


if __name__ == '__main__':
    main()

