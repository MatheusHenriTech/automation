import discord

from discord.ext import commands
from discord import app_commands

from db.database import Session
from db.models import User
from db.helpers import get_user


CHANNEL_FEEDBACK = 1509993572525670430


class FeedbackModal(discord.ui.Modal, title="Feedback"):

    feedback_title = discord.ui.TextInput(label='Feedback_title', placeholder='Feedback title', required=True, max_length=50)

    sugestion = discord.ui.TextInput(label='Suggestions & Feedback', placeholder='Bug, suggestion, etc..', required=True, style=discord.TextStyle.long)


    async def on_submit(self, interact:discord.Interaction):

        channel = interact.guild.get_channel(CHANNEL_FEEDBACK)

        embed = discord.Embed(
            title='New feedback',
            color=discord.Color.purple()
        )

        embed.add_field(
            name='User',
            value=interact.user.mention,
            inline=False
        )

        embed.add_field(
            name='Title',
            value=self.feedback_title.value,
            inline=False
        )

        embed.add_field(
            name='Feedback',
            value=self.sugestion.value,
            inline=False
        )

        await channel.send(embed=embed)

        await interact.response.send_message(
            "The feedback was sent", ephemeral=True
        )


class Feedback(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @app_commands.command(name='feedback')
    async def feedback(self, interact: discord.Interaction):

        await interact.response.send_modal(
            FeedbackModal()
        )


async def setup(bot):
    await bot.add_cog(Feedback(bot))
