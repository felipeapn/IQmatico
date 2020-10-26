from datetime import datetime
import time
import sys
from tqdm import tqdm
from utils.calculadorDirecao import CalculadorDirecao
from utils.martingale import Martingale
from automacao.inteligencia import Inteligencia #usado para descobri qual é a melhor paridade.

class Mhi:

    def __init__(self, API, stopLoss, stopGain):
        self.API = API
        self.stopLoss = float(stopLoss)
        self.stopGain = float(stopGain)
        self.intel = Inteligencia(self.API)
        

    def run(self, par, valorEntrada, payout):
        paridadePeso = self.intel.anlizar()
        par = paridadePeso['paridade']
        payout = float(paridadePeso['payout']) / 100
        calculadora = CalculadorDirecao()
        direcao = 0
        martingale = Martingale(2)
        valoresEntrada = martingale.getMartingales(valorEntrada, payout)
        resultadoTodasOperacoes = 0
        resultadoTodasTentativas = 0
        resultadoTotalAcertos = 0
        
        analiseParidade = True
        initPbar = True
        while True :

            minutos = float((datetime.now().strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
            calcularParidade = True if (minutos >= 3.58 and minutos <= 4) or (minutos >= 8.58 and minutos <= 9) else False

            if (analiseParidade and calcularParidade):
                analiseParidade = False
                paridadePeso = self.intel.anlizar()
                par = paridadePeso['paridade']
                payout = float(paridadePeso['payout']) / 100
                #se o peso maior q 5 dobrar aposta
                if paridadePeso["peso"] >= 5:
                    valoresEntrada = martingale.getMartingales(valorEntrada * 2, payout)
                else:
                    valoresEntrada = martingale.getMartingales(valorEntrada, payout)

            if initPbar:
                initPbar = False
                pbar = tqdm(total=(5*60-1))
                pbar.update(self.getProgressBarTime(minutos))
            pbar.update(1)
            if entrar:
                initPbar = True
                pbar.close()
                print('Hora de entrar?',entrar,'/ Minutos:',minutos)
                print('\nIniciando operação!')
                dir = False
                print('Verificando cores..', end='')
                velas = self.API.get_candles(par, 60, 3, time.time())
                direcao = calculadora.calcularDirecao(velas[0], velas[1], velas[2])

                if direcao == 0 :
                    print(f'Direcao = {direcao} vela DOJO na avalicao!')
                
                else:
                    dir = calculadora.getMhiDirecao(direcao)
                    resultado = 0
                    countMt = 0
                    somaResultado = 0

                    analiseParidade = True # Se comprar temos que refazer a analise de paridade

                    while resultado <= 0 and countMt < len(valoresEntrada):
                        if resultado <= 0:
                            print(f'Compra um {dir}, {valoresEntrada[countMt]} | {par} peso: {paridadePeso["peso"]}')
                            status,id = self.API.buy(float(valoresEntrada[countMt]), par, dir , 1)

                            if status:
                                print(f'Compra realizada id:{id}, valor:{valoresEntrada[countMt]}, Gale:{countMt}')
                                resultado = round(self.API.check_win_v3(id), 2)
                                somaResultado += resultado
                                countMt += 1
                            else:
                                print('\nERRO AO REALIZAR OPERAÇÃO: {id}\n\n')
                                break
                    
                    if somaResultado >= 0:
                        print(f'Vitoria na tentativa {countMt} valor de {round(somaResultado,2)}')
                        resultadoTotalAcertos += 1
                    else:
                        print(f'Derrota na tentativa {countMt} valor de {round(somaResultado,2)}')

                    resultadoTodasOperacoes += somaResultado
                    resultadoTodasTentativas += 1

                    print(f'Resultado Geral -> {round(resultadoTodasOperacoes,2)}. {resultadoTotalAcertos} acertos em {resultadoTodasTentativas} tentativas')
                    self.stop(round(resultadoTodasOperacoes,2), self.stopGain, self.stopLoss)
                    
            time.sleep(1)

    def getProgressBarTime(self, minutos):
        min = int(str(minutos)[:1])
        sec = int(str(minutos)[2:])
        if minutos > 5:
            min = min - 5
        
        return (min * 60) + sec

        
    def stop(self, lucro, gain, loss):
        if lucro <= float('-' + str(abs(loss))):
            print('Stop Loss batido!')
            sys.exit()
            
        if lucro >= float(abs(gain)):
            print('Stop Gain Batido!')
            sys.exit()

                