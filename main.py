import re
import pandas as pd
import numpy as np

palavraReservada = {'def': '41'}

charArray = {',': ['15', 'VIRGULA'], ':': ['13', 'DOIS PONTOS'], '(': ['17', 'ABRE PARENT.'], ')': ['18', 'FECHA PARENT.']}

rules = ['([0-9]+(.[0-9]+))', 'DECIMAL']

classificados = []
nextWord = False
isNum = False
isString = False
numeral = ''
fullComment = ''

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
    l = a.split(' ')
    for item in l:
        if (item != ''):
            f.append(item)
    return f

def isPalavraReservada(word):
    return word in palavraReservada

def isSpecialChar(word):
    return word in charArray

def isIdentfier(word):
    if re.match('^[0-9]', word) != None:
        raise ValueError(word + ' Identificadores não podem iniciar com numerais')
    if re.fullmatch('^[a-zA-Z0-9]{1,}$', word) != None:
        return True

def isNumber(word):
    return re.fullmatch('^[0-9]{1,}$', word) != None

def trataCaracter(lista, index, char):
    global nextWord
    global numeral
    keyChar = charArray[char]
    if keyChar[0] == ' ':
        if lista[index + 1].upper() in palavraReservada:
            classificados.append((keyChar[0], char, keyChar[1]))
        else:
            raise ValueError(char + lista[index + 1] + ' Não é reconhecido como comando valido.')
    else:
        classificados.append((keyChar[0], char, keyChar[1]))

def validaExistencia(l, i, word):
    global specialChar
    if isPalavraReservada(word):
        classificados.append((palavraReservada[word], word, 'PALAVRA RESERVADA'))
        return
    if isSpecialChar(word):
        trataCaracter(l, i, word)
        return
    if isIdentfier(word):
        classificados.append(('41', word, 'IDENTIFICADOR'))
        return

    raise ValueError(word + ' Não é reconhecido como comando valido.')

def validaString(char):
    global isString
    global nextWord
    global fullComment
    if char == '"':
        if isString:
            isString = False
            fullComment += char
            classificados.append(('100', fullComment, 'STRING'))
            fullComment = ''
            nextWord = True
        else:
            isString = True
            fullComment += char
            nextWord = True
    elif isString:
        fullComment += ' ' + char
        nextWord = True

def mostrar():
    global classificados
    classificados = np.array(classificados)
    for i, p in enumerate(' '):
        data = pd.DataFrame({'Token': classificados[:, 1], 'Descrição': classificados[:, 2]})
        print(data)

def cursor(l):
    global nextWord
    global comentario
    global fullComment
    global isNum
    global classificados
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
