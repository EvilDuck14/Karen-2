import discord
from discord.ext import commands

from karen.ui.parseComboString import parseComboString, preEval
from karen.state import State
from karen.actions.basicActions import *
from karen.actions.earlyCancels import *
from karen.actions.movestacks import *

EVAL_COLOUR = 0x8C7FFF
DEV_LOG_COLOUR = 0x4480AA
WARNING_COLOUR = 0xB73A00
INFO_COLOUR = 0x77C6FF

# getting environment variables
import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# bot runs in the dev channel iff the bot is in development mode
DEV_MODE = True
DEV_SERVER_ID = int(os.getenv("DEV_SERVER_ID"))
DEV_CHANNEL_ID = int(os.getenv("DEV_CHANNEL_ID"))
def devModeMismatch(ctx: commands.Context):
    return bool((ctx.guild.id == DEV_SERVER_ID) and (ctx.channel.id == DEV_CHANNEL_ID)) ^ bool(DEV_MODE)

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

@bot.command()
async def eval(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
        return

    inputString: str = " ".join(arr)
    print(f"\nreceived command: !eval {inputString}")

    warningList: list[str] = []
    actionSequence = parseComboString(inputString, warningList)
    print(f"interpreted action sequence as {actionSequence}")
    actionSequence = preEval(actionSequence, warningList, advancedMode=False)

    evalState = State(actionSequence)
    warningList += evalState.getWarnings()

    # formatting
    details: dict[str, str | int] = evalState.getComboDetails()
    message: str = f"*{details["sequence string"]}*" if details["sequence string"] != "" else ""
    message += f"\n\n**Time:** {details["time seconds"]}s ({details["time frames"]}f)"
    message += f"\n**Time From Damage:** {details["time from damage seconds"]}s ({details["time from damage frames"]}f)"
    message += f"\n**Damage:** {details["damage"]}"

    try:
        await ctx.send(embed=discord.Embed(
            title="Unknown Combo",
            description=message,
            color=EVAL_COLOUR
        )
    )
    except Exception as e:
        print(e)

    # output warnings
    if len(warningList) > 0:
        message = ""
        for warning in warningList:
            message += f"**WARNING:** {warning}\n"
        message = message[:-1]

        try:
            await ctx.send(embed=discord.Embed(
                description=message,
                color=WARNING_COLOUR
            )
        )
        except Exception as e:
            print(e)

    # development mode only: send action log
    if len(evalState.log) > 0:
        message = "```"
        for entry in evalState.log:
            message += f"\n[{entry.frame}] {entry.details}"
        message += "\n```"

        try:
            await ctx.send(embed=discord.Embed(
                title="Debug log",
                description=message,
                color=DEV_LOG_COLOUR
            )
        )
        except Exception as e:
            print(e)

#=========================================================================================================#

# run bot
bot.run(BOT_TOKEN)