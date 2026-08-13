import discord
from discord.ext import commands

from karen.discord.util import *

async def prefs(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
            return

    inputString: str = " ".join(arr)
    print(f"\nreceived command: !prefs {inputString}")

    title: str = "Preferences"
    message: str = ""
    colour = INFO_COLOUR

    # TO DO
    message = "Command not yet implemented."
    colour = WARNING_COLOUR

    # sending message
    try:
        messageEmbed: discord.Embed = discord.Embed(
            title=title,
            description=message,
            color=colour
        )
        messageEmbed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=messageEmbed)
    except Exception as e:
        print(e)