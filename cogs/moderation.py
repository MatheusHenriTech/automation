import discord

from discord.ext import commands
from datetime import datetime, timedelta, timezone

from utils.bad_words import bad_words

from db.database import Session
from db.helpers import get_user

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.list_messages = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        text = message.content.lower()

        for word in text.split():
            if word in bad_words:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, Please, don't speak these type of words")
                return

        with Session() as session:
            
            usuario = get_user(session, message.author)

            user_id = message.author.id

            if user_id not in self.list_messages:
                self.list_messages[user_id] = []

            user_messages = self.list_messages[user_id]

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

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(Moderation(bot))