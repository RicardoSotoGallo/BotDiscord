from math import *
from random import random
import re
from unicodedata import normalize
from clasificar import eliminarFrase
#https://cienciadedatos.net/documentos/33_arboles_de_prediccion_bagging_random_forest_boosting#Introducci%C3%B3n
class rama():
    ramaId:str = ""
    valorId:int = 0
    hijo:"list[str]" = [] #Los valores de ramaId hijo primero si segundo no
    hijoSi:"list[int]" = [] #Hijos que si
    hijoNo:"list[int]" = [] #Hijos que no
    lsEntradas:"list[int]" = []
    lsPalabras:"list[str]" = []
    puntuacion:float = 0
    def crear(self,nombre:str,valorId):
        self.ramaId = nombre
        self.valorId = valorId
    
    def colocarHijo(self,hijo):
        self.hijo = hijo
        tipo = "rama"
        if len(hijo) == 0:
            tipo = "hoja"
        self.tipo = tipo
    
    def conocerTipo(self):
        res = ''
        if self.tipo == '':
            tipo = "rama"
            if len(self.hijo) == 0:
                tipo = "hoja"
            self.tipo = tipo
            res = tipo
        else:
            res = self.tipo
        return res

    def valores(self,lsClasificar:"list[list[str]]"):
        self.lsClasificar = lsClasificar

    def calcularCaos(self):
        """
        Calcular si los resultados son binarios
        """
        self.puntuacion = -(self.positivo/self.total)*log2(self.positivo/self.total)-(self.negativo/self.total)*log2(self.negativo/self.total)

