import re
import pandas as pd
import numpy as np

palavraReservada = {'def': '41'}

charArray = {',': ['15', 'VIRGULA'], ':': ['13', 'DOIS PONTOS'], '(': ['17', 'ABRE PARENT.'], ')': ['18', 'FECHA PARENT.']}

caracteresEspeciais = {'!': ['01'],
                        '@': ['02'],
                        '#': ['03'],
                        '$': ['04'],
                        '%': ['05'],
                        '&': ['06'],
                        '*': ['07'],
                        '?': ['08'],
                        '~': ['09'],
                        '^': ['10 ']}

classificados = []
nextWord = False
isString = False

def readTxt():
    print('-- Lendo arquivo de texto --\n')
    l, f = [], []
    g = open('ExpressaoRegular.txt', 'r')
    g = g.read()
    a = g.replace('\n', ' ')
    a = a.replace(',', ' , ')
    a = a.replace(':', ' : ')
    a = a.replace('(', ' ( ')
    a = a.replace(')', ' ) ')
    a = a.replace('!', ' ! ')
    a = a.replace('@', ' @ ')
    a = a.replace('#', ' # ')
    a = a.replace('$', ' $ ')
    a = a.replace('%', ' % ')
    a = a.replace('&', ' & ')
    a = a.replace('*', ' * ')
    a = a.replace('?', ' ? ')
    a = a.replace('~', ' ~ ')
    a = a.replace('^', ' ^ ')
    l = a.split(' ')
    for item in l:
        if (item != ''):
            f.append(item)
    return f

def verificaNumero(palavra):
    return re.match('^[0-9]', palavra) != None

def verificaLetra(palavra):
    return re.fullmatch('^[a-zA-Z0-9]{1,}$', palavra) != None

def verificarCaractereEspecial(palavra):
    return palavra in caracteresEspeciais

def verificarPalavraReservada(palavra):
    return palavra in palavraReservada

def verificarSpecialChar(palavra):
    return palavra in charArray

def verificarIdentificador(palavra):
    if verificaNumero(palavra):
        raise ValueError(palavra + ' Identificadores não podem iniciar com numerais')
    if verificaLetra(palavra):
        return True

def trataCaracter(lista, index, char):
    keyChar = charArray[char]
    if keyChar[0] == ' ':
        if lista[index + 1].upper() in palavraReservada:
            classificados.append((keyChar[0], char, keyChar[1]))
        else:
            raise ValueError(char + lista[index + 1] + ' Não é reconhecido como comando valido.')
    else:
        classificados.append((keyChar[0], char, keyChar[1]))

def validaExistencia(lista, index, palavra):
    if verificarPalavraReservada(palavra):
        classificados.append((palavraReservada[palavra], palavra, 'PALAVRA RESERVADA'))
        return
    if verificarSpecialChar(palavra):
        trataCaracter(lista, index, palavra)
        return
    if verificarIdentificador(palavra):
        classificados.append(('rules', palavra, 'IDENTIFICADOR'))
        return
    if verificarCaractereEspecial(palavra):
        classificados.append((caracteresEspeciais, palavra, 'CARACTERES ESPECIAS'))
        return

    raise ValueError(palavra + ' Não é reconhecido como comando valido.')

def validaString(char):
    global isString
    global nextWord
    if char == '"':
        if isString:
            isString = False
            classificados.append(('100', 'STRING'))
            nextWord = True
        else:
            isString = True
            nextWord = True
    elif isString:
        nextWord = True

def mostrar():
    global classificados
    classificados = np.array(classificados)
    for p in enumerate(' '):
        data = pd.DataFrame({'Token': classificados[:, 1], 'Descrição': classificados[:, 2]})
        print(data)

def cursor(l):
    global nextWord
    global isString
    try:
        for i, p in enumerate(l):
            validaString(p)
            if isString:
                continue
            if nextWord:
                nextWord = False
                continue
            validaExistencia(l, i, p)
        mostrar()
        print('Finalizada Analise sem Erros.')
    except ValueError as e:
        print('ERRO: ' + str(e))
        mostrar()

l = readTxt()
cursor(l)