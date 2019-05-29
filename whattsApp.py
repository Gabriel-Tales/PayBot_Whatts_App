from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from commands import pdf_to_name, listen, check_messages
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


ff = webdriver.Firefox()



class WhattsApp:
    def __init__(self, web_driver):
        """CN: Class Name"""
        # Navigate Info
        self.driver = web_driver
        self.url = "https://web.whatsapp.com"



z = WhattsApp(ff)


