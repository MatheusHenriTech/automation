import discord

from discord.ext import commands
from discord import app_commands

from datetime import datetime, timedelta, timezone

from db.database import Session
from db.models import User
from db.helpers import get_user

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='profile')
    async def profile(self, interaction: discord.Interaction):

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


    @app_commands.command(name='daily')
    async def daily(self, interaction: discord.Interaction):

        with Session() as session:

            embed = discord.Embed(
                title='Daily awards',
                description='get your awards right now!',
                color=discord.Color.fuchsia()
            )

            usuario = get_user(session, interaction.user)

            current_time = datetime.now()

            if usuario.daily is not None:
                if current_time - usuario.daily < timedelta(hours=24):
                    embed.description=f"You already claimed your daily reward, you'll need to wait pass 24 hours since you had recue the daily awards "
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
            
            usuario.coins += 100
            usuario.daily = current_time
                
            session.commit()

            embed.description=f"You just won 100 coins\nNow you have {usuario.coins} coins"
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name='donate')
    async def donate_coins(self, interaction: discord.Interaction, receiver: discord.Member, coin:int):

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


    @app_commands.command(name='ranking')
    async def ranking(self, interaction: discord.Interaction):
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


async def setup(bot):
    await bot.add_cog(Economy(bot))