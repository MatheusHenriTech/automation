import discord

from discord.ext import commands
from discord import app_commands

from db.database import Session
from db.models import User
from db.helpers import get_user

from random import choices

class Casino(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='open_treasure')
    async def open_treasure(self, interaction: discord.Interaction, coins:int):

        with Session() as session:
            usuario = get_user(session, interaction.user)

            options = [
                ("Lost it all",0),
                ("Lost half",0.5),
                ("Draw",1),
                ("Doubled",2),
                ("JACKPOT Tripled",3)
            ]

            weights = [35, 20, 25, 18, 2]

            choice = choices(options, weights=weights, k=1)[0]

            message = choice[0]
            multiplicator = choice[1]

            gain = int(coins * multiplicator)

            await interaction.response.send_message(f"Sorte ou azar?, {message } você transformou {coins} coins em {gain} coins")

            usuario.coins -= coins
            usuario.coins += gain

            session.commit()


async def setup(bot):
    await bot.add_cog(Casino(bot))

