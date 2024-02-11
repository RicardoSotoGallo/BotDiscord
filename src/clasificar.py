import re
from unicodedata import normalize

def clasDiscor(file:str):
    texto = open(file,mode="r",encoding="utf-8")
    testClas = []
    aux = ""
    primero = True
    for i in texto.readlines():#Miramos si tiene el formato con fecha y hora
                                #se guarda la frase en aux
        if ("—" in i and "/" in i and ":" in i):
            if primero:
                primero = False
            else:
                testClas.append(aux)
                aux = ""
        else:#quitamos los enter
            i = i.replace("\n","")
            aux += i
    respuesta:"list[list]" = []
    anterior = None
    aux = []
    for i in testClas:
        if anterior == None:
            anterior = i
        else:
            aux = []
            aux.append(anterior)
            aux.append(i)
            anterior = i
            respuesta.append(aux)

    texto.close()
    texto = open("file/datosDiscordPreparado.txt",mode="w",encoding="utf-8")
    for i in respuesta:#se guarda en la base de datos 
        texto.write(f"{i[0]}-><-{i[1]}\n")
    texto.close()

textoEliminar = ["el","la","los","las","qva","mas","menos","hey","tu","me","te","se","una","que","mas","por",]
Textointerior = ["?","¿",",","\n",".",")","(","[","]"]

def tratarDatosTodo():
    textoDiscord = open("file/datosDiscordPreparado.txt",mode="r",encoding="utf-8")
    textoWhatapp = open("file/datosPreparadosWhatapp.txt",mode="r",encoding="utf-8")
    textoWhatOperacion = open("file/contestacionesCapturadas.txt",mode="r",encoding="utf-8")
    vectorDiscord = []
    for i in textoDiscord:
        aux = i.split("-><-")
        aux[0] = eliminarFrase(aux[0])
        aux[1] = aux[1].replace("\n","")
        vectorDiscord.append(aux)
    vectorWhatApp = []
    for i in textoWhatapp:
        aux = i.split("-><-")
        aux[0] = eliminarFrase(aux[0])
        aux[1] = aux[1].replace("\n","")
        vectorWhatApp.append(aux)
    vectorOperacion = []
    for i in textoWhatOperacion:
        aux = i.split("-><-")
        aux[0] = eliminarFrase(aux[0])
        aux[1] = aux[1].replace("\n","")
        vectorOperacion.append(aux)
    res:"list" = []
    for i in vectorDiscord:
        if len(i[0]) != 0:
            res.append(i)
    for i in vectorWhatApp:
        if len(i[0]) != 0:
            res.append(i)
    for i in vectorOperacion:
        if len(i[0]) != 0:
            res.append(i)
    return res

def eliminarFrase(cacho:str):
    cacho = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", cacho), 0, re.I)
    cacho = normalize( 'NFC', cacho)
    cacho = cacho.lower()

    palabra:"list[str]" = cacho.split(" ")
    aux = []
    for i in palabra:
        aux2 = i
        for j in Textointerior:
            aux2 = aux2.replace(j,"")
        for j in textoEliminar:
            if aux2 == j:
                aux2 = ""
        if len(aux2) > 2:
            aux.append(aux2)
    palabra = aux
    if '' in palabra:
        palabra.remove('')
    return palabra

def escribirEnLaBase(ls:"list[list]"):
    escribir = open("file/datoParaRed.txt",mode="w",encoding="utf-8")
    for i in ls:
        escribir.write(f"{i[0]}-><-{i[1]}\n")
    escribir.close()

def leerEnLaBase(file:str):
    leer = open(file,mode="r",encoding="utf-8")
    entrada = []
    salida = []
    for i in leer:
        aux = i.split("-><-")

        aux[0] = aux[0].replace("[","")
        aux[0] = aux[0].replace("]","")
        aux[0] = aux[0].replace("'","")
        lsAux = aux[0].split(", ")
        aux[0] = []
        for i in lsAux:
            aux[0].append(i)
        entrada.append(aux[0])
        aux[1] = aux[1].replace("\n","")

        salida.append(aux[1])
    
    res = dict()
    contAux = 0
    for e,s in zip(entrada,salida):
        res[contAux] = [e,s]
        contAux += 1
    return res

def añadir(file:str,entrada:str,salida:str):
    with open(file,mode="a",encoding="utf-8") as archivo:
        archivo.write(f"{entrada}-><-{salida}\n")
clasDiscor("file/datosDiscor.txt")
cachos = tratarDatosTodo()
escribirEnLaBase(cachos)
leerEnLaBase("file/datoParaRed.txt")
#hacer dos lista una de palabras completas y otra de por media
#texto = "Te gusta el porno? por"
#texto = eliminarFrase(texto)
#print(texto)