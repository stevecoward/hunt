import logging
from bs4 import BeautifulSoup
from hunt.utils.requests import RequestData

class CloudflareRadarRequestData(RequestData):
    base_url = 'https://radar.cloudflare.com/domains/feedback'
    name = 'cloudflare'
    
    def __init__(self):
        super(CloudflareRadarRequestData, self).__init__(self.base_url)

    async def check(self, target_domain):
        category = 'N/A'
        self._update_headers({
            'Accept-Language': 'en-US;en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Origin': self.base_url,
            'Referer': self.base_url,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Upgrade-Insecure-Requests': '1',
        })

        response = await self.async_client.get(f'{self.url}/{target_domain}')
        if response.status_code != 200:
            logging.warning(f'got HTTP {response.status_code} response fetching results')
            return category

        content = BeautifulSoup(response.content, 'html.parser')
        card_form = content.find("form", class_="radar-card")
        try:
            ulist = card_form.find("ul", class_="radar-tag-list")
            tags = ulist.find_all("span", class_="radar-tag-label")
            if len(tags) > 1:
                category = '|'.join([tag.text for tag in tags])
            else:
                category = tags[0].text
        except Exception as e:
            logging.warning(f'error getting category text. check classes for HTML parsing')
    
        await self.async_client.aclose()

        return {
            'name': self.name,
            'category': category if not '' else 'N/A',
        }
