
class Martingale:
    def __init__(self, qtd):
        self.qtd = int(qtd)

    def getMartingales(self, valorEntrada, payout):
        listaEntrada = []
        listaEntrada.append(float(valorEntrada))
        retornoEsperado = valorEntrada * float(payout)
        for i in range(self.qtd):
            listaEntrada.append(round(listaEntrada[i] + (listaEntrada[i] / float(payout)),2))
        
        return listaEntrada