class arbol():
    nodo:"list[rama]" = []
    #entrada:"list[list[str]]" = []
    #salida:"list[str]" = []
    diccionarioES:"dict[int:list[list[str]:str]]" = {}
    palabras:"list[str]" = []
    maximoGrupo:int = 0
    cont:int = 0
    def crearPorTxt(self,file:str):
        grafoLeer = open(file,mode="r")
        lsNombre = []
        for i in grafoLeer:
            i = i.replace("\n","")
            n = i.split(";")
            
            nombre = n[0]
            enlace = n[1].split(",")
            ram = rama()
            ram.crear(nombre,enlace)
            self.nodo.append(ram)
            if nombre in lsNombre:
                lsNombre.remove(nombre)
            lsNombre += enlace
        grafoLeer.close()
        for i in lsNombre:
            ram = rama()
            ram.crear(i,[])
            self.nodo.append(ram)
    
    def escribirViz(self):
        texto = open("file/grafoViz.txt",mode="w")
        texto.write("digraph g{\n")
        for i in self.nodo:
            texto.write(f"\t{i.valorId} [label=\"{i.ramaId}\"]\n")
        for i in self.nodo:
            #print(f"nodo -> {i.ramaId}{i.valorId} hijo -> {i.hijo}")
            hijo = i.hijo
            nombre = i.ramaId
            valor = i.valorId
            for j in hijo:
                if j != None:
                    texto.write(f"\t{valor} -> {j};\n")
        texto.write("}")
        texto.close()

    def crearPorDatos(self,maximasFrasesPraKnn:int):
        palabras = []
        entradas = []
        aMirar:"list[rama]" = []
        for i in self.diccionarioES.keys():
            palabras += self.diccionarioES[i][0]
            entradas.append(i)
        self.palabras = list(set(palabras))
        nodoAux = self.mejor(entradas,self.palabras)
        self.nodo.append(nodoAux)
        aMirar.append(nodoAux)
        while(len(aMirar) != 0):
            nodoActual = aMirar[0]
            #print(f"nombre -> {nodoActual.ramaId} hijoSi -> {nodoActual.hijoSi} hijoNo -> {nodoActual.hijoNo} aMirar -> {aMirar}")
            aMirar.pop(0)
            CondicionParadaNoPalabras = len(nodoActual.lsPalabras)
            if (len(nodoActual.hijoSi) < maximasFrasesPraKnn and len(nodoActual.hijoNo) < maximasFrasesPraKnn) or CondicionParadaNoPalabras == 0:
                if CondicionParadaNoPalabras == 0:
                    nodoActual.hijo = [None,None]
            else:
                hijos = []
                if len(nodoActual.hijoSi) > maximasFrasesPraKnn:
                    nodoHijoSi = self.mejor(nodoActual.hijoSi,nodoActual.lsPalabras.copy())
                    if (nodoActual.hijoSi != [] and nodoActual.hijoNo != []):
                        aMirar.append(nodoHijoSi)
                        self.nodo.append(nodoHijoSi)
                        hijos.append(nodoHijoSi.valorId)
                else:
                    hijos.append(None)
                if len(nodoActual.hijoNo) > maximasFrasesPraKnn:
                    nodoHijoNo = self.mejor(nodoActual.hijoNo,nodoActual.lsPalabras.copy())
                    if (nodoActual.hijoSi != [] and nodoActual.hijoNo != []):
                        aMirar.append(nodoHijoNo)
                        self.nodo.append(nodoHijoNo)
                        hijos.append(nodoHijoNo.valorId)
                else:
                    hijos.append(None)
                nodoActual.hijo = hijos

            
    def mejor(self,lsEntrada:"list[int]",condicion:"list[str]"):
        minimo = None
        letraMin = ""
        lsPosi = []
        lsNega = []
        for i in condicion:
            minimoAux,lsPosiAux,lsNegaAux = self.calculoPuntos(lsEntrada,i)
            if minimo == None:
                minimo =  minimoAux
                letraMin = i
                lsPosi = lsPosiAux
                lsNega = lsNegaAux
            elif minimoAux < minimo:
                minimo =  minimoAux
                letraMin = i
                lsPosi = lsPosiAux
                lsNega = lsNegaAux
            
        mejorNodo = self.crearNodo(letraMin,condicion.copy(),lsPosi,lsNega)
        return mejorNodo
                       
    def crearNodo(self,letraMin:str,condicion:"list[str]",lsPosi:"list[int]",lsNega:"list[int]"):
        mejorNodo = rama()
        mejorNodo.ramaId = letraMin
        mejorNodo.valorId = self.cont
        self.cont += 1
        condicion.remove(letraMin)
        #print(f"letra -> {letraMin} condiciones -> {condicion}")
        mejorNodo.lsPalabras = condicion
        mejorNodo.hijoSi = lsPosi
        mejorNodo.hijoNo = lsNega
        return mejorNodo
    
    def calculoPuntos(self,lsEntrada:"list[int]",condicion:str):
        """
        El bueno es el que tiene la puntiacion mas baja
        """
        entrada = []
        for i in lsEntrada:
            entrada.append(self.diccionarioES[i][0])
        total = 0
        posi = 0
        nega = 0
        lsPosi:"list[str]" = []
        lsNega:"list[str]" = []
        for texto,numero in zip(entrada,lsEntrada):
            total += 1
            if condicion in texto:
                posi += 1
                lsPosi.append(numero)
            else:
                nega += 1
                lsNega.append(numero)
        puntuacion = abs(posi-nega)
        return puntuacion,lsPosi,lsNega
    
    def recorrer(self,texto:str):
        res = []
        texto = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", texto), 0, re.I)
        texto = normalize( 'NFC', texto)
        texto = texto.lower()
        lsTexto:"list[str]" = texto.split(" ")
        aux = []
        for i in  lsTexto:
            aux.append(i.strip())
        lsTexto = aux
        nodoActual = self.nodo[0]
        while(True):
            condicion = nodoActual.ramaId
            #print(f"para porfa -> {nodoActual.lsPalabras} hijos -> {nodoActual.hijo} hijosSi -> {nodoActual.hijoSi} hijosNo -> {nodoActual.hijoNo}")
            if len(nodoActual.hijo) == 2:
                if condicion in lsTexto:
                    sige = nodoActual.hijo[0]
                    if sige != None:
                        for i in self.nodo:
                            if i.valorId == sige:
                                nodoActual = i
                    else:
                        res = nodoActual.hijoSi
                        break

                else:
                    sige = nodoActual.hijo[1]
                    if sige != None:
                        for i in self.nodo:
                            if i.valorId == sige:
                                nodoActual = i
                    else:
                        res = nodoActual.hijoNo
                        break

            else:
                if condicion in lsTexto:
                    res = nodoActual.hijoSi  
                else:
                    res = nodoActual.hijoNo
                break

        resAux = []
        for i in res:
            resAux.append(self.diccionarioES[i])
        return resAux

