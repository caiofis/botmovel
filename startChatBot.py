from lib_chat import send, wait_new_message, chat_bot_sequence
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Firefox()
driver.get('https://web.whatsapp.com/')

login = False
i=0

input('Por favor, faça o login do whatsapp web pelo QRCode e dê enter!')
while (not login and i < 3):
    try:
        driver.find_element_by_class_name("iHhHL")
        login = True
    except NoSuchElementException:
        i+=1

'''if (not login):
    print("Desculpe, não foi possível fazer o login")
else:'''
#send(driver, 'Hackathon Unesp', 'Batata')
while (True):
    chat_bot_sequence(driver)

