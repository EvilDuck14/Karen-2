import discord
from discord.ext import commands

from karen.discord.util import *
from karen.actions.actionData import ACTION_NAMES
from karen.combos.comboData import COMBO_NAMES
from karen.discord.tech import TECHS
from karen.discord.prefs import PARAMS

async def list(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
        return

    inputString: str = " ".join(arr)
    print(f"\nreceived command: !list {inputString}")

    title: str = "List"
    message: str = "```"
    colour = INFO_COLOUR

    if inputString.lower().replace(" ", "") in ["actions", "action", "attacks", "attack", "inputs", "input", "moves", "move", "a", "i", "m"]:
        title = "Action List"
        spacing: int = max([len(symbol) for symbol in ACTION_NAMES.keys()])
        for symbol in ACTION_NAMES.keys():
            if symbol in ["T", "s"]:
                continue
            message += f"\n{symbol}{"".join([" "] * (spacing - len(symbol)))} | {ACTION_NAMES[symbol]}"
        message += "\n```"

    elif inputString.lower().replace(" ", "") in ["combos", "combo", "c", ""]:
        title = "Combo List"
        spacing: int = max([len(sequence) for sequence in COMBO_NAMES.keys()])
        for sequence in COMBO_NAMES.keys():
            message += f"\n{sequence}{"".join([" "] * (spacing - len(sequence)))} | {COMBO_NAMES[sequence]}"
        message += "\n```"

    elif inputString.lower().replace(" ", "") in ["techs", "tech", "t"]:
        title = "Tech List"
        for techName in TECHS.keys():
            message += f"\n{techName}"
        message += "\n```"

    elif inputString.lower().replace(" ", "") in ["params", "param", "parameters", "parameter", "prefs", "pref", "preferences", "preference", "settings", "setting", "p", "s"]:
        title = "Parameter List"
        spacing: int = max([len(key) for key in PARAMS.keys()])
        for key in PARAMS.keys():
            message += f"\n--{key}{"".join([" "] * (spacing - len(key)))} | {PARAMS[key]}"
        message += "\n```"

    else:
        message = f"Unrecognised list type \"{inputString}\""
        colour = WARNING_COLOUR

    # sending message
    if type(ctx) == commands.Context:
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

    else:
        print(f"\n{title}:\n\n{message.replace("**", "").replace("`", "")}\n\n", end="")