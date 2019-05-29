from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.common.exceptions import NoSuchElementException
from commands import pdf_to_name, listen, check_messages
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


ff = webdriver.Firefox()



class WhattsApp:
    """Page Object of Web Whatts'App"""
    def __init__(self, web_driver):
        """CN: Class Name"""
        # Navigate Info
        self.driver = web_driver
        self.url = "https://web.whatsapp.com"
        # xpath
        self.XPATH_btnSettings = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/button"
        self.XPATH_lblSearch = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/input"
        self.XPATH_contact = "/html/body/div[1]/div/div/div[3]/div/div[2]/div/div/div/div"
        self.XPATH_lblMessage = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]"
        self.XPATH_btnSend = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button"
        self.XPATH_btnAllSettings = "/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]"
        self.XPATH_btnRm = "/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[6]"

    def navigate(self):
        self.driver.get(self.url)

    def find_contacts(self, contact_name):
        """ Fill the search with contact_name label and return if contact was found or no"""
        self.driver.find_element_by_xpath(self.XPATH_btnSettings).click()
        self.driver.find_element_by_xpath(self.XPATH_lblSearch).send_keys(
            contact_name)
        self.wait(1)
        find = False
        contacts = ''
        try:
            contacts = self.driver.find_elements_by_xpath(self.XPATH_contact)
        except NoSuchElementException:
            pass
        if contacts:
            for contact in contacts:
                if contact.text.split("\n")[0].upper() == contact_name.upper():
                    contact.click()
                    find = True
            self.driver.find_element_by_xpath(self.XPATH_lblSearch).clear()
        return find

    def send_message(self, message, contact_name=None):
        """ Fill the label message and click in send Button"""
        if contact_name:
            if self.find_contacts(contact_name):
                pass
            else:
                return
        try:
            lbl = self.driver.find_element_by_xpath(self.XPATH_lblMessage)
        except NoSuchElementException:
            pass
        else:
            lbl.clear()
            try:
                lbl.send_keys(message)
            except NoSuchElementException:
                pass
            else:
                z.driver.find_element_by_xpath(self.XPATH_btnSend).click()

    def cobrar(self):
        """ Special method. work with Debt pdf of Santander, that read the pdf and find names,
        then return a list_name and send a pattern message to contact with name in list"""
        name_list = pdf_to_name("../zipzop/vencidos 18.05.pdf")
        for name in name_list:
            self.send_message("Ta devendo", name)

    def wait(self, seconds):
        sleep(seconds)

    def quit(self):
        """ Close session with web Whatts'App, quit the web driver and quit the Python"""
        self.driver.find_elements_by_xpath(self.XPATH_btnAllSettings)[0].click()
        self.driver.find_element_by_xpath(self.XPATH_btnRm).click()
        self.driver.quit()
        exit()


z = WhattsApp(ff)
z.navigate()