class k_nn():
    entrada:"list[list[str]]" = []
    salida:"list[str]" = []
    frase:"list[str]" = []
    valorSalida:"list[int,str]" = []
    referencias = ["alagame","albion online","ella abajo"]
    def __init__(self,datos:"list[list[list[str]],list[str]]",frase:str) -> None:
        NoRefrencia = False
        if frase in self.referencias:
            NoRefrencia = True
            if frase == self.referencias[0]:
                self.valorSalida = [[1,"Eres realmente excepcional. Tu curiosidad y disposición para aprender son admirables. La forma en que abordas los desafíos con determinación demuestra tu valentía y perseverancia. Además, tu amabilidad y respeto hacia los demás hacen que seas una persona realmente agradable de tener cerca. Sigue brillando con tu luz única, ¡eres increíble!",[]]]
            if frase == self.referencias[1]:
                self.valorSalida = [[1," albion online es un mmorpg no lineal en el que escribes tu propia historia sin limitarte a seguir un camino prefijado, explora un amplio mundo abierto con cinco biomas unicos, todo cuanto hagas tendra su repercusíon en el mundo, con su economia orientada al jugador de albion los jugadores crean practicamente todo el equipo a partir de los recursos que consiguen, el equipo que llevas define quien eres, cambia de arma y armadura para pasar de caballero a mago o juego como una mezcla de ambas clases, aventurate en el mundo abierto y haz frente a los habitantes y las criaturas de albion, inicia expediciones o adentrate en mazmorras en las que encontraras enemigos aun mas dificiles, enfrentate a otros jugadores en encuentros en el mundo abierto, lucha por los territorios o por ciudades enteras en batallas tacticas, relajate en tu isla privada donde podras construir un hogar, cultivar cosechas, criar animales, unete a un gremio, todo es mejor cuando se trabaja en grupo [musica] adentrate ya en el mundo de albion y escribe tu propia historia. ",[]]]
            if frase == self.referencias[2]:
                self.valorSalida = [[1,"y arriba españa",[]]]
        if not NoRefrencia:
            self.valorSalida = []
            fraseCopia = eliminarFrase(frase)
            for i in datos:
                e = i[0]
                s = i[1]
                posi = 0
                difLen = len(e)-len(fraseCopia)
                self.frase = eliminarFrase(frase)
                for j in e:
                    if j in self.frase:
                        posi += 1
                valor = (2*posi )**2- abs(difLen)
                if valor < 0:
                    valor = 0.1
                self.valorSalida.append([valor,s,e])
            self.valorSalida.sort(reverse= True)
    def obtenerXprimero(self,x:int):
        if self.valorSalida[0][0] == 0.1:
            self.valorSalida = [
                [1,"tus putos muertos",[]],
                [1,"feliu es maricon",[]],
                [1,"las tetas de manu",[]],
                [1,"como caca seca",[]],
                [1,"pa ti mi cola",[]],
                [1,"tu madre por si acaso",[]],
                [1,"ricardo es fantastico",[]],
                [1,"Thanos no hizo nada malo",[]]
            ]
        return self.valorSalida[:x]

def eleguirUnoPorRuleta(valores:"list[int,str]"):
    suma = 0
    for i in valores:
        suma += i[0]
    posicion = random()*suma
    res = valores[0][1]
    acumulador = i[0]
    for i in valores:
        if acumulador > posicion:
            break
        else:
            res = i[1]
            acumulador += i[0]
    return res