import base64
from hunt.utils.requests import RequestData


class IbmXforceRequestData(RequestData):
    url = 'https://api.xforce.ibmcloud.com/api/url/{target_domain}'
    name = 'ibm-xforce'
    
    def __init__(self, api_key, api_secret):
        super(IbmXforceRequestData, self).__init__(self.url)
        auth_string = f'{api_key}:{api_secret}'
        encoded_authentication = f'Basic {base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")}'
        self._update_headers({'Authorization': encoded_authentication})

    async def check(self, target_domain):
        category = 'N/A'
        self.url = self.url.format(target_domain=target_domain)
        
        response = await self.async_client.get(self.url, timeout=20)
        if response.status_code != 200:
            return {
                'name': self.name,
                'category': category,
            }
        
        response_json = response.json()
        category = [item for item in response_json['result']['cats']][0]
        score = response_json['result']['score']
        category = f'{category} (Score: {score})'
        
        return {
            'name': self.name,
            'category': category,
        }
