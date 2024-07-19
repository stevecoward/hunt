import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from hunt import config

class WebDriver:
    def __init__(self):
        service = Service(config.CHROMEDRIVER_PATH)
        
        if os.name == 'nt':
            self.driver = webdriver.Chrome(service=service)
        else:
            self.driver = webdriver.Chrome()