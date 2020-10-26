import PySimpleGUI as sg
import time
from datetime import datetime
from fabricas.conectionFactory import ConnectionFactory
from utils.paridade import Paridade
from utils import horas
from catalogo import catalogador

class CatalogadorTela:
    def __init__(self):
        #layout
        self.API = ConnectionFactory.getConnection()
        self.paridade = Paridade(self.API).getParidadeAbertas()
        self.listaHora = horas.listaHora()
        layout = [
            [sg.Text('Par',size=(8,0)),sg.Combo(self.paridade, enable_events=True, key='par', size=(15,0))],
            [sg.Text('Hora Inicio',size=(8,0)),sg.Combo(self.listaHora, key='horaInicio', size=(15,0)), sg.Text('Hora Fim',size=(7,0)),sg.Combo(self.listaHora, size=(15,0), key=('horaFim'))],
            [sg.Text('Data Inicio',size=(8,0)),sg.Input(key='dataInicio', enable_events=True, visible=True, size=(20,0)), sg.CalendarButton('Calendario', target='dataInicio', pad=None, key='_CALENDAR_', format=('%Y-%m-%d'))],
            [sg.Text('Data Fim',size=(8,0)),sg.Input(key='dataFim', enable_events=True, visible=True, size=(20,0)), sg.CalendarButton('Calendario', target='dataFim', pad=None, key='_CALENDAR_', format=('%Y-%m-%d'))],
            [sg.Text('Selecione os algoritimos')],
            [sg.Checkbox('MHI', key='mhi'), sg.Checkbox('VT', key='vituxo'), sg.Checkbox('C3', key='c3')],
            [sg.Button('Conectar'), sg.Button('Enviar Dados'), sg.Button('Limpar')]
            #[sg.Output(size=(150,10), key="_output_")]
        ]
        #janela
        self.janela = sg.Window('Catalogador de Velas').layout(layout)
        #extrair dados
        #self.values = self.janela.Read()

    def iniciar(self): 
        while True:
            self.event, self.values = self.janela.Read()
            print(self.event, self.values)
            self.janela.find_element('horaInicio').expand(expand_row=False)
            if self.event is None:
                break
            
            if self.event == 'Conectar':
                self.conectar()

            if self.event == 'Limpar':
                self.janela.find_element('_output_').Update('')

    def conectar(self):
        estrategias = self.getEstrategias()
        dataInicio = datetime.fromisoformat(f'{self.values["dataInicio"]} {self.values["horaInicio"]}')
        dataFim = datetime.fromisoformat(f'{self.values["dataFim"]} {self.values["horaFim"]}')
        catalogador.catalogar(self.values['par'], dataInicio, dataFim, estrategias, self.API )

    def getEstrategias(self):
        estrategias = []
        if self.values['mhi']:
            estrategias.append('mhi')

        if self.values['vituxo']:
            estrategias.append('vituxo')

        if self.values['c3']:
            estrategias.append('c3')
        
        return estrategias
              
tela = CatalogadorTela()
tela.iniciar()
