from datetime import datetime, timedelta
import time

def contarVelas (lista):
    tamanhoLista = len(lista)
    print(tamanhoLista)
    print(lista[0])
    print(lista[tamanhoLista - 1])

    print(datetime.fromtimestamp(lista[0]["from"]))

def mhi(velas):
    
    direcao = 0
    vitoria = 0
    derrota = 0
    naoavaliado = 0
    listaCsv = []

    for i in range(len(velas)):
        data = datetime.fromtimestamp(velas[i]["from"])

        if (data.minute % 5) == 0 and ((datetime.timestamp(data + timedelta(minutes=3))) <= time.time()):
            direcao = calcularDirecao(velas[i -1], velas[i - 2], velas[i - 3])

            if direcao != 0:
            
                if not((i + 3) > len(velas)) :
                    tentativas = calcularVitoria(-direcao, velas[i], velas[i + 1], velas[i + 2])
                    #print('Time: ', data, ' Direcao: ', direcao, ' Tentativas: ', tentativas)
                    if tentativas == 0:
                        derrota += 1
                    else:
                        vitoria += 1
            else:
                tentativas = -1
                #print('Time: ', data, ' Direcao: ', direcao, ' Tentativas: DOJO')
                naoavaliado += 1

            #print('Time: ', data, ' Direcao: ', direcao, ' Tentativas: ', tentativas)
            listaCsv.append({
                'Data':data.date().strftime("%Y/%m/%d"),
                'Hora':data.time().strftime("%H:%M"),
                'Estrategia':'MHI',
                'direcao':direcao, 
                'tenativas':tentativas})
                
    #print('MHI -> Derrotas: ', derrota, 'Vitorias: ', vitoria, 'Nao Avalidado: ', naoavaliado)
    return listaCsv
    
def c3(velas):
    
    direcao = 0
    vitoria = 0
    derrota = 0
    naoavaliado = 0
    listaCsv = []

    for i in range(len(velas)):
        data = datetime.fromtimestamp(velas[i]["from"])
        tentativas = 0

        if (data.minute % 5) == 0 :

            if (getColor(velas[i - 1]) != 0) and (getColor(velas[i - 3]) != 0) and (getColor(velas[i - 5]) != 0):
            
                if not((i + 5) > len(velas)) :
                    if getColor(velas[i]) != getColor(velas[i - 5]):
                        tentativas = 1
                    elif getColor(velas[i + 2]) != getColor(velas[i - 3]):
                        tentativas = 2
                    elif getColor(velas[i + 4]) != getColor(velas[i - 1]):
                        tentativas = 3
                    #print('Time: ', data, ' Direcao: ', direcao, ' Tentativas: ', tentativas)
                    if tentativas == 0:
                        derrota += 1
                    else:
                        vitoria += 1
            else:
                tentativas = -1
                #print('Time: ', data, ' Direcao: ', direcao, ' Tentativas: DOJO')
                naoavaliado += 1

            print('Time: ', data, ' Direcao: ', direcao, ' Tentativas: ', tentativas)
            listaCsv.append({
                'Data':data.date().strftime("%Y/%m/%d"),
                'Hora':data.time().strftime("%H:%M"),
                'Estrategia':'C3',
                'direcao':direcao, 
                'tenativas':tentativas})
                
    print('C3 -> Derrotas: ', derrota, 'Vitorias: ', vitoria, 'Nao Avalidado: ', naoavaliado)
    return listaCsv

def vituxo(velas):
    
    direcao = 0
    vitoria = 0
    derrota = 0
    naoavaliado = 0
    listaCsv = []

    for i in range(len(velas)):
        data = datetime.fromtimestamp(velas[i]["from"])

        if (data.minute % 5) == 0 :
            direcao = calcularDirecao(velas[i - 3], velas[i - 4], velas[i - 5])
        
            if direcao != 0:
                #evitar acesso a indice inexistente.
                if not((i + 5) > len(velas)) :
                    tentativas = calcularVitoria(direcao, velas[i + 2], velas[i + 3], velas[i + 4])
                    
                    if tentativas == 0:
                        derrota += 1
                    else:
                        vitoria += 1
            else:
                tentativas = -1
                #print('Time: ', data, ' Direcao: ', direcao, ' Tentativas: DOJO')
                naoavaliado += 1

            print('Time: ', data, ' Direcao: ', direcao, ' Tentativas: ', tentativas)
            listaCsv.append({
                'Data':data.date().strftime("%Y/%m/%d"),
                'Hora':data.time().strftime("%H:%M"),
                'Estrategia':'Vituxo',
                'direcao':direcao, 
                'tenativas':tentativas})
                
    print('VITUXO -> Derrotas: ', derrota, 'Vitorias: ', vitoria, 'Nao Avalidado: ', naoavaliado)
    return listaCsv

def getColor(vela):

    if vela['open'] == vela['close']:
        return 0 #dojo
    else:
        if vela['open'] < vela['close']:
            return 1 #verde
        else:
            return -1 #vermelho

def calcularDirecao(vela1, vela2, vela3):
    return getColor(vela1) + getColor(vela2) + getColor(vela3)

def calcularVitoria(direcao, vela1, vela2, vela3):
    if direcao > 0 :
        direcao = 1
    else:
        direcao = -1

    if direcao == getColor(vela1):
        return 1
    if direcao == getColor(vela2):
        return 2
    if direcao == getColor(vela3):
        return 3

    return 0