import httpx
import random
from hunt import config


random_ua = lambda: random.choice(config.HTTP_USER_AGENTS)
global_headers = {
    'User-Agent': random_ua(),
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept': 'application/json, text/plain, */*',
}


class RequestData:
    def __init__(self, url):
        self.url = url
        self.async_client = httpx.AsyncClient(headers=global_headers, proxies=config.HTTP_PROXY, verify=False)
        

    def _update_headers(self, header_dict):
        self.async_client.headers.update(header_dict)
