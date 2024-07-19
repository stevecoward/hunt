import asyncio
import logging
import re
from selenium.webdriver.common.by import By
from hunt.utils.webdriver import WebDriver


class CloudflareRadarWebDriver(WebDriver):
    base_url = 'https://radar.cloudflare.com/domains/feedback'
    name = 'cloudflare'
    
    def __init__(self):
        super(CloudflareRadarWebDriver, self).__init__()
    

    async def check(self, target_domain):
        category = 'N/A'
        
        self.driver.get(f'{self.base_url}/{target_domain}')
        
        try:            
            card = self.driver.find_element(By.CLASS_NAME, "radar-card")
            
            pattern = r'is currently categorized as:\n(.+)\nand'
            matches = re.search(pattern, card.text, re.DOTALL)
            
            if matches:
                category = matches.groups()[0]
                category = '|'.join(category.split('\n')) if '\n' in category else category
        except:
            logging.warning(f'error getting category text from radar-card element')

        return {
            'name': self.name,
            'category': category,
        }
