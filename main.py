import discord

from discord.ext import commands
from dotenv import load_dotenv

import asyncio
import os

from db.init_db import init_db

load_dotenv()

TOKEN = os.getenv("TOKEN")

permissions = discord.Intents.default().all()
bot = commands.Bot(command_prefix='/', intents=permissions)


async def main():

    init_db()

    async with bot:
        await bot.load_extension("cogs.economy")
        await bot.load_extension("cogs.events")
        await bot.load_extension("cogs.moderation")
        await bot.load_extension("cogs.casino")
        await bot.load_extension("cogs.modals")
        await bot.start(TOKEN)


asyncio.run(main())

