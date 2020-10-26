import PySimpleGUI as sg
import time
from datetime import datetime
from utils.paridade import Paridade
from fabricas.conectionFactory import ConnectionFactory
from automacao.mhi import Mhi

class RoboTela:
    def __init__(self):
        #layout
        self.API = ConnectionFactory.getConnection()
        self.paridade = Paridade(self.API)
        layout = [
            [sg.Text('Par',size=(7,0)),sg.Combo(self.paridade.getParidadeAbertas(), enable_events=True, key='par', size=(15,0))],
            [sg.Text('Entrada',size=(7,0)), sg.Input(key='entrada', size=(15,0))],
            [sg.Text('Martingale',size=(7,0)), sg.Input(key='martingale', size=(15,0))],
            [sg.Text('Stop Loss',size=(7,0)), sg.Input(key='stoploss', size=(15,0))],
            [sg.Text('Stop Gain',size=(7,0)), sg.Input(key='stopgain', size=(15,0))],
            [sg.Text('Selecione os algoritimos')],
            [sg.Checkbox('MHI', key='mhi'), sg.Checkbox('VT', key='vituxo'), sg.Checkbox('C3', key='c3')],
            [sg.Button('Executar'), sg.Button('Limpar')]
            #[sg.Output(size=(50,20), key="_output_")]
        ]
        #janela
        self.janela = sg.Window('Catalogador de Velas').layout(layout)
        #extrair dados
        #self.values = self.janela.Read()

    def iniciar(self): 
        while True:
            self.event, self.values = self.janela.Read()
            print(self.event, self.values)
            
            if self.event is None:
                break
            
            if self.event == 'Executar':
                self.executar()

            if self.event == 'Limpar':
                self.janela.find_element('_output_').Update('')

    def executar(self):
        robo = Mhi(self.API, float(self.values['stoploss']), float(self.values['stopgain']))
        #payout = float(self.paridade.payout(self.values['par'])) / 100
        robo.run(self.values['par'], float(self.values['entrada']), 1)
        estrategias = self.getEstrategias()        

    def getEstrategias(self):
        estrategias = []
        if self.values['mhi']:
            estrategias.append('mhi')

        if self.values['vituxo']:
            estrategias.append('vituxo')

        if self.values['c3']:
            estrategias.append('c3')
        
        return estrategias
              
tela = RoboTela()
tela.iniciar()
