import discord
from discord.ext import commands

from karen.discord.util import *

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
        message += "Explains the given command in greater detail."

    # !help eval
    elif inputString in ["eval", "comp"]:
        message += "**!eval [action sequence]**\n"
        message += "The eval command takes a sequence of actions and outputs the time taken to perform those actions, as well as the damage dealt by the combo."
        message += " Actions can optionally be separated by \">\" characters, spaces, or nothing at all."
        message += " For a list of recognised actions that can be included in a combo, use \"!list actions\".\n\n"
        message += "Multiple combos can be compared at a time by separating them with commas.\n\n"
        message += "The output of this command can also be modified by using parameters. For a list of all parameters, use \"!list params\"."
        message += " If no parameters are provided, defaults are taken from the user's preferences, which can be modified with the \"!prefs\" command."

    # !help tech
    elif inputString == "tech":
        message += "**!tech [tech name]**\n"
        message += "Gives a description of the requested tech and, where applicable, links a relevant YouTube video."
        message += " For a list of all recognised parameters, use \"!list techs\"."

    # !help list
    elif inputString == "list":
        message += "**!list [actions/combos/techs/params]**\n"
        message += "The list command can display:\n"
        message += "- all basic actions that are recognised by \"!eval\"\n"
        message += "- all named combos in the database\n"
        message += "- all techs recognised by \"!tech\"\n"
        message += "- all parameters that can be used with \"!eval\" and \"!params\"\n\n"
        message += "If no list is specified, the command will default to listing combos."

    # !help prefs
    elif inputString == "prefs":
        message += "**!prefs [params]**\n"
        message += "When the \"!eval\" command is used with no parameters specified, a default set of parameters are used. The prefs command allows a user to personalise their default parameters."
        message += " Any parameters listed in this command will become the default set for this user."
        message += " For a list of all parameters, use \"!list params\".\n\n"
        message += "Using only a blank \"--\" gives the original default parameters, whether it is used in \"!eval\" or \"!params\""
        message += " (ie. the user can reset their prefs via \"!prefs --\")."

    # !help help
    elif inputString == "help":
        message += "**!help [command]**\n"
        message += "The help command displays a detailed description of the requested command. If no command is given, it instead lists all commands, with brief descriptions included."

    # unknown command
    else:
        message += f"Unknown command \"!{inputString}\"."
        message += "\n\nYou can use \"!help\" for a list of all commands."
        colour = WARNING_COLOUR

    message += "\n\nSee the full documentation [here](https://github.com/EvilDuck14/Karen-2), or to report a bug contact [evilduck_](https://discordapp.com/users/233099051757731851)"

    # sending message
    try:
        messageEmbed: discord.Embed = discord.Embed(
            title="Help Desk",
            description=message,
            color=colour
        )
        messageEmbed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=messageEmbed)
    except Exception as e:
        print(e)