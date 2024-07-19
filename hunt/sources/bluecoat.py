import asyncio
import logging
from selenium.webdriver.common.by import By
from hunt.utils.webdriver import WebDriver


class BluecoatRequestData(WebDriver):
    base_url = 'https://sitereview.bluecoat.com/#/'
    name = 'bluecoat'
    
    def __init__(self):
        super(BluecoatRequestData, self).__init__()
    

    async def check(self, target_domain):
        category = 'N/A'
        
        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, 'txtUrl').send_keys(target_domain)
        self.driver.find_element(By.ID, 'btnLookup').click()
        
        await asyncio.sleep(3)
        
        try:
            category_first = self.driver.find_element(By.XPATH, '//*[@id="submissionForm"]/span/span[1]/div/div[2]/span[1]/span')
            category = category_first.text
        except:
            logging.warning(f'error getting category text from span element')

        return {
            'name': self.name,
            'category': category,
        }
