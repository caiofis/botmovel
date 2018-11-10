""" Basecode to reply static mensages"""


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Firefox()
driver.get('https://web.whatsapp.com/')

#name = input('Enter the name of user or group : ')
#msg = input('Enter your message : ')
#count = int(input('Enter the count : '))
msg = "Oi"

def sendMsg(user,msg,count):
    user.click()
    msg_box = driver.find_element_by_class_name('_2S1VP')

    for i in range(count):
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_35EW6')
        button.click()
    time.sleep(2)

input('Enter anything after scanning QR code')

while True:
    # Last msg
    try:
        user = driver.find_element_by_class_name('OUeyt')
        sendMsg(user, msg, 1)

    except NoSuchElementException:
        print("No msg")

#user.click()

# msg_box = driver.find_element_by_class_name('_2S1VP')
#
# for i in range(count):
#     msg_box.send_keys(msg)
#     button = driver.find_element_by_class_name('_35EW6')
#     button.click()
