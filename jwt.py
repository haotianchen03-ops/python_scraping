import requests
from urllib.parse import urljoin


BASE_URL = 'https://login3.scrape.center'
LOGIN_URL = urljoin(BASE_URL, '/api/login')
INDEX_URL = urljoin(BASE_URL, 'api/book')
USERNAME = 'admin'
PASSWORD = 'admin'

response_login = requests.post(LOGIN_URL, json={
    'username': USERNAME,
    'password': PASSWORD,
})

data = response_login.json()
jwt = data['token']
headers = {'Authorization': f'jwt {jwt}'}

response_index = requests.get(INDEX_URL, headers=headers, params={'limit':18,'offset':0})
print(response_index.json())