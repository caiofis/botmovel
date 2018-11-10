""" Basecode to send static mensages"""
import time
from selenium.common.exceptions import NoSuchElementException


def send(driver, user, msg):

    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(user))
    user.click()

    msg_box = driver.find_element_by_class_name('_2S1VP')
    msg_box.send_keys(msg)
    button = driver.find_element_by_class_name('_35EW6')
    button.click()

    time.sleep(2)

def wait_new_message(driver):
    while True:
        # Last msg
        try:
            user = driver.find_element_by_class_name('OUeyt')
            user.click()
            read_message(driver)

        except NoSuchElementException:
            pass


def read_message(driver):
    mensagem = driver.find_elements_by_xpath("//div[contains(@class, 'message-in')]")[-1].text[:-6]
    return mensagem