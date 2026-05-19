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
        color=discord.Color.darker_grey()
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
    user_id = interaction.user.id
    last_daily = datetime.now()

    if user_id not in users:
        users[user_id] = {
            'coins':0
        }

    users[user_id]['date'] = last_daily
    if datetime.now() - last_daily <= timedelta(hours=24):
        await interaction.response.send_message(f"You've already got the daily coins bonus", ephemeral=True)
    else:
        users[user_id]['coins'] += 100
        coins = users[user_id]['coins']

        await interaction.response.send_message(f'You just won 100 coins\nNow you have {coins} coins', ephemeral=True)

@bot.tree.command()
async def share_coins(interaction: discord.Interaction, receiver: discord.Member, coin:int):
    user_id = interaction.user.id
    if user_id not in users:
        users[user_id] = {
            'coins':0
        }
    coins = users[user_id]['coins']
    if coin > coins or coin <= 0:
        await interaction.response.send_message(f"Sorry, You ain't share this quantity of coins :/", ephemeral=True)
        return
    receiver_id = receiver.id
    if receiver.id not in users:
        users[receiver.id] = {
            'coins':0
        }
    users[user_id]['coins'] -= coin
    users[receiver_id]['coins'] += coin

    await interaction.response.send_message(f"You've just donated {coin} coins to {receiver}")



bot.run("MTUwNDI0MjEzMDg5NjI5MzkzOQ.G_IbOR.uXax0-a-umP-S0_uAwrxzyIde4try-6t52U5vE")