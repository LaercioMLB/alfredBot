import discord
from discord.ext import commands
import random
from decouple import config
import asyncio
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


# Variáveis para controlar o estado do jogo IMPAR OU PAR
jogadores = {}  # Dicionário para armazenar as escolhas dos jogadores
jogo_em_andamento = False  # Variável para controlar se um jogo está em andamento


@client.event
async def on_member_join(member):
    principal = client.get_channel(1064346596856299540)
    regras = cclient.get_channel(1162776573682921535)
    mensagem = await principal.send("Bem vindo {member.mention}! Sou Alfred, o mordomo da casa. Leias as regras em {regras.mention}")

@bot.event
async def on_ready():
    print(f'Estou conectado como {bot.user.name} - {bot.user.id}')

#Comando limpar chat
@bot.command()
async def limpar(ctx, quantidade: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=quantidade + 1)
        await ctx.send(f"{quantidade} mensagens foram apagadas por {ctx.author.mention}.", delete_after=5)
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

#Repostas basicas do BOT
@bot.command()
async def teste(ctx):
    await ctx.send("Bot está no ar!")

@bot.command()
async def hello(ctx):
    await ctx.send("Olá!")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! {latency}ms")

#------------------------------------------------------------------------#

#JOGO IMPAR PAR
@bot.command()
async def parouimpar(ctx):
    global jogo_em_andamento

    if jogo_em_andamento:
        await ctx.send("Jogo em andamento. Aguarde o resultado ou cancele com !cancelarjogo.")
        return

    jogo_em_andamento = True
    jogador_id = ctx.author.id
    jogadores[jogador_id] = {'numero': None}
    
    # Envia a mensagem com os emojis dos números
    numeros_emojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    mensagem = await ctx.send("Clique no número desejado:")
    for i in range(10):
        await mensagem.add_reaction(numeros_emojis[i])

    await asyncio.sleep(10)  # Aguarda reações por 10 segundos

    mensagem = await ctx.fetch_message(mensagem.id)  # Atualiza a mensagem para obter reações

    # Filtra as reações dos jogadores
    for reacao in mensagem.reactions:
        if reacao.emoji in numeros_emojis:
            async for usuario in reacao.users():
                if usuario.id not in jogadores:
                    continue
                jogadores[usuario.id]['numero'] = numeros_emojis.index(reacao.emoji)

    # Verifica se dois jogadores escolheram números
    if len(jogadores) == 2:
        await inicia_jogo(ctx)
    else:
        await ctx.send("Não houve escolha suficiente. O jogo foi cancelado.")
        jogo_em_andamento = False
        jogadores.clear()

@bot.command()
async def cancelarjogo(ctx):
    global jogo_em_andamento

    if jogo_em_andamento:
        jogo_em_andamento = False
        jogadores.clear()
        await ctx.send("Jogo cancelado.")

@bot.command()
async def inicia_jogo(ctx):
    global jogo_em_andamento

    if len(jogadores) != 2:
        await ctx.send("Ainda não há jogadores suficientes para iniciar o jogo.")
        return

    jogadores_list = list(jogadores.values())
    numeros = [jogadores_list[0]['numero'], jogadores_list[1]['numero']]
    resultado = (sum(numeros) % 2 == 0)

    resultado_str = "par" if resultado else "ímpar"
    
    await ctx.send(f"Resultado: Jogador 1 escolheu o número {numeros[0]}.")
    await ctx.send(f"Resultado: Jogador 2 escolheu o número {numeros[1]}.")

    if resultado:
        await ctx.send("Par ganhou!")
    else:
        await ctx.send("Ímpar ganhou!")

    jogo_em_andamento = False
    jogadores.clear()

#------------------------------------------------------------------------#
token = config('TOKEN_SERVER')

if token is not None:
    bot.run(token)
else:
    print("A variável de ambiente 'TOKEN_SERVER' não está definida.")
