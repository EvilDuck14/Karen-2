import json
import os
from pathlib import Path
import discord
from discord.ext import commands

from karen.discord.util import *

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = Path(str(PROJECT_ROOT) + "/data/prefs.json")
os.makedirs(DATA_PATH.parent, exist_ok=True)
if not DATA_PATH.exists():
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump({}, f)

userPrefs: dict[int, dict[str, bool]]
with DATA_PATH.open("r", encoding="utf-8") as f:
    userPrefs = json.load(f)

PARAMS = {
    "a" : "Advanced mode (don't automatically fix combo)",
    "b" : "Show breakdown",
    "n" : "No warnings",
    "t" : "Display time",
    "tfd" : "Display time from damage",
    "d" : "Display damage",
    "dps" : "Display damage per second",
    "ult" : "Display ult charge generation"
}

DEFAULT_PARAMS = {
    "a" : False,
    "b" : False,
    "n" : False,
    "t" : True,
    "tfd" : True,
    "d" : True,
    "dps" : False,
    "ult" : False
}

def getUserPrefs(userId: int) -> dict[str, bool]:
    if str(userId) in userPrefs.keys():
        return userPrefs[str(userId)].copy()
    else:
        return DEFAULT_PARAMS.copy()

# separates parameters from the rest of the input
def extractParams(ctx: commands.Context, inputString: str, warningList: list[str]) -> tuple[str, dict[str, bool]]:

    # default parameters
    params: dict[str, bool] = DEFAULT_PARAMS.copy()

    # load user prefs if no params given
    if (type(ctx) == commands.Context) and not ("--" in inputString):
        params = getUserPrefs(ctx.author.id)

    # the first time a display parameter is changed, set all others to false
    displayChanged: bool = False

    # shorten sequences of dashes to 2 in a row
    while "---" in inputString:
        inputString = inputString.replace("---", "--")

    # symbols that automatically end parameter input field
    inputString = inputString.replace(">", " >").replace(",", " ,").replace("--", " --")

    # search for parameters
    words: list[str] = inputString.split(" ")
    filteredString: str = ""
    for word in words:
        if "--" in word:

            if (len(word) == 2):
                continue

            # parameter not recognised
            if not (word[2:] in params.keys()):
                warningList.append(f"parameter not recognised \"{word}\"")
                continue

            if (not displayChanged) and (word[2:] in ["t", "tfd", "d", "dps", "ult"]):
                displayChanged = True
                params["t"] = False
                params["tfd"] = False
                params["d"] = False
                params["dps"] = False
                params["ult"] = False

            params[word[2:]] = True
            
        else:
            filteredString += word

    return filteredString, params

async def prefs(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
        return

    if type(ctx) != commands.Context:
        print("\nSaving preferences is not supported in local mode.\n\n", end="")
        return

    inputString: str = " ".join(arr)
    print(f"\nreceived command: !prefs {inputString}")

    if inputString in ["reset", "r", "default"]:
        inputString = ""

    title = f"{ctx.author} Preferences Updated"
    message: str = ""

    processedString: str = "--" + inputString
    processedString = "--".join(processedString.split(" "))
    processedString = "--".join(processedString.split(">"))
    processedString = "--".join(processedString.split(","))

    warningList: list[str] = []
    params: dict[str, bool] 
    _, params = extractParams(ctx, processedString, warningList)

    userPrefs[str(ctx.author.id)] = params
    isDefault = not (False in [params[key] == DEFAULT_PARAMS[key] for key in DEFAULT_PARAMS.keys()])
    if isDefault:
        title = f"{ctx.author} Preferences Reset"
        userPrefs.pop(str(ctx.author.id), None)

    with DATA_PATH.open("w", encoding="utf-8") as f:
        f.write(json.dumps(userPrefs, indent=4))
    
    for key in params.keys():
        message += f"- {PARAMS[key]} = {params[key]}\n"
    message = message[:-1]

    # sending message
    try:
        messageEmbed: discord.Embed = discord.Embed(
            title=title,
            description=message,
            color=INFO_COLOUR
        )
        messageEmbed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=messageEmbed)
        await sendWarnings(ctx, warningList)
    except Exception as e:
        print(e)