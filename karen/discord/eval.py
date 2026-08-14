import discord
from discord.ext import commands

from karen.discord.util import *
from karen.state.state import State
from karen.combos.parseComboString import parseComboString
from karen.combos.preEval import preEval
from karen.combos.nameCombo import nameCombo
from karen.discord.stats import logEval

async def singleEval(ctx: commands.Context, actionSequence: list[str], warningList: list[str], params: dict[str, bool]):

    improvedActionSequence: list[str] = preEval(actionSequence, warningList, advancedMode=params["a"])
    if (len(actionSequence) != len(improvedActionSequence)) or (False in [actionSequence[i] == improvedActionSequence[i] for i in range(len(actionSequence))]):
        print(f"improved action sequence to {improvedActionSequence}")

    if not DEV_MODE:
        logEval(improvedActionSequence)

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
    if params["ult"]:
        message += f"\n**Ult Charge Gained:** {details["ult charge gained"]}%"

    if type(ctx) == commands.Context:
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

    else:
        print(f"{"" if title == "" else f"\n{title}:"}\n{message.replace("**", "")}\n\n", end="")

    # breakdown mode only: send action log
    if (params["b"]) and (len(evalState.log) > 0):
        message: str = "```"
        for entry in evalState.log:
            message += f"\n[{entry.frame}] {entry.details}"
        message += "\n```"

        if type(ctx) == commands.Context:
            try:
                await ctx.send(embed=discord.Embed(
                    title="Breakdown",
                    description=message,
                    color=BREAKDOWN_COLOUR
                )
            )
            except Exception as e:
                print(e)

        else:
            print(f"Breakdown:\n{message[4:-4]}\n\n", end="")

async def comparisonEval(ctx: commands.Context, combos: list[list[str]], warningList: list[str], params: dict[str, bool]):

    numCombos: int = len(combos)
    sequences: list[str] = [""] * numCombos
    times: list[int] = [0] * numCombos
    timesFromDamage: list[int] = [0] * numCombos
    damages: list[int] = [0] * numCombos
    damagePerSeconds: list[int] = [0] * numCombos
    ultChargesGained: list[float] = [0] * numCombos

    for index in range(numCombos):
        combos[index] = preEval(combos[index], warningList, advancedMode=params["a"])

        if not DEV_MODE:
            logEval(combos[index])

        evalState: State = State(combos[index])
        warningList += evalState.getWarnings()
        details: dict[str, str | int | float] = evalState.getComboDetails()

        sequences[index] = details["sequence string"]
        times[index] = details["time frames"]
        timesFromDamage[index] = details["time from damage frames"]
        damages[index] = details["damage"]
        damagePerSeconds[index] = details["dps"]
        damagePerSeconds[index] = 0 if damagePerSeconds[index] == "NaN" else int(damagePerSeconds[index])
        ultChargesGained[index] = details["ult charge gained"]

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

    if params["ult"]:
        winValue = max(ultChargesGained)
        winners = [str(index + 1) for index in range(numCombos) if ultChargesGained[index] == winValue]
        message += f"\n\n**Ult Charge Gained:** Combo{"s" if len(winners) > 1 else ""} {" & ".join(winners)}"
        message += "\n`" + " vs ".join(
            [(("🟢" if value == winValue else "🟥") + f" {value}%" + ("" if value == winValue else f" (-{round(abs(value - winValue), 1)}%)")) for value in ultChargesGained]
        ) + "`"

    if type(ctx) == commands.Context:
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

    else:
        print(f"\nCombo Comparison:\n{message.replace("**", "").replace("`", "")}\n\n", end="")

async def eval(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
        return

    warningList: list[str] = []

    inputString: str = " ".join(arr)
    if type(ctx) == commands.Context:
        print(f"\nreceived command: !eval {inputString}")

    actionSequence: list[str] 
    params: dict[str, bool]
    actionSequence, params = parseComboString(ctx, inputString, warningList)
    if type(ctx) == commands.Context:
        print(f"interpreted action sequence as {actionSequence}")

    # multiple combos, discard empty
    combos: list[list[str]] = [[]]
    for action in actionSequence:
        if action == ",":
            combos.append([])
        else:
            combos[-1].append(action)
    combos = [combo for combo in combos if len(combo) > 0]
    if len(combos) == 0:
        combos = [[]]

    # single combo
    if len(combos) == 1:
        await singleEval(ctx, combos[0], warningList, params)

    # combo comparison
    else:
        await comparisonEval(ctx, combos, warningList, params)

    # send warnings
    if not params["n"]:
        await sendWarnings(ctx, warningList)