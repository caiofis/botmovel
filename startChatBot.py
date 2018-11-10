from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Firefox()
driver.get('https://web.whatsapp.com/')

login = False
i=0
while (not login and i < 3):
    input('Por favor, faça o login do whatsapp web pelo QRCode e dê enter!')
    try:
        driver.find_element_by_xpath('//span[@title = "{}"]')
        login = True
    except NoSuchElementException:
        i+=1
        print(i)

if (not login):
    print("Desculpe, não foi possível fazer o login")
else:
    print('Batatas')