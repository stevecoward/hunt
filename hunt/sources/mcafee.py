import logging
from bs4 import BeautifulSoup
from hunt.utils.requests import RequestData

class McAfeeRequestData(RequestData):
    base_url = 'https://sitelookup.mcafee.com'
    lookup_url = f'{base_url}/en/feedback/url'
    name = 'mcafee'
    
    def __init__(self):
        super(McAfeeRequestData, self).__init__(self.base_url)

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

        response = await self.async_client.get(self.url)
        if response.status_code != 200:
            logging.warning(f'got HTTP {response.status_code} response fetching base URL')
            return category

        content = BeautifulSoup(response.content, 'html.parser')
        input_sid = content.find('input', {'name': 'sid'}).get('value')
        input_e = content.find('input', {'name': 'e'}).get('value')
        input_c = content.find('input', {'name': 'c'}).get('value')
        input_p = content.find('input', {'name': 'p'}).get('value')

        # the None tuples are necessary for the multipart-form data type post request
        request_params = {
            'sid': (None, input_sid),
            'e': (None, input_e),
            'c': (None, input_c),
            'p': (None, input_p),
            'action': (None, 'checksingle'),
            'url': (None, target_domain),
        }
        
        response = await self.async_client.post(self.lookup_url, files=request_params)
        if response.status_code != 200:
            logging.warning(f'got HTTP {response.status_code} response fetching results')
            return category

        content = BeautifulSoup(response.content, 'html.parser')
        result_table = content.find('table', {'class': 'result-table'})

        category_cells = result_table.find_all('td', {'nowrap': 'nowrap'})
        # only interested in the last two elements
        parsed_cells_first_pass = [cell.text.replace('-', '').strip() for cell in category_cells][2:]
        parsed_cells = [list(filter(None, [text_value.strip() for text_value in cell.split('\n')])) for cell in parsed_cells_first_pass]
        final_result = [', '.join(cell) for cell in parsed_cells]
        category = f'{[x for x in final_result if x != ""][0]}'
        
        await self.async_client.aclose()

        return {
            'name': self.name,
            'category': category if not '' else 'N/A',
        }
