import re
from hunt.utils.requests import RequestData


class TrendMicroRequestData(RequestData):
    base_url = 'https://global.sitesafety.trendmicro.com'
    intermediary_url = f'{base_url}/lib/idn.php'
    lookup_url = f'{base_url}/result.php'
    name = 'trendmicro'
    
    def __init__(self):
        super(TrendMicroRequestData, self).__init__(self.base_url)

    async def check(self, target_domain):
        category = 'N/A'
        category_class = 'labeltitlesmallresult'
        request_params = {
            'urlname': target_domain,
            'getinfo': 'Check+Now'
        }
        
        # get / first
        response = await self.async_client.get(self.url)
        if response.status_code != 200:
            return category
        
        # get intermediary request
        response = await self.async_client.post(self.intermediary_url, data={
            'url': target_domain
        })
        
        # get result request
        response = await self.async_client.post(self.lookup_url, data=request_params)

        if response.status_code == 200:
            category_tmp = ''
            for element_class in [category_class]:
                pattern = re.compile(f'(<div class="{element_class}">)(.+)(<\/div>)')
                search = pattern.search(response.text).groups()
                if element_class == category_class:
                    category_tmp = search[1] if search else 'Bad Match'
            category = category_tmp
        
        return {
            'name': self.name,
            'category': category,
        }
