import requests
import logging
import re
import pymongo
from pyquery import PyQuery as pq
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')

BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10

'''
程序作用: 爬取指定页面，返回页面文本
参数: url (爬取页面地址)
返回值: response.text (页面文本)
'''
def scrape_page(url):   # url = 'https://ssr1.scrape.center/page/1'
    logging.info('scraping %s', url) # xxx(xxx, xxx); xxx(xxx) scraping https://ssr1.scrape.center/page/1
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.info('get invalid status code %s while scraping %s', 
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

'''
程序作用: 爬取电影列表页，返回列表页面的文本
参数: page (电影列表页)
返回值: scrape_page函数结果 (电影列表页面的文本)
'''
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}' # index_url = 'https://ssr1.scrape.center/page/1'
    return scrape_page(index_url)

'''
程序作用: 解析电影列表页，返回每部电影的详情页网址
参数: html (电影列表页面的文本)
返回值: detail_url (电影详情页网址)
'''
def parse_index(html):  # html = index_html 该网址的源代码
    doc = pq(html)
    links = doc('.el-card .name')
    detail_urls = []
    for link in links.items():
        href = link.attr('href')
        detail_url = urljoin(BASE_URL, href)  # https://ssr1.scrape.center/detail/1
        logging.info('get detail url %s', detail_url)
        detail_urls.append(detail_url)
    return detail_urls

'''
程序作用: 爬取电影详情页，返回详情页面的文本
参数: url (电影详情页网址)
返回值: scrape_page函数结果 (电影详情页面的文本)
'''
def scrape_detail(url):
    return scrape_page(url)

'''
程序作用: 解析电影列表页，返回每部电影的详情页网址
参数: html (电影列表页面的文本)
返回值: detail_url (电影详情页网址)
'''
def parse_detail(html):
    doc = pq(html)   # 将源代码初始化为PyQuery对象
    cover = doc('img.cover').attr('src')
    name = doc('a > h2').text()
    categories = [item.text() for item in doc('.categories button span').items()]
    published_at = doc('.info:contains(上映)').text()
    published_at = re.search(r'\d{4}-\d{2}-\d{2}', published_at).group(0) \
        if published_at and re.search(r'\d{4}-\d{2}-\d{2}', published_at) else None
    drama = doc('.drama p').text()
    score = doc('.score').text()
    score = float(score) if score else None
    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }

'''
注意：
(1)
categories = [item.text() for item in doc('.categories button span').items()]
等价于
categories = []
for item in doc('.categories button span').items():
    categories.append(item.text())
    
(2)
published_at = re.search(r'\d{4}-\d{2}-\d{2}', published_at).group(0) \
    if published_at and re.search(r'\d{4}-\d{2}-\d{2}', published_at) else None
等价于
if published_at and re.search(r'\d{4}-\d{2}-\d{2}', published_at):
    published_at = re.search(r'\d{4}-\d{2}-\d{2}', published_at).group(0)
else:
    None
'''

# 定义MongoDB的连接字符串
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'movies0120'
MONGO_COLLECTION_NAME = 'movies0120'

client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

'''
程序作用: 保存数据到mongodb
参数: data (电影详情数据)
返回值: 无
'''
def save_data(data):
    collection.update_one({
        'name': data.get('name')
        }, {
            '$set': data
        }, upsert=True
    )

'''
程序作用: 主函数，用来串联调用各个函数
参数: 无
返回值: 无
'''
def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)  # https://ssr1.scrape.center/detail/1
        for detail_url in detail_urls:          # https://ssr1.scrape.center/detail/1  第一次遍历的结果
            detail_html = scrape_detail(detail_url)  # scrape_detail:爬取电影详情页 
            data = parse_detail(detail_html)
            save_data(data)
            logging.info('saved data successfully, data is: %s', data)

if __name__ == '__main__':
    main()