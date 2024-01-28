'''
第一阶段为所有列表页的异步爬取，我们可以将所有的列表页的爬取任务集合起来，
声明为 task 组成的列表，进行异步爬取。

第二阶段则是拿到上一步列表页的所有内容并解析，拿到所有书的 id 信息，
组合为所有详情页的爬取任务集合，声明为 task 组成的列表，进行异步爬取，
同时爬取的结果也以异步的方式存储到 MongoDB 里面。
'''

import asyncio
import aiohttp
import logging
import json
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level = logging.ERROR, 
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 定义MongoDB的连接字符串
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'books10'
MONGO_COLLECTION_NAME = 'books10'

client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

INDEX_URL = 'https://spa5.scrape.center/api/book?limit=18&offset={offset}'
DETAIL_URL = 'https://spa5.scrape.center/api/book/{id}'
PAGE_SIZE = 18
PAGE_NUMBER = 10
CONCURRENCY = 5

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None
timeout_urls = []

'''
程序作用: 爬取指定页面,返回响应的json数据
参数: url (爬取页面地址)
返回值: response.json() (响应的json数据)
'''
async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('scraping %s', url)
            async with session.get(url, timeout=20) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('Error occurred while scraping %s', url, exc_info=True)

'''
程序作用: 爬取列表页,返回列表页面的json数据
参数: page (电影列表页)
返回值: scrape_api函数结果 (电影列表页面的json数据)
results: 是所有 task 返回结果组成的列表
'''
async def scrape_index(page):
    url = INDEX_URL.format(offset = PAGE_SIZE * (page - 1))
    return await scrape_api(url)

'''
程序作用: 保存数据到mongodb
参数: data (数据)
返回值: 无
'''
async def save_data(data):
    logging.info('Save data %s', data)
    if data:
        return await     collection.update_one({
        'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True
    )

'''
程序作用: 获取详情页数据并保存
参数: id (书籍id)
返回值: 无
'''
async def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    try:
        data = await scrape_api(url)
        await save_data(data)
    except asyncio.TimeoutError:
        logging.error('Error occurred while scraping %s', url)
        timeout_urls.append(url)

async def scrape_other(url):
    try:
        data = await scrape_api(url)
        await save_data(data)
    except asyncio.TimeoutError:
        logging.error('Error occurred while scraping %s', url)
        timeout_urls.append(url)

'''
程序作用: 主函数，用来串联调用各个函数
参数: 无
返回值: 无
json.dumps参数说明:
    ensure_ascii=True: 默认输出ASCLL码, 如果把这个该成False, 就可以输出中文
    indent: 参数根据数据格式缩进显示，读起来更加清晰
'''
async def main():
    global session
    session = aiohttp.ClientSession()
    # index tasks
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(page)) for page in range(1, PAGE_NUMBER + 1)]
    results = await asyncio.gather(*scrape_index_tasks)
    # detail tasks
    print('results', results)
    ids = []
    for index_data in results:
        if not index_data: continue
        for item in index_data.get('results'):
            ids.append(item.get('id'))
    scrape_detail_tasks = [asyncio.ensure_future(scrape_detail(id)) for id in ids]
    await asyncio.wait(scrape_detail_tasks)
    scrape_other_tasks = [asyncio.ensure_future(scrape_other(url)) for url in timeout_urls]
    await asyncio.wait(scrape_other_tasks)
    await session.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
