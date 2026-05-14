import discord
from discord.ext import commands
import os

class Bot_modificado(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=discord.Intents.all())
    async def setup_hook(self):
        self.add_view(View_persistente())
bot=Bot_modificado()

async def carregar_cogs():
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f'cogs.{arquivo[:-3]}')
    

@bot.event
async def on_ready():
    await carregar_cogs()
    print("Estou pronto!")

@bot.command()
async def ola(ctx:commands.Context):
    usuario = ctx.author
    canal = ctx.channel
    await ctx.reply(f"Olá, {usuario.display_name}\nVocê está no canal: {canal.name}")


@bot.command()
async def falar(ctx:commands.Context, *,frase):
    await ctx.send(frase)

@bot.command()
async def enviar_embed(ctx:commands.Context):
    meu_embed=discord.Embed(title='Olá, Mundo!', description='Descrição :D')
    
    imagem_arquivo=discord.File('imagens/logo_metro.png', 'logo_metro.png')
    meu_embed.set_image(url="attachment://logo_metro.png")

    thumb_arquivo=discord.File('imagens/fundo-tropical.png', 'fundo-tropial.png')
    meu_embed.set_thumbnail(url="attachment://fundo-tropical.png")

    meu_embed.set_footer(text='Este é o footer')
    meu_embed.color=discord.Color.purple()

    meu_embed.add_field(name='Moedas', value=10, inline=False)
    meu_embed.add_field(name='Filme Favorito', value='DBS: Broly', inline=False)
    meu_embed.add_field(name='Rank', value='Prata', inline=False)

    await ctx.reply(files=[imagem_arquivo, thumb_arquivo],embed=meu_embed)

@bot.command()
async def enviar_botao(ctx:commands.Context):
    async def resposta_botao(interact:discord.Interaction):
        await interact.response.send_message('Botão Pressionado')
        await interact.followup.send('Botão Pressionado de novo')

    view = discord.ui.View()
    botao = discord.ui.Button(label='Botão', style=discord.ButtonStyle.green)
    botao.callback=resposta_botao

    botao_url=discord.ui.Button(label='Meu canal', url='https://www.google.com.br/maps')

    view.add_item(botao)
    view.add_item(botao_url)
    await ctx.reply(view=view)



@bot.command()
async def jogo_favorito(ctx:commands.Context):
    async def select_resposta(interact:discord.Interaction):
        escolha=interact.data['values'][0]
        jogos={'1':'Minecraft', '2':'GTA V', '3':'Mario'}
        jogo_escolhido = jogos[escolha]
        await interact.response.send_message(f'Você escolheu {jogo_escolhido}')


    menuSelecao=discord.ui.Select(placeholder='Selecione uma opção')
    opcoes=[
        discord.SelectOption(label='Minecraft', value='1'),
        discord.SelectOption(label='GTA V', value='2'),
        discord.SelectOption(label='Mario', value='3')
    ]
    menuSelecao.options=opcoes
    menuSelecao.callback=select_resposta

    view = discord.ui.View()
    view.add_item(menuSelecao)
    await ctx.send(view=view)

@bot.event
async def on_guild_channel_create(canal:discord.abc.GuildChannel):
    await canal.send(f"Novo canal criado: {canal.name}")

@bot.event
async def on_member_join(membro:discord.Member):
    canal = bot.get_channel(1504583787949068449)
    meu_embed = discord.Embed(title=f'Bem vindo, {membro.name}!')
    meu_embed.description='Aproveite a estadia!'
    meu_embed.set_thumbnail(url=membro.avatar)

    await canal.send(embed=meu_embed)

@bot.event
async def on_member_remove(membro:discord.Member):
    canal = bot.get_channel(1504583787949068449)
    await canal.send(f"{membro.display.name} Saiu do servidor...\nAté breve")

class View_persistente(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label='me aperte', custom_id='botao')
    async def botao(self, interact:discord.Interaction, button):
        await interact.response.send_message('O botão foi pressionado')

@bot.command()
async def gugu(ctx:commands.Context):
    await ctx.reply(view=View_persistente())


bot.run("MTUwNDI0MjEzMDg5NjI5MzkzOQ.GJPXlp.hWXBGyPVBs2GWcGz4Ytiu4uNnbprDQaiq0Efj4")