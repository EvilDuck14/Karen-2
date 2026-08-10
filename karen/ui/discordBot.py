import discord
from discord.ext import commands

# getting environment variables
import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# bot runs in the dev channel iff the bot is in development mode
DEV_MODE = True
DEV_SERVER_ID = os.getenv("DEV_SERVER_ID")
DEV_CHANNEL_ID = os.getenv("DEV_CHANNEL_ID")
def devModeMismatch(ctx: commands.Context):
    return ((ctx.guild.id == DEV_SERVER_ID) and (ctx.channel.id == DEV_CHANNEL_ID)) ^ (not DEV_MODE)

# basic discord setup
intents = discord.Intents.default()
intents.guild_messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# prints to console on successful launch
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        await bot.tree.sync()
        print(f"successfully connected to {len(bot.guilds)} servers")
    except Exception as e:
        print(e)


#=========================================================================================================#
#                                                  Eval                                                   #
#=========================================================================================================#

from karen.ui.parseComboString import parseComboString
from karen.state import State
from karen.actions.basicActions import *
from karen.actions.earlyCancels import *
from karen.actions.movestacks import *

@bot.command()
async def eval(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
        return

    inputString: str = " ".join(arr)
    print(f"\nreceived command: !eval {inputString}")
    warningList: list[str] = []
    actionSequence = parseComboString(inputString, warningList)
    print(f"interpreted action sequence as {actionSequence}")
    evalState = State(actionSequence)
    warningList += evalState.getWarnings()

    # formatting
    message: str = ""
    # TO DO: sequence string
    message += f"\n**Time:** {evalState.lastDamageTime}f"
    message += f"\n**Time From Damage:** {0 if evalState.firstDamageTime == "unknown" else evalState.lastDamageTime - evalState.firstDamageTime}f"
    message += f"\n**Damage:** {evalState.damageDealt}"

    try:
        await ctx.send(embed=discord.Embed(
            title="Unknown Combo",
            description=message
        )
    )
    except Exception as e:
        print(e)

    # development mode only: send action log

    if not DEV_MODE:
        return

    message = "```"
    for entry in evalState.log:
        message += f"\n[{entry.frame}] {entry.details}"
    message += "\n```"

    try:
        await ctx.send(embed=discord.Embed(
            title="Debug log",
            description=message
        )
    )
    except Exception as e:
        print(e)

#=========================================================================================================#

# run bot
bot.run(BOT_TOKEN)