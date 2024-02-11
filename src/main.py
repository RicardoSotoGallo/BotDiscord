from arbol import *
from clasificar import *
import discord
#"file/grafo1.txt"
token = "Aqui pon tu toqken"
diccionarioIn = {
    1:[['eso', 'hablo', 'mucho', 'aqui'],"buenas que"],
    2:[['eso', 'hablo', 'mucho', 'aqui'],"buenas que"],
    3:[['eso', 'hablo', 'mucho', 'aqui'],"buenas que"],
    4:[['eso', 'hablo', 'mucho', 'aqui'],"buenas que"],
    5:[['poyade', 'eso', 'riorio'],"buenas que"],
    6:[['poyade', 'eso', 'riorio'],"buenas que"],
    7:[['poyade', 'eso', 'riorio'],"buenas que"],
    8:[['eso', 'igual','voy'],"buenas que"],
    9:[['eso', 'igual','voy'],"buenas que"],
    10:[['eso', 'igual','voy'],"buenas que"],
    11:[['eso', 'igual','voy'],"buenas que"],
    12:[['sip', 'eso', 'voy', 'hacer'],"buenas que"],
    13:[['sip', 'eso', 'voy', 'hacer'],"buenas que"],
    14:[['sip', 'eso', 'voy', 'hacer'],"buenas que"],
    15:[['sip', 'eso', 'voy', 'hacer'],"buenas que"]
}
tree = arbol()
diccionario = leerEnLaBase("file/datoParaRed.txt")
tree.diccionarioES = diccionario
tree.crearPorDatos(500)
tree.escribirViz()




primerCaracter = "*"
intente = discord.Intents.default()
intente.message_content = True
bot = discord.Client(intents= intente)

@bot.event
async def on_message(ctx:discord.message.Message):
    if ctx.author.bot == False and len(ctx.content) > 0:
        if ctx.content[0] == primerCaracter:
            frase = ctx.content[1:]
            historiaTexto = []
            historiaEsBot = []
            async for i in ctx.channel.history(limit=2):
                historiaTexto.append(i.content)
                historiaEsBot.append(i.author.bot)
            print(historiaTexto)
            print(historiaEsBot)
            #print(Ini)
            if historiaEsBot[1] == True:
                entrada = historiaTexto[1]
                salida = historiaTexto[0]
                salida = salida[1:]
                añadir("file/contestacionesCapturadas.txt",entrada,salida)
            texto = tree.recorrer(frase)
            kn = k_nn(texto,frase)
            resultado1 = kn.obtenerXprimero(10)
            resultado = eleguirUnoPorRuleta(resultado1)
            print("entradas -> {frase}")
            print(f"posibles salidas -> {resultado1}")
            await ctx.channel.send(resultado)
            
bot.run(token)

#-----------------------------------------------------------------------------
"""frase = "hola"
texto = tree.recorrer(frase)
#print(texto)
kn = k_nn(texto,frase)
resultado = kn.obtenerXprimero(10)
print(f"Posibles valores -> {resultado}")
resultado = eleguirUnoPorRuleta(resultado)
print(f"resultado -> {resultado}")

"""