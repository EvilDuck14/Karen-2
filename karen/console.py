import asyncio

# causes ApplyAction functions to load
from karen.state.state import State
from karen.actions.basicActions import *
from karen.actions.earlyCancels import *
from karen.actions.movestacks import *

print("KAREN\n\n", end="")

# setting up commands
from karen.discord.eval import eval
from karen.discord.tech import tech
from karen.discord.list import list
from karen.discord.prefs import prefs
from karen.discord.help import help

async def runConsole():
    while True:
        print(">> ", end="")
        inputString = input()
        while (len(inputString) > 0) and (inputString[0] == "!"):
            inputString = inputString[1:]

        if inputString[:5] == "eval ":
            await eval(None, (inputString[5:]))

        elif inputString[:5] == "comp ":
            await eval(None, (inputString[5:]))

        elif inputString[:5] == "tech ":
            await tech(None, (inputString[5:]))

        elif inputString[:5] == "list ":
            await list(None, (inputString[5:]))

        elif inputString[:6] == "prefs ":
            await prefs(None, (inputString[6:]))

        elif inputString[:5] == "help ":
            await help(None, (inputString[5:]))

        else:
            print(f"\nCommand \"!{inputString[:inputString.find(" ")] if " " in inputString else inputString}\" not recognised. For a list of recognised commands, use !help.\n\n", end="")

asyncio.run(runConsole())