import requests
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

BASE_URL = 'https://login2.scrape.center'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

browser = webdriver.Chrome()
browser.get(LOGIN_URL)
browser.find_element(By.XPATH, '//input[@type="text"]').send_keys(USERNAME)
browser.find_element(By.XPATH, '//input[@type="password"]').send_keys(PASSWORD)
browser.find_element(By.XPATH, '//input[@type="submit"]').click()
time.sleep(4)

cookies = browser.get_cookies()
browser.close()

session = requests.Session()

for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

response = session.get(INDEX_URL)

print(response.text)

