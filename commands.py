from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import re
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def pdf_to_name():
    pages = convert_from_path(r"vencidos 18.05.pdf")
    page_pdf = []
    for i, page in enumerate(pages):
        page.save(f'vencidos{i}.jpg')
        page_pdf.append(pytesseract.image_to_string(Image.open(f"vencidos{i}.jpg")))
        subprocess.run(["rm", f"vencidos{i}.jpg"])

    text = '\n'.join(page_pdf)

    text_list = re.findall(r"\n[A-Z]{2,}\s[A-Z\s.]{2,}[A-Z]+", text)
    name_list = []

    for text in text_list:
        for name in text.split('\n'):
            if len(name.split()) > 1:
                if name[-1] == '.':
                    name_list.append(name[:-1])
                else:
                    name_list.append(name)

    return name_list


def listen(bot, group):
    if bot.check_new_message(group):
        bot.wait(4)
        bot.send_message("Teste concluido", group)
        bot.driver.execute_script("document.getElementsByClassName('message-in')[0].click()")


def check_messages(message, bot):
    bot.send_message(message, )








