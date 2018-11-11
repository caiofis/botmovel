from utils.google_api_utils import GoogleApiUtils

inicial = 0
partida = 1
destino = 2
feedback = 3


class Usuario():

    def __init__(self, nome):
        self.nome = nome
        self.estado = inicial
        self.partida = ""
        self.destino = ""
        self.googleApi = GoogleApiUtils()

    def getInstructions(self):
        if self.googleApi.queryRoute(self.partida, self.destino):
            steps = self.googleApi.getInstructions()
            return steps
        else:
            return None
