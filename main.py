import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timedelta

engine = create_engine("sqlite:///database.db")

Session = sessionmaker(engine)
Base = declarative_base()

permissions = discord.Intents.default().all()
bot = commands.Bot(command_prefix='/', intents=permissions)

users = {}

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    username = Column(String)
    coins = Column(Integer, default=0)
    daily = Column(DateTime, default=None)
    
Base.metadata.create_all(engine)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Synchronized')

 
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    session = Session()

    usuario = session.query(User).filter_by(
        user_id = str(message.author.id)
    ).first()

    if not usuario:
        usuario = User(
            user_id = str(message.author.id),
            username = message.author.name,
            coins=0
        )

        session.add(usuario)

    usuario.coins += 1
    session.commit()


    await bot.process_commands(message)


@bot.tree.command()
async def perfil(interaction: discord.Interaction):
    
    session = Session()

    usuario = session.query(User).filter_by(
        user_id = str(interaction.user.id)
    ).first()

    if not usuario:
        usuario = User(
            user_id=interaction.user.id,
            username=interaction.user.name,
            coins=0
        )

    embed = discord.Embed(
        title="title",
        color=discord.Color.fuchsia()
    )

    embed.add_field(
        name='Name:',
        value=usuario.username,
        inline=False
    )

    embed.add_field(
        name='ID:',
        value=usuario.id,
        inline=False
    )

    embed.add_field(
        name="Coins",
        value=usuario.coins,
        inline=False
    )  

    embed.set_thumbnail(
        url=interaction.user.avatar.url
    )

    session.add(usuario)
    session.commit()

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command()
async def daily(interaction: discord.Interaction):

    session = Session()

    embed = discord.Embed(
        title='Daily awards',
        description='get your awards right now!',
        color=discord.Color.fuchsia()
    )

    usuario = session.query(User).filter_by(
        user_id = str(interaction.user.id)
    ).first()

    if not usuario:
        usuario = User(
            user_id=interaction.user.id,
            username=interaction.user.name,
            coins=0
        )

    actually_daily = datetime.now()

    if usuario.daily is not None:
        if actually_daily - usuario.daily < timedelta(hours=24):
            embed.description=f"You alreay have got the daily awards, you'll need to wait pass 24 hours since you had recue the daily awards "
            return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    usuario.coins += 100
    usuario.daily = actually_daily
        
    session.add(usuario)
    session.commit()

    embed.description=f"You just won 100 coins\nNow you have {usuario.coins} coins"
    await interaction.response.send_message(embed=embed, ephemeral=True)



@bot.tree.command()
async def donate_coins(interaction: discord.Interaction, receiver: discord.Member, coin:int):

    session = Session()

    usuario = session.query(User).filter_by(
        user_id = str(interaction.user.id)
    ).first()

    if not usuario:
        usuario = User(
            user_id=interaction.user.id,
            username=interaction.user.name,
            coins=0    
        )
        
    
    embed = discord.Embed(
        title='Donate Coins',
        description='Here you can donate your coins',
        color=discord.Color.fuchsia()
    )

    coins_user = usuario.coins
    if coin > coins_user or coin <= 0:
        embed.description = f"Sorry, You ain't donate this quantity of coins :/"
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    receiver_user = session.query(User).filter_by(
        user_id = str(receiver.id)
    ).first()

    if not receiver_user:
        embed.description = f"This user does not exist :/"
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    usuario.coins -= coin
    receiver_user.coins += coin

    session.add(usuario)
    session.commit()

    embed.description = f"You've just donated {coin} coins to {receiver_user.username}"
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command()
async def ranking(interaction: discord.Interaction):

    session = Session()

    usuario = session.query(User).filter_by(
        user_id = str(interaction.user.id)
    ).first()

    if not usuario:
        usuario = User(
            user_id=interaction.user.id,
            username=interaction.user.name,
            coins=0      
        )
        
    embed = discord.Embed(
        title='Ranking',
        description='Ranking of the most rich users',
        color=discord.Color.fuchsia()
    )

    list_ranking = []
    list_user = session.query(User).order_by(User.coins.desc()).all()
    for user in list_user:
        name_user= f'User: {user.username}'
        coin_user = f'Coins: {user.coins}\n'
        answer_ranking = f'User: {user.username}\nCoins: {user.coins}'
        list_ranking.append(f'{answer_ranking}')
    list_formated = '\n\n'.join(list_ranking)
    session.add(usuario)
    session.commit()

    embed.description = list_formated
    await interaction.response.send_message(embed=embed)


bot.run("MTUwNDI0MjEzMDg5NjI5MzkzOQ.GKJ9KW.7Jqs0KN8qhVSKdYjACHF-F35BsmNZIUehQmcso")