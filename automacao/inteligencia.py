from catalogo import catalogador
import time
from fabricas.conectionFactory import ConnectionFactory
from utils.paridade import Paridade

class Inteligencia:
    def __init__(self, API):
        self.API = API

    def anlizar(self):
        pesoParidades = self.prepararDados()
        pesoParidades = sorted(pesoParidades, key = lambda i: i['peso'], reverse=True)
        return pesoParidades[0]

    def prepararDados(self):
        paridade = Paridade(self.API)
        listaParidades = paridade.getTodosPayoutsAbertos()
        pesoParidades = []
        maiorPeso = 0
        for paridade in listaParidades:
            if int(paridade['payout']) >= 70:
                apostas = catalogador.catalogarToList('mhi', paridade['paridade'], time.time(), 12, self.API)
                pesoParidades.append({'paridade':  paridade['paridade'], 'peso': self.calcularPeso(apostas, paridade['payout']), 'payout': paridade['payout']})

        return pesoParidades

    def calcularPeso(self, apostas, payout):
        #Vericar quanto derratas em 12 (1hora). Quanto Mais derrotar melhor.
        qtdZeros = self.qtdDeZeros(apostas)
        qtdZerosSeguidos = self.zerosSeguidos(apostas)
        return float((qtdZeros + pow(qtdZerosSeguidos, 2)) * (int(payout) / 100))

    def qtdDeZeros(self, apostas):
        qtdZeros = 0
        for aposta in apostas:
            if aposta['tenativas'] == 0:
                qtdZeros += 1
        return qtdZeros

    def zerosSeguidos(self, apostas):
        qtdZeros = 0
        for aposta in reversed(apostas):
            if aposta['tenativas'] == 0:
                qtdZeros += 1
            else:
                return qtdZeros
        return qtdZeros
