import time
from datetime import datetime

from . import calcular
from utils.exportarCsv import ExportarCsv


def mhi(velas):
	listaCsv = calcular.mhi(velas)
	return listaCsv

def vituxo(velas):
	listaCsv = calcular.vituxo(velas)
	return listaCsv

def c3(velas):
	listaCsv = calcular.c3(velas)
	return listaCsv

operations = {
	'mhi': mhi,
	'vituxo': vituxo,
	'c3': c3,
}

def catalogar(par, dataInicio, dataFim, estrategias, API):
	
	print(f'Paridade: {par} - Dias: {dataInicio.hour} - {dataFim} - Estratégia: {estrategias}')
	velas = []

	if dataInicio.date() <= dataFim.date() :

		dayCounter = 0

		while dataInicio.replace(day=dataInicio.day + dayCounter).date() <= dataFim.date():
			
			horaInicio = dataInicio.hour
			horaFim = dataFim.hour
			qtdVelas1minuto = int(horaFim - horaInicio) * 60
			
			#Altera hora inicio pra hora fim pois API vai do final para tras
			dataVelas = dataInicio.replace(day=dataInicio.day + dayCounter, hour=dataFim.hour)

			timestamp = datetime.timestamp(dataVelas)
			#se for o dia corrente tem q pegar a hora atual
			agora = datetime.fromtimestamp(time.time())
			if dataVelas.date() ==  agora.date():
				timestamp = time.time()
				qtdVelas1minuto = int (agora.hour - horaInicio) * 60

			velas.extend(API.get_candles(par, 60, qtdVelas1minuto, timestamp))

			dayCounter += 1
		
		listaCsv = []
		for estrategia in estrategias:
			if estrategia in operations:
				listaCsv.extend(operations[estrategia](velas))

		print(listaCsv[0])
		toCsv = ExportarCsv(listaCsv, par)
		toCsv.criarCsv()

	else:
		print(f'Data inicio {dataInicio.date()} é maior que data fim {dataFim.date()}')
		print(dataFim.replace(day=dataFim.day + 1).date())

def catalogarToList(estrategia, par, inicio, qtdAnalises, API):
	qtdVelas1minuto = qtdAnalises * 5 + 6 #5 da primeira analise e 4 se tiver no minuto 4 ou 9
	velas = API.get_candles(par, 60, qtdVelas1minuto, inicio)

	return operations[estrategia](velas)