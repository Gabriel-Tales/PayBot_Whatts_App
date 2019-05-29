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
        # Side-Menu
        self.XPATH_contact = "/html/body/div[1]/div/div/div[3]/div/div[2]/div/div/div/div[]"
        self.CN_lblSearch = "jN-F5"
        self.CN_btnSearch = "C28xL"
        self.XPATH_btnMenu = "/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/div"
        self.CN_menuItems = "_3L0q3"
        # Message-Side
        self.CN_lblMessage = "_2S1VP"
        self.CN_btnSend = "_35EW6"
        self.XPATH_Op = "/html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[3]/div"
        self.CN_btnSettings = "rAUz7"
        self.CN_settings = "_3L0q3"
        self.CN_confL = "_1WZqU"

    def wait(self, time=0):
        sleep(time)

    def navigate(self):  # OK
        self.driver.get(self.url)

    def check_new_message(self, filters=None):   # OK
        contacts = self.driver.find_elements_by_xpath(self.XPATH_contact)
        find = False
        for contact in contacts:
            contact_info = contact.text.split('\n')
            if filters :
                if filters.upper() in contact_info[0].upper():
                    if re.search(r"^[\d]{1,3}$",contact.text.split('\n')[-1] ):
                        print(f"Nova Mensagem de {contact_info[0]}")
                        return True
            else:
                if re.search(r"^[\d]{1,3}$", contact.text.split('\n')[-1]):
                    print(f"Nova Mensagem de {contact_info[0]}")
                    find = True
        return find

    def check_my_message(self, filter, bot):
        self.find_contact(filter)
        my_messages = self.driver.find_elements_by_class_name("message-out")
        check_messages(my_messages[len(my_messages)-1], bot)

    def find_contact(self, contact_name):   # OK
        ok = ''

        lbl = self.driver.find_element_by_class_name(self.CN_lblSearch)
        lbl.send_keys(contact_name)
        try:
            contacts_find = self.driver.find_elements_by_class_name(self.CN_contact)
            for contact in contacts_find:
                if contact_name.upper() == contact.text.split('\n')[0].upper():
                    contact.click()
                    self.driver.find_element_by_class_name(self.CN_btnSearch)
                    ok = 1
                    break

        except Exception as e:
            print(e)
            pass
        lbl.clear()
        return ok

    def send_message(self, message, contact_name=None):    # OK
        btn_Send = None
        if contact_name:
            self.find_contact(contact_name)
        self.driver.find_element_by_class_name(self.CN_lblMessage).send_keys(message)
        try:
            btn_Send = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, self.CN_btnSend)))
        finally:
            if btn_Send:
                btn_Send.click()

    def cobrar(self):
        list_name = pdf_to_name()
        for name in list_name:
            if self.find_contact(name):
                self.send_message("Ta devendo", name)

    #def bot(self, bot):
            #listen(bot)



    def quit(self):   # OK
        self.driver.find_element(By.XPATH, self.XPATH_btnMenu).click()
        menu_list = self.driver.find_elements_by_class_name(self.CN_menuItems)
        for menu_item in menu_list:
            if "SAIR" in menu_item.text.upper():
                menu_item.click()
        self.wait(6)
        self.driver.quit()
        exit()


z = WhattsApp(ff)
z.navigate()

