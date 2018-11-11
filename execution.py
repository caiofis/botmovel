import time
from model.usuario import *
from lib_chat import *

usuarios = {}

def chat_bot_sequence(driver):

    mensagem, user_name = wait_new_message(driver)
    mensagem = mensagem[:-6]
    time.sleep(1)
    #Consulta usuario
    if user_name in usuarios.keys():
        user = usuarios[user_name]
        if user.estado == inicial:
            user.partida = mensagem
            user.estado = partida
            send(driver, user_name, mensagem_destino)

        elif user.estado == partida:
            user.destino = mensagem

            steps = user.getInstructions()
            if steps is not None:
                for step in steps:
                    send(driver, user_name, step)
                send(driver, user_name, "A minha resposta lhe ajudou de alguma forma?")
                user.estado = feedback
            else:
                send(driver, user_name, "Sinto muito, mas não consegui definir uma rota")
                send(driver, user_name, "Que tal falar com a nossa central de atendimento? O número é (14) 4009-1740")
                del usuarios[user_name]

        elif user.estado == feedback:
            send(driver, user_name, avaliacao_mensagem(mensagem))
            time.sleep(2)
            del usuarios[user_name]

    #Nao encontrou - começa a conversa
    else:
        usuarios[user_name] = Usuario(user_name)
        send(driver, user_name, mensagem_boasvindas)