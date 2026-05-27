import discord

from discord.ext import commands

from db.database import Session
from db.helpers import get_user

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Synchronized')


    @commands.Cog.listener()
    async def on_member_join(self, member):
        with Session() as session:
            usuario = get_user(session, member)
            session.commit()
        await member.send('Welcome to the server')


async def setup(bot):
    await bot.add_cog(Events(bot))