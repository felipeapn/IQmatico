class CalculadorDirecao:
    def __init__(self):
        pass

    def getColor(self, vela):

        if vela['open'] == vela['close']:
            return 0 #dojo
        else:
            if vela['open'] < vela['close']:
                return 1 #verde
            else:
                return -1 #vermelho

    def calcularDirecao(self, vela1, vela2, vela3):
        return self.getColor(vela1) + self.getColor(vela2) + self.getColor(vela3)

    def getMhiDirecao(self, direcao):
        if direcao < 0:
            return 'call'
        
        return 'put'