import requests
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOTAL_NUMBER = 100
BASE_URL = 'https://ssr4.scrape.center/detail/{id}'

start_time = time.time()

for id in range(1, TOTAL_NUMBER + 1):
    url = BASE_URL.format(id=id) # 'https://ssr4.scrape.center/detail/1'
    logging.info('scraping %s', url)
    response = requests.get(url)

end_time = time.time()

logging.info('Total time %s sconds', end_time - start_time)
