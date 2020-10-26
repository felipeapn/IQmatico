def listaHora():
    contador = 0 
    lista = []

    while contador < 10 :
        lista.append(f'0{contador}:00')
        contador += 1
    
    while contador < 24 :
        lista.append(f'{contador}:00')
        contador += 1
            
    return lista
