import asyncio
import aiohttp
import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s: %(message)s')
INDEX_URL = 'https://cuiqingcai.com/archives/{offset}'
DETAIL_URL = 'https://cuiqingcai.com/archives/{id}'
PAGE_SIZE = 5
PAGE_NUMBER = 100
CONCURRENCY = 5

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None
async def scrape_api(url):
    async with semaphore:
            try:
                    logging.info('scraping %s', url)
                    async with session.get(url) as response:
                            return await response.json()
            except aiohttp.ClientError:
                logging.error('error occurred while scraping %s', url, exc_info=True)