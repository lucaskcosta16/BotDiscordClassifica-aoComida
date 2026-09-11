import discord
from discord.ext import commands
from model import get_class

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Fizemos login como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Ola! Eu sou um bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh=5):
    await ctx.send("he" * count_heh)

@bot.command()
async def check(ctx):
    #verifica se ha arquivos anexados na mensagem
    if ctx.message.attachments:
        #percorrer as imagens anexadas e salvar cada uma delas
        for attachment in ctx.message.attachments:
            #pega o nome do arquivo
            filename = attachment.filename
            #pegar URL do arquivo
            file_url = attachment.url
            #mostrar no terminal que recebeu o arquivo
            print(f"Recebendo imagem: {filename} - URL: {file_url}")
            #salvar o arquivo localmente
            await attachment.save(f"./{attachment.filename}")
            #receber e salvar a imagem
            await ctx.send(f"Imagem ./{attachment.filename} recebida e salva com sucesso!")
            #fazer a previsão com o modelo
            class_name, confidence_score = get_class("./keras_model.h5", "./labels.txt", f"./{attachment.filename}")
            #enviar o resultado da previsão
            await ctx.send(f"Classe: {class_name} - Confiança: {confidence_score:.2f}")
    else:
        #se a lista de anexos estiver vazia, envia uma mensagem informando que não há imagens anexadas
        await ctx.send("Nenhuma imagem anexada na mensagem.")
            

bot.run("bote o token do seu bot aqui")
