""" Basecode to send static mensages"""
import time
from selenium.common.exceptions import NoSuchElementException

mensagem_boasvindas ="Olá, eu sou o bot da Transurb e estou aqui para auxiliar em sua viagem. " \
               "Por favor, me informe o seu local de origem?"
mensagem_destino = "Para onde gostaria de ir?"

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
        try:
            usuario = driver.find_element_by_class_name('_2FBdJ').text[:-6]
            user = driver.find_element_by_class_name('OUeyt')
            user.click()
            mensagem = driver.find_elements_by_xpath("//div[contains(@class, 'message-in')]")[-1].text
            time.sleep(5)
            user = driver.find_element_by_xpath('//span[@title = "{}"]'.format("Hackathon Unesp"))
            user.click()
            return mensagem, usuario
        except NoSuchElementException:
            pass

def espera_resposta(driver, usuario, mensagem_anterior):
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(usuario))
    user.click()
    mensagem = driver.find_elements_by_xpath("//div[contains(@class, 'message-in')]")[-1].text

    while(mensagem == mensagem_anterior):
        mensagem = driver.find_elements_by_xpath("//div[contains(@class, 'message-in')]")[-1].text
        user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(usuario))
        user.click()

    time.sleep(5)
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format("Hackathon Unesp"))
    user.click()
    return mensagem

def chat_bot_sequence(driver):
    mensagem, usuario = wait_new_message(driver)
    print(usuario)
    send(driver, usuario, mensagem_boasvindas)
    ponto_partida = espera_resposta(driver, usuario, mensagem)
    print(ponto_partida)
    send(driver, usuario, mensagem_destino)
    ponto_destino = espera_resposta(driver, usuario, ponto_partida)
    print(ponto_destino)
    # chama a validacao

