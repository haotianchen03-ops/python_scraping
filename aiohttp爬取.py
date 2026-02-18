import asyncio
import aiohttp
import logging
import json

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
INDEX_URL = 'https://spa5.scrape.center/api/book/?limit=18&offset={offset}'
DETAIL_URL = 'https://spa5.scrape.center/api/book/{book_id}'
TOTAL_PAGE = 10
PAGE_SIZE = 18
CONCURRENCY = 10
semaphore = asyncio.Semaphore(CONCURRENCY)
timeout = aiohttp.ClientTimeout(total=10)


async def scrape_api(session: aiohttp.ClientSession, url):  # 爬取page页
    async with semaphore:
        try:
            async with session.get(url) as response:
                return await response.json()

        except aiohttp.ClientError:
            logging.error(f'Error while scraping {url}',exc_info=True)


async def scrape_index(session: aiohttp.ClientSession, page):
    url = INDEX_URL.format(offset=PAGE_SIZE*(page-1))
    return await scrape_api(session, url)

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('mongodb://localhost:27017/')  # 建立异步客户端
db = client['test']
collection = db['books']


async def save_data(data):
    if data:
        return await collection.update_one({'id': data.get('id')}, {'$set': data}, upsert=True)


async def scrape_detail(session: aiohttp.ClientSession, book_id):
    url = DETAIL_URL.format(book_id=book_id)
    data = await scrape_api(session, url)
    await save_data(data)


async def main():
    ids = []
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [asyncio.create_task(scrape_index(session,page)) for page in range(1,TOTAL_PAGE+1)]
        results = await asyncio.gather(*tasks)
        for index_data in results:
            for item in index_data.get('results'):
                ids.append(item.get('id'))

        scrape_detail_tasks = [asyncio.create_task(scrape_detail(session, id)) for id in ids]
        await asyncio.gather(*scrape_detail_tasks)
        logging.info(json.dumps(results,ensure_ascii=False,indent=4))


if __name__ == '__main__':
    asyncio.run(main())




