import os
from discord.ext import commands

EVAL_COLOUR = 0x8C7FFF
BREAKDOWN_COLOUR = 0x4480AA
WARNING_COLOUR = 0xB73A00
INFO_COLOUR = 0x77C6FF

DEV_MODE = True
DEV_SERVER_ID = int(os.getenv("DEV_SERVER_ID"))
DEV_CHANNEL_ID = int(os.getenv("DEV_CHANNEL_ID"))
def devModeMismatch(ctx: commands.Context):
    return bool((ctx.guild.id == DEV_SERVER_ID) and (ctx.channel.id == DEV_CHANNEL_ID)) ^ bool(DEV_MODE)