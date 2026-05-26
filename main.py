import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from badwords import bad_words

load_dotenv()

TOKEN = os.getenv("TOKEN")

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


def get_user(session, discord_user):
    usuario = session.query(User).filter_by(
        user_id = str(discord_user.id)
    ).first()

    if not usuario:
        usuario = User(
            user_id = str(discord_user.id),
            username = discord_user.name,
            coins = 0
        )

        session.add(usuario)

    return usuario
    
Base.metadata.create_all(engine)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Synchronized')

@bot.event
async def on_member_join(member):
    with Session() as session:
        usuario = get_user(session, member)
        session.commit()
    await member.send('Welcome to the server')

list_messages = {}
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    badwords = bad_words
    text = message.content.lower()

    for word in text.split():
        if word in bad_words:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, Please, don't speak these type of words")
            return

    with Session() as session:
        
        usuario = get_user(session, message.author)

        user_id = message.author.id

        if user_id not in list_messages:
            list_messages[user_id] = []

        user_messages = list_messages[user_id]

        current_time = datetime.now(timezone.utc)
        user_messages.append(message.created_at)
        limit = current_time - timedelta(seconds=5)
        excluded_times = []

        for time in user_messages:
            if time < limit:
                excluded_times.append(time)

        for time_excluded in excluded_times:
            user_messages.remove(time_excluded)

        if len(user_messages) >= 7:
            await message.author.timeout(
                timedelta(minutes=1),
                reason="Spam detected"
            )

            await message.channel.send(f"{message.author.mention}, You just received a serious warning for spamming. You are muted for 1 minute")

        usuario.coins += 1
        session.commit()


    await bot.process_commands(message)


@bot.tree.command()
async def perfil(interaction: discord.Interaction):
    with Session() as session:

        usuario = get_user(session, interaction.user)

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
            value=usuario.user_id,
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

        session.commit()

        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command()
async def daily(interaction: discord.Interaction):

    with Session() as session:

        embed = discord.Embed(
            title='Daily awards',
            description='get your awards right now!',
            color=discord.Color.fuchsia()
        )

        usuario = get_user(session, interaction.user)

        actually_daily = datetime.now()

        if usuario.daily is not None:
            if actually_daily - usuario.daily < timedelta(hours=24):
                embed.description=f"You alreay have got the daily awards, you'll need to wait pass 24 hours since you had recue the daily awards "
                return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        usuario.coins += 100
        usuario.daily = actually_daily
            
        session.commit()

        embed.description=f"You just won 100 coins\nNow you have {usuario.coins} coins"
        await interaction.response.send_message(embed=embed, ephemeral=True)



@bot.tree.command()
async def donate_coins(interaction: discord.Interaction, receiver: discord.Member, coin:int):

    with Session() as session:

        usuario = get_user(session, interaction.user)
               
        embed = discord.Embed(
            title='Donate Coins',
            description='Here you can donate your coins',
            color=discord.Color.fuchsia()
        )

        if interaction.user.id == receiver.id:
            embed.description = "You can't donate coins to yourself."
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        coins_user = usuario.coins
        if coin > coins_user or coin <= 0:
            embed.description = f"You can't donate this amount of coins."
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        receiver_user = session.query(User).filter_by(
            user_id = str(receiver.id)
        ).first()


        if not receiver_user:
            embed.description = f"This user does not exist :/"
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        usuario.coins -= coin
        receiver_user.coins += coin

        session.commit()

        embed.description = f"You've just donated {coin} coins to {receiver_user.username}"
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command()
async def ranking(interaction: discord.Interaction):
    with Session() as session:
                
        embed = discord.Embed(
            title='Ranking',
            description='Ranking of the most rich users',
            color=discord.Color.fuchsia()
        )

        list_ranking = []
        list_user = session.query(User).order_by(User.coins.desc()).all()
        if list_user:
            for user in list_user:
                answer_ranking = f'User: {user.username}\nCoins: {user.coins}'
                list_ranking.append(f'{answer_ranking}')
            list_formated = '\n\n'.join(list_ranking)

            embed.description = list_formated
            await interaction.response.send_message(embed=embed)
        else:
            embed.description = f"There no people here"
            await interaction.response.send_message(embed=embed)

bot.run(TOKEN)