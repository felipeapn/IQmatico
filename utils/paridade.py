from fabricas.conectionFactory import ConnectionFactory
import time

class Paridade:

    def __init__(self, API):
        self.API = API
        self.profits = self.API.get_all_profit()

    def payout(self, par):
        
        return int(100 * self.profits[par]['turbo'])

    def getParidadeAbertas(self):
        par = self.API.get_all_open_time()
        lista = []
        for paridade in par['turbo']:
            
            if par['turbo'][paridade]['open'] == True:
                lista.append(paridade)
        
        return lista

    def getTodosPayoutsAbertos(self):
        par = self.API.get_all_open_time()
        lista = []
        for paridade in par['turbo']:
            
            if par['turbo'][paridade]['open'] == True:
                payout = str(self.payout(paridade))
                lista.append({'paridade': paridade, 'payout': payout })
        
        return lista
    #print(f'Paridades: {paridade} ')