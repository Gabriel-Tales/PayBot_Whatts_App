from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from commands import pdf_to_name, listen, check_messages
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains



#ff = webdriver.Firefox()


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
        self.XPATH_btnListSettings = "/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li"
        self.XPATH_contact_name = "/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]"
        self.XPATH_groupContacts = "/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div/div[2]/div/div/div/div"
        self.XPATH_btnGroupConf = "/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div/span/div"
        self.XPATH_lblGroupName = "/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div/div[2]/div/div[2]/div/div[2]"
        self.XPATH_btnCreateGroupConf = "/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div/span/div/div"
        self.XPATH_btnDataGroup = "/html/body/div[1]/div/div/div[4]/div/header/div[2]"
        self.XPATH_divDataGroup = "/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div"
        self.XPATH_btnContactGroup = "/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div/div[5]/div[4]/div/div[2]"
        self.XPATH_btnDeleteContactGroup = "/html/body/div[1]/div/span[4]/div/ul/li[2]/div"
        self.XPATH_btnDeleteConfirm = "/html/body/div[1]/div/span[2]/div/div/div/div/div/div/div[2]/div[2]"
        self.CN_messages = "message-out"

        self.last_messages = ""

    def navigate(self):
        self.driver.get(self.url)

    def find_contacts(self, contact_name):
        """ Fill the search with contact_name label and return if contact was found or no"""
        contact_now = ""
        try:
            contact_now = self.driver.find_element_by_xpath(self.XPATH_contact_name).text
        except NoSuchElementException:
            pass
        if contact_now.upper() != contact_name.upper():
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
        else:
            return True

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
                self.driver.find_element_by_xpath(self.XPATH_btnSend).click()

    def cobrar(self):
        """ Special method. work with Debt pdf of Santander, that read the pdf and find names,
        then return a list_name and send a pattern message to contact with name in list"""
        name_list = pdf_to_name("../zipzop/vencidos 18.05.pdf")
        for name in name_list:
            self.send_message("Ta devendo", name)

    def commands(self, bot, group="comandos"):
        if not self.find_contacts(group):
            print("grupo nao encontrado")
            self.driver.find_elements_by_xpath(self.XPATH_btnAllSettings)[0].click()
            self.driver.find_elements_by_xpath(self.XPATH_btnListSettings)[0].click()
            contacts = self.driver.find_elements_by_xpath(self.XPATH_groupContacts) #Contatos para grupo
            for contact in contacts:
                if len(contact.text.split("\n")) > 1:
                    contact.click()
                    break
            self.driver.find_element_by_xpath(self.XPATH_btnGroupConf).click() # Confirma contato adicionado
            self.driver.find_element_by_xpath(self.XPATH_lblGroupName).send_keys(group) # Define nome do grupo
            self.driver.find_element_by_xpath(self.XPATH_btnCreateGroupConf).click() # Confirmar
            self.wait(2)
            self.driver.find_element_by_xpath(self.XPATH_btnDataGroup).click()
            css_class = ".".join(self.driver.find_elements_by_xpath(self.XPATH_divDataGroup)[0].get_attribute("class").split())
            self.wait(3)
            self.driver.execute_script(f"document.querySelector('.{css_class}').scrollBy(0,1000)")
            self.wait(3)
            hover = ActionChains(self.driver)
            hover.context_click(self.driver.find_elements_by_xpath(self.XPATH_btnContactGroup)[0])
            hover.perform()
            self.driver.find_element_by_xpath(self.XPATH_btnDeleteContactGroup).click()
            self.driver.find_element_by_xpath(self.XPATH_btnDeleteConfirm).click()

        if not self.last_messages:
            self.last_messages = []
            messages_now = self.driver.find_elements_by_class_name(self.CN_messages)
        else:
            messages_now = self.driver.find_elements_by_class_name(self.CN_messages)

        if len(messages_now) > len(self.last_messages):
            if "BOT:" not in messages_now[-1].text.split("\n")[0].upper():
                message_input = messages_now[-1].text.split("\n")[0]
                return check_messages(message_input, bot)
        return True

    def wait(self, seconds):
        sleep(seconds)

    def quit(self):
        """ Close session with web Whatts'App, quit the web driver and quit the Python"""
        self.driver.find_elements_by_xpath(self.XPATH_btnAllSettings)[0].click()
        self.driver.find_elements_by_xpath(self.XPATH_btnListSettings)[5].click()
        self.driver.quit()
        exit()


#z = WhattsApp(ff)
#z.navigate()


