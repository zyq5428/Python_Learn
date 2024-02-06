import requests  # 用于爬取数据
import logging   # 用于日志
import re        # 用于正则表达式
import pymongo   # 用于连接MongoDB数据库
from pyquery import PyQuery as pq   # 用于解析HTML源代码
from urllib.parse import urljoin    # 用于拼接url

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s') # 设置日志输出格式
                    
# 定义MongoDB的连接字符串
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017' # 连接字符串
MONGO_DB_NAME = 'movies0120' # 数据库名称
MONGO_COLLECTION_NAME = 'movies0120'  # 集合名称

client = pymongo.MongoClient(MONGO_CONNECTION_STRING) # 连接MongoDB
db = client[MONGO_DB_NAME]    # 获得数据库
collection = db[MONGO_COLLECTION_NAME] # 获得数据库的集合

BASE_URL = 'https://ssr1.scrape.center' #基础网址
TOTAL_PAGE = 10                           # 总页数

'''
程序作用: 爬取指定页面，返回页面文本
参数: url (爬取页面地址)
返回值: response.text (页面文本)
'''
def scrape_page(url):   # 定义函数为scrape_page
    # url = 'https://ssr1.scrape.center/page/1' 
    logging.info('scraping %s', url)  # 以info级别的日志信息输出这个“url"网址  
    # xxx(xxx, xxx); xxx(xxx) scraping https://ssr1.scrape.center/page/1
    try: # 异常处理 try 和 except
        response = requests.get(url)    # 爬取 请求网址响应
        if response.status_code == 200: # 状态码为200时返回页面文本 
            return response.text        # 返回页面文本 
        logging.info('get invalid status code %s while scraping %s', response.status_code, url)
        # 以info级别的日志信息输出 “获取无效状态代码  或者 解析失败   url= https://ssr1.scrape.center/page/1”
    except requests.RequestException:    # 如果请求异常 
        logging.error('error occurred while scraping %s', url, exc_info=True) 
        # 以error级别的日志信息输出 “请求异常  url= https://ssr1.scrape.center/page/1”

'''
程序作用: 爬取电影列表页，返回列表页面的文本
参数: page (电影列表页)
返回值: scrape_page函数结果 (电影列表页面的文本)
'''
def scrape_index(page):        # 定义函数为scrape_index
    index_url = f'{BASE_URL}/page/{page}' # 拼接电影列表页网址 ## index_url 索引网址 = 'https://ssr1.scrape.center/page/1'
    return scrape_page(index_url)           # 返回列表页面的文本

'''
程序作用: 解析电影列表页，返回每部电影的详情页网址   
参数: html (电影列表页面的文本)  
返回值: detail_url (电影详情页网址) 
'''
def parse_index(html):  #  定义函数parse_index    html = index_html 该网址的源代码 
    doc = pq(html)       # 将源代码初始化为PyQuery对象 
    links = doc('.el-card .name')   # 选择器
    detail_urls = []      # 电影详情页网址 以列表形式存储
    for link in links.items(): # 遍历每个电影
        href = link.attr('href') # 获取电影详情页网址 attr为内置函数
        detail_url = urljoin(BASE_URL, href) # 以BASE_URL为基础拼接，输出电影详情页网址
        # https://ssr1.scrape.center/detail/1
        logging.info('get detail url %s', detail_url) # 以info级别的日志信息输出这个电影详情页网址 
        detail_urls.append(detail_url)                # 电影详情页网址 以列表形式存储
    return detail_urls                                # 返回电影详情页网址

'''
程序作用: 爬取电影详情页，返回详情页面的文本
参数: url (电影详情页网址)
返回值: scrape_page函数结果 (电影详情页面的文本)
'''
def scrape_detail(url):        # 定义函数为scrape_detail
    return scrape_page(url)    # 返回详情页面的文本

'''
程序作用: 解析电影列表页，返回每部电影的详情页网址
参数: html (电影列表页面的文本)
返回值: detail_url (电影详情页网址)
'''
def parse_detail(html):            # 定义函数为parse_detail
    doc = pq(html)                 # 将源代码初始化为PyQuery对象
    cover = doc('img.cover').attr('src') # 获取电影封面网址
    name = doc('a > h2').text()          # 获取电影名称
    categories = [item.text() for item in doc('.categories button span').items()] # 获取电影类别
    published_at = doc('.info:contains(上映)').text()                             # 获取电影上映时间
    published_at = re.search(r'\d{4}-\d{2}-\d{2}', published_at).group(0) \      
        if published_at and re.search(r'\d{4}-\d{2}-\d{2}', published_at) else None # 获取电影上映时间
    drama = doc('.drama p').text()                                                  # 获取电影简介
    score = doc('.score').text()                                                    # 获取电影评分
    score = float(score) if score else None                                         # 获取电影评分
    return {                                                                        # 返回电影详情数据
        'cover': cover,           #封面
        'name': name,             #名称
        'categories': categories, #类别
        'published_at': published_at, #上映时间
        'drama': drama,               #简介
        'score': score                #评分
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



'''
程序作用: 保存数据到mongodb
参数: data (电影详情数据)
返回值: 无
'''
def save_data(data):    # 定义函数为save_data
    collection.update_one({  # 更新或插入数据
        'name': data.get('name')  # 名称
        }, {                      # 数据
            '$set': data          
        }, upsert=True            
    )

'''
程序作用: 主函数，用来串联调用各个函数
参数: 无
返回值: 无
'''
def main():                                      # 定义函数为main
    for page in range(1, TOTAL_PAGE + 1):        # page第一次遍历的结果 1，依次加1，最后结果为TOTAL_PAGE总页数
        index_html = scrape_index(page)          # scrape_index:爬取电影列表页，索引网址
        detail_urls = parse_index(index_html)  # https://ssr1.scrape.center/detail/1 # parse_index:解析电影列表页
        for detail_url in detail_urls:          # https://ssr1.scrape.center/detail/1  第一次遍历的结果
            detail_html = scrape_detail(detail_url)  # scrape_detail:爬取电影详情页 
            data = parse_detail(detail_html)         # parse_detail:解析电影详情页
            save_data(data)
            logging.info('saved data successfully, data is: %s', data) # 以info级别的日志信息输出保存数据成功，数据为data

if __name__ == '__main__':  # 当文件被直接运行时 __name__ = __main__ 就直接运行main()
    main()