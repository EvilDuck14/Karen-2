import discord
from discord.ext import commands

from karen.ui.parseComboString import parseComboString
from karen.ui.preEval import preEval
from karen.ui.nameCombo import nameCombo
from karen.state import State

# causes ApplyAction functions to load
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
intents: discord.Intents = discord.Intents.default()
intents.guild_messages = True
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)
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
#                                                  Help                                                   #
#=========================================================================================================#

@bot.command()
async def help(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
            return

    inputString: str = " ".join(arr)
    print(f"\nreceived command: !help {inputString}")

    while (len(inputString) > 0) and (inputString[0] == "!"):
        inputString = inputString[1:]

    message: str = ""
    colour: int = INFO_COLOUR

    # !help
    if inputString.replace(" ", "") == "":
        message += "**!eval [action sequence]**\n"
        message += "Evaluates the time taken & damage dealt by a given combo.\n\n"

        message += "**!tech [tech name]**\n"
        message += "Outputs description of given tech.\n\n"

        message += "**!list [actions/combos/techs/params]**\n"
        message += "Displays a list of all documented items of the requested type.\n\n"

        message += "**!prefs [params]**\n"
        message += "Allows the user to set a default set of parameters to apply to their inputs.\n\n"

        message += "**!help [command]**\n"
        message += "Explains the given command in greater detail.\n\n"

        message += "To report a bug/issue, please contact user evilduck_"

    # !help eval
    elif inputString in ["eval", "comp"]:
        pass

    # !help help
    elif inputString == "help":
        pass

    # unknown command
    else:
        message += f"Unknown command \"!{inputString}\"."
        message += "\n\nYou can use \"!help\" for a list of all commands."
        colour = WARNING_COLOUR

    # sending message
    try:
        messageEmbed: discord.Embed = discord.Embed(
            title="Karen Help Desk",
            description=message,
            color=colour
        )
        messageEmbed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=messageEmbed)
    except Exception as e:
        print(e)

#=========================================================================================================#
#                                                  Eval                                                   #
#=========================================================================================================#

@bot.command()
async def eval(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
        return

    warningList: list[str] = []

    inputString: str = " ".join(arr)
    print(f"\nreceived command: !eval {inputString}")

    actionSequence: list[str] 
    params: dict[str, bool]
    actionSequence, params = parseComboString(inputString, warningList)
    print(f"interpreted action sequence as {actionSequence}")

    # single combo
    if not ("," in actionSequence):
        await singleEval(ctx, actionSequence, warningList, params)

    # combo comparison
    else:
        combos: list[list[str]] = [[]]
        for action in actionSequence:
            if action == ",":
                combos.append([])
            else:
                combos[-1].append(action)
        await comparisonEval(ctx, combos, warningList, params)

    # send warnings
    if not params["n"]:
        await sendWarnings(ctx, warningList)

async def singleEval(ctx: commands.context, actionSequence: list[str], warningList: list[str], params: dict[str, bool]):

    improvedActionSequence: list[str] = preEval(actionSequence, warningList, advancedMode=params["a"])
    if (len(actionSequence) != len(improvedActionSequence)) or (False in [actionSequence[i] == improvedActionSequence[i] for i in range(len(actionSequence))]):
        print(f"improved action sequence to {improvedActionSequence}")

    evalState: State = State(improvedActionSequence)
    warningList += evalState.getWarnings()

    # formatting
    title: str = nameCombo(improvedActionSequence)
    details: dict[str, str | int | float] = evalState.getComboDetails()
    message: str = f"> {details["sequence string"]}"
    if params["t"]:
        message += f"\n**Time:** {details["time seconds"]}s ({details["time frames"]}f)"
    if params["tfd"]:
        message += f"\n**Time From Damage:** {details["time from damage seconds"]}s ({details["time from damage frames"]}f)"
    if params["d"]:
        message += f"\n**Damage:** {details["damage"]}"
    if params["dps"]:
        message += f"\n**Damage Per Second:** {details["dps"]}"

    try:
        messageEmbed: discord.Embed = discord.Embed(
            title=title,
            description=message,
            color=EVAL_COLOUR
        )
        messageEmbed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=messageEmbed)
    except Exception as e:
        print(e)

    # breakdown mode only: send action log
    if (params["b"]) and (len(evalState.log) > 0):
        message: str = "```"
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

