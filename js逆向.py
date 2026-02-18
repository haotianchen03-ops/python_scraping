import hashlib
import time
import requests
import base64
import json
from typing import Any,List


INDEX_URL = 'https://spa6.scrape.center/api/movie/?limit={limit}&offset={offset}&token={token}'
LIMIT = 10
OFFSET = 0


def get_token(args: List[Any]):
    timestamp = str(int(time.time()))          # 第2步：获取时间戳
    args.append(timestamp)                     # 压入列表
    
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    # 第3步 + 第4步：用分号拼接后做 SHA1 哈希，得到 sign
    
    return base64.b64encode(','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')


# 构造参数并生成 token
args = ['/api/movie']
token = get_token(args=args)

# 拼接请求 URL
index_url = INDEX_URL.format(limit=LIMIT, offset=OFFSET, token=token)

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 发请求
response = requests.get(index_url, verify=False)
result = response.json()


DETAIL_URL = 'https://spa6.scrape.center/api/movie/{id}?token={token}'
SCRERT = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb1'


for item in result.get('results'):
    id = item.get('id')
    encrypt_id = base64.b64encode((str(id)+SCRERT).encode('utf-8')).decode('utf-8')
    args = [f'/api/movie/{encrypt_id}']
    detail_token = get_token(args=args)
    detail_url = DETAIL_URL.format(id=encrypt_id, token=detail_token)
    response = requests.get(detail_url, verify=False)
    result = response.json()

    to_remove = {'cover', 'photos'}
    result = {k: v for k, v in result.items() if k not in to_remove}
    print(json.dumps(result, indent=4, ensure_ascii=False))
    









