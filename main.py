from whattsApp import WhattsApp
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

ff = webdriver.Firefox()

bot = WhattsApp(ff)
bot.navigate()
test = ""
while not test:
    try:
        test = bot.driver.find_element_by_xpath(bot.XPATH_contact)
    except NoSuchElementException:
        pass
bot.wait(3)

while bot.commands(bot):
    continue
