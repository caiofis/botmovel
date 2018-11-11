# -*- coding: utf-8 -*-

""" Basecode to send static mensages"""
import time
import unicodedata
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from utils.google_api_utils import GoogleApiUtils

mensagem_boasvindas ="Olá, eu sou o bot da Transurb e estou aqui para auxiliar em sua viagem. " \
               "Por favor, me informe o seu local de origem?"
mensagem_destino = "Para onde gostaria de ir?"


def send(driver, user, msg):

    '''Busca classe de título dos contatos'''
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(user))
    user.click()

    '''Classe para encontrar o input message para enviar a mensagem ao usuário'''
    msg_box = driver.find_element_by_class_name('_2S1VP')
    msg_box.send_keys(msg)
    msg_box.send_keys(Keys.RETURN)
    #button = driver.find_element_by_class_name('_35EW6')
    #button.click()

def wait_new_message(driver):
    while True:
        try:
            mensagem_nao_lida = driver.find_element_by_class_name('OUeyt')
            mensagem_nao_lida.click()
            usuario = driver.find_element_by_class_name('_2zCDG').text
            mensagem = driver.find_elements_by_xpath("//div[contains(@class, 'message-in')]")[-1].text
            user = driver.find_element_by_xpath('//span[@title = "{}"]'.format("Hackathon Unesp"))
            user.click()
            return mensagem, usuario
        except NoSuchElementException:
            pass

def espera_resposta(driver, usuario, mensagem_anterior):
    '''user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(usuario))
    user.click()
    mensagem = driver.find_elements_by_xpath("//div[contains(@class, 'message-in')]")[-1].text

    while(mensagem == mensagem_anterior):
        mensagem = driver.find_elements_by_xpath("//div[contains(@class, 'message-in')]")[-1].text
        user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(usuario))
        user.click()
        time.sleep(1)
        user = driver.find_element_by_xpath('//span[@title = "{}"]'.format("Hackathon Unesp"))
        user.click()
        time.sleep(1)'''
    while True:
        try:
            user = driver.find_element_by_class_name('OUeyt')
            user.click()
            mensagem = driver.find_elements_by_xpath("//div[contains(@class, 'message-in')]")[-1].text
            user = driver.find_element_by_xpath('//span[@title = "{}"]'.format("Hackathon Unesp"))
            user.click()
            msg_box = driver.find_element_by_class_name('_2S1VP')
            msg_box.send_keys("")
            return mensagem, usuario
        except NoSuchElementException:
            pass

    return mensagem


def avaliacao_mensagem(mensagem):
    positivas = ['sim', 'muito', 'obrigada']
    negativas = ['nao', 'nunca', 'pessimo']

    resp = False
    for positiva in positivas:
        if (positiva in str(normalize(mensagem)).lower()):
            return "Fico feliz em poder ajudar :D"
            resp = True

    if (not resp):
        return "Sinto muito que não pude ajudar. \n" \
               "Que tal falar com a nossa central de atendimento? O número é (14) 4009-1740"


def normalize(string, codif='utf-8'):
    return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore')


def chat_bot_sequence(driver):
    g = GoogleApiUtils()

    mensagem, usuario = wait_new_message(driver)
    print(usuario)
    send(driver, usuario, mensagem_boasvindas)
    time.sleep(0.3)

    ponto_partida, _ = espera_resposta(driver, usuario, mensagem)
    print(ponto_partida[:-6])
    send(driver, usuario, mensagem_destino)
    time.sleep(0.3)
    ponto_destino, _ = espera_resposta(driver, usuario, ponto_partida)
    print(ponto_destino[:-6])

    if g.queryRoute(ponto_partida[:-6], ponto_destino[:-6]):
        steps = g.getInstructions()
        for step in steps:
            send(driver, usuario, step)

        time.sleep(10)
        send(driver, usuario, "A minha resposta lhe ajudou de alguma forma?")
        resposta_avaliacao, _ = espera_resposta(driver, usuario, ponto_partida)
        send(driver, usuario, avaliacao_mensagem(resposta_avaliacao[:-6]))

    else:
        send(driver, usuario, "Sinto muito, mas não consegui definir uma rota")
        send(driver, usuario, "Que tal falar com a nossa central de atendimento? O número é (14) 4009-1740")
    time.sleep(0.3)


if __name__ == "__main__":
    print(avaliacao_mensagem(str(normalize("Ajudou muito"))))
