import discord
from discord.ext import commands, tasks
from datetime import time

intents=discord.Intents.all()
bot=commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    sincs = await bot.tree.sync()
    print(f'{len(sincs)} comandos sincronizados!')
    enviar_mensagem.start()
    print("Bot inicializado com sucesso")


@bot.event
async def on_message(msg:discord.Message):
    if msg.author.bot:
        return
    await bot.process_commands(msg)
    # await msg.reply(f"O usuário {msg.author.mention} enviou uma mensagem no canal {msg.channel.name}")


@bot.event
async def on_member_join(membro:discord.Member):
    canal=bot.get_channel(1504252572502986902)
    await canal.send(f"{membro.mention} entrou no servidor")


@bot.event
async def on_reaction_add(reacao:discord.Reaction, membro:discord.Member):
    await reacao.message.reply(f"O membro {membro.name} reagiou a mensagem com {reacao.emoji}")
    

@bot.command()
async def somar(ctx:commands.Context, num1:float, num2:float):
    resultado = num1 + num2
    await ctx.send(f"A soma entre {num1} e {num2} é igual a {resultado}")


@bot.command()
async def enviar_embed(ctx:commands.Context):
    minha_embed = discord.Embed()
    minha_embed.title = "Titulo da embed"
    minha_embed.description = "Descrição da embed"

    imagem=discord.File("imagens/logo_metro.png", "logo_metro.png")
    minha_embed.set_image(url="attachment://logo_metro.png")
    minha_embed.set_thumbnail(url="attachment://logo_metro.png")

    minha_embed.set_footer(text="Esse é o footer da minha embed!")

    minha_embed.set_author(name="Goku", icon_url="https://scc10.com.br/wp-content/uploads/2025/12/Instinto-Superior-Goku-Manga-vs-Anime.webp", url="https://www.google.com.br/maps")

    await ctx.reply(embed=minha_embed, file=imagem)


@tasks.loop(time=time(20, 7))
async def enviar_mensagem():
    canal=bot.get_channel(1504242634233745450)
    await canal.send("Mensagem programada por horário (USA)")


@bot.tree.command()
async def ola(interact:discord.Interaction):
    await interact.response.defer()
    await interact.followup.send("Pronto")

@bot.tree.command()
async def falar(interact:discord.Interaction, texto:str):
    await interact.response.send_message(texto)


@bot.tree.command()
async def somar(interact:discord.Interaction, num1:int, num2:int):
    resultado=num1+num2
    await interact.response.send_message(f"O resultado de {num1} + {num2} é igual a {resultado}")

@bot.tree.command()
async def selecionar_membro(interact:discord.Interaction, membro:discord.Member):
    await interact.response.send_message(f"Você selecionou o usuário {membro.mention}")


bot.run("MTUwNDI0MjEzMDg5NjI5MzkzOQ.G9bTFw.Lk4g1xnLQvnwiJ2U5Tz8NobARuAlPaplWqsNmc")
