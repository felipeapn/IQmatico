from iqoptionapi.stable_api import IQ_Option
import time

class ConnectionFactory:

    @classmethod
    def getConnection(self):
        API = IQ_Option('login', 'senha')

        check, reason= API.connect()
        API.change_balance('PRACTICE') # PRACTICE / REAL

        while True:
            if API.check_connect() == False:
                print('Erro ao se conectar')
                API.connect()
            else:
                print('Conectado com sucesso')
                break
            
            time.sleep(1)
        return API