# -*- coding: utf-8 -*-

""" Basecode to send static mensages"""

import time
import unicodedata
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



mensagem_boasvindas ="Olá, eu sou o bot da Transurb e estou aqui para auxiliar em sua viagem. " \
               "Por favor, me informe o seu local de origem?"
mensagem_destino = "Para onde gostaria de ir?"


def send(driver, user, msg):

    '''Busca classe de título dos contatos'''
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(user))
    user.click()

    '''Classe para encontrar o input message para enviar a mensagem ao usuário'''
    msg_box = driver.find_element_by_class_name('_2S1VP')
    msg_box.click()
    msg_box.send_keys(msg)
    msg_box.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//div[@class='_3j7s9' and contains(text, '{}')]/div[@class='OUeyt']".format(user))))


def wait_new_message(driver):
    while True:
        try:
            mensagem_nao_lida = driver.find_element_by_class_name('OUeyt')
            mensagem_nao_lida.click()
            usuario = driver.find_element_by_class_name('_2zCDG').text
            mensagem = driver.find_elements_by_xpath("//div[contains(@class, 'message-in')]")[-1].text

            return mensagem, usuario
        except NoSuchElementException:
            pass


def avaliacao_mensagem(mensagem):
    positivas = ['sim', 'muito', 'obrigada', 'show']

    resp = False
    for positiva in positivas:
        if (positiva in str(normalize(mensagem)).lower()):
            return "Fico feliz em poder ajudar :D"
            resp = True

    if (not resp):
        return "Sinto muito que não pude ajudar. \n" \
               "Que tal falar com a nossa central de atendimento? O número é (14) 4009-1740"


def normalize(string):
    return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore')



if __name__ == "__main__":
    print(avaliacao_mensagem(str(normalize("Ajudou muito"))))
