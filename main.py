import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

permissions = discord.Intents.default().all()
bot = commands.Bot(command_prefix='/', intents=permissions)

users = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Synchronized')

@bot.tree.command()
async def perfil(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id not in users:
        users[user_id] = {
            'coins':0
    }
        
    coins = users[user_id]['coins']

    embed = discord.Embed(
        title="title",
        color=discord.Color.fuchsia()
    )

    embed.add_field(
        name='Name:',
        value=interaction.user.display_name,
        inline=False
    )

    embed.add_field(
        name='ID:',
        value=user_id,
        inline=False
    )

    embed.add_field(
        name="Coins",
        value=coins,
        inline=False
    )  

    embed.set_thumbnail(
        url=interaction.user.avatar.url
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)
 
@bot.event
async def on_message(message):
    user_id = message.author.id
    if user_id not in users:
        users[user_id] = {
            'coins':0
        }

    coins = users[user_id]['coins']
    users[user_id]['coins']+=1
    
    await bot.process_commands(message)

@bot.tree.command()
async def daily(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Daily awards',
        description='get your awards right now!',
        color=discord.Color.fuchsia()
    )

    user_id = interaction.user.id

    if user_id not in users:
        users[user_id] = {
            'coins':0,
            'date':None
        }

    last_daily = users[user_id].get('date')
    now = datetime.now()
    if last_daily is not None and now - last_daily < timedelta(hours=24):
        embed.description="You've already got the daily coins bonus"
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    users[user_id]['coins'] += 100
    users[user_id]['date'] = now

    coins = users[user_id]['coins']

    embed.description=f"You just won 100 coins\nNow you have {coins} coins"
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command()
async def donate_coins(interaction: discord.Interaction, receiver: discord.Member, coin:int):
    embed = discord.Embed(
        title='Donate Coins',
        description='Here you can donate your coins',
        color=discord.Color.fuchsia()
    )

    user_id = interaction.user.id
    if user_id not in users:
        users[user_id] = {
            'coins':0
        }
    coins = users[user_id]['coins']
    if coin > coins or coin <= 0:
        embed.description = f"Sorry, You ain't donate this quantity of coins :/"
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    receiver_id = receiver.id
    if receiver.id not in users:
        users[receiver.id] = {
            'coins':0
        }
    users[user_id]['coins'] -= coin
    users[receiver_id]['coins'] += coin

    embed.description = f"You've just donated {coins} coins to {receiver}"
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command()
async def ranking(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Ranking',
        description='Ranking of the most rich users',
        color=discord.Color.fuchsia()
    )

    list_users = []
    ranking_text = []
    if users:
        for p in users.items():
            member = interaction.guild.get_member(p[0])
            coins = p[1]['coins']
            user = (member.display_name, coins)
            list_users.append(user)
            list_users.sort(key=lambda x: x[1], reverse=True)
        for nome, coins in list_users:
            txt = f'Name: {nome}\nCoins: {coins}'
            ranking_text.append(txt)
        final_text = '\n\n'.join(ranking_text)
        embed.description = final_text
        await interaction.response.send_message(embed=embed)
    else:
        embed.description='There no people here'
        await interaction.response.send_message(embed=embed)