async def comparisonEval(ctx: commands.context, combos: list[list[str]], warningList: list[str], params: dict[str, bool]):

    numCombos: int = len(combos)
    sequences: list[str] = [""] * numCombos
    times: list[int] = [0] * numCombos
    timesFromDamage: list[int] = [0] * numCombos
    damages: list[int] = [0] * numCombos
    damagePerSeconds: list[int] = [0] * numCombos

    for index in range(numCombos):
        combos[index] = preEval(combos[index], warningList, advancedMode=params["a"])

        evalState: State = State(combos[index])
        warningList += evalState.getWarnings()
        details: dict[str, str | int | float] = evalState.getComboDetails()

        sequences[index] = details["sequence string"]
        times[index] = details["time frames"]
        timesFromDamage[index] = details["time from damage frames"]
        damages[index] = details["damage"]
        damagePerSeconds[index] = details["dps"]
        damagePerSeconds[index] = 0 if damagePerSeconds[index] == "NaN" else int(damagePerSeconds[index])

    message: str = ""
    for index in range(numCombos):
        message += f"> {index + 1}. {sequences[index]}"
        if numCombos > index + 1:
            message += "\nvs\n"

    if params["t"]:
        winValue = min(times)
        winners = [str(index + 1) for index in range(numCombos) if times[index] == winValue]
        message += f"\n\n**Time:** Combo{"s" if len(winners) > 1 else ""} {" & ".join(winners)}"
        message += "\n`" + " vs ".join(
            [(("🟢" if value == winValue else "🟥") + f" {value}f" + ("" if value == winValue else f" (+{abs(value - winValue)}f)")) for value in times]
        ) + "`"

    if params["tfd"]:
        winValue = min(timesFromDamage)
        winners = [str(index + 1) for index in range(numCombos) if timesFromDamage[index] == winValue]
        message += f"\n\n**Time From Damage:** Combo{"s" if len(winners) > 1 else ""} {" & ".join(winners)}"
        message += "\n`" + " vs ".join(
            [(("🟢" if value == winValue else "🟥") + f" {value}f" + ("" if value == winValue else f" (+{abs(value - winValue)}f)")) for value in timesFromDamage]
        ) + "`"

    if params["d"]:
        winValue = max(damages)
        winners = [str(index + 1) for index in range(numCombos) if damages[index] == winValue]
        message += f"\n\n**Damage:** Combo{"s" if len(winners) > 1 else ""} {" & ".join(winners)}"
        message += "\n`" + " vs ".join(
            [(("🟢" if value == winValue else "🟥") + f" {value}" + ("" if value == winValue else f" (-{abs(value - winValue)})")) for value in damages]
        ) + "`"

    if params["dps"]:
        winValue = max(damagePerSeconds)
        winners = [str(index + 1) for index in range(numCombos) if damagePerSeconds[index] == winValue]
        message += f"\n\n**Damage Per Second:** Combo{"s" if len(winners) > 1 else ""} {" & ".join(winners)}"
        message += "\n`" + " vs ".join(
            [(("🟢" if value == winValue else "🟥") + f" {value if value != 0 else "NaN"}" + ("" if (value == winValue or value == 0) else f" (-{abs(value - winValue)})")) for value in damagePerSeconds]
        ) + "`"

    try:
        messageEmbed: discord.Embed = discord.Embed(
            title="Combo Comparison",
            description=message,
            color=EVAL_COLOUR
        )
        messageEmbed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=messageEmbed)
    except Exception as e:
        print(e)

async def sendWarnings(ctx: commands.context, warningList: list[str]):
    if len(warningList) > 0:
        message: str = ""
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

@bot.command()
async def comp(ctx: commands.Context, *arr: str):
    await eval(ctx, *arr)

#=========================================================================================================#

# run bot
bot.run(BOT_TOKEN)