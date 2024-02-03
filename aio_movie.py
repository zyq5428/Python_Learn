import asyncio
import aiohttp
import logging
import json
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level = logging.ERROR, 
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 定义MongoDB的连接字符串
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'movie'
MONGO_COLLECTION_NAME = 'movie'

client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10

