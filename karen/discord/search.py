import discord
from discord.ext import commands
import heapq

from karen.discord.util import *
from karen.state.state import State
from karen.combos.parseComboString import parseComboString
from karen.combos.preEval import preEval
from karen.combos.nameCombo import nameCombo
from karen.discord.stats import logEval

class candidateCombo:
    sequence: str
    time: int
    damage: int

    def __init__(self, sequence: str, time: int, damage: int):
        self.sequence = sequence
        self.time = time

    # comparison operators for sorting list by time
    def __lt__(self, other: candidateCombo) -> bool:
        return self.time < other.time
    def __le__(self, other: candidateCombo) -> bool:
        return self.time <= other.time
    def __gt__(self, other: candidateCombo) -> bool:
        return self.time > other.time
    def __ge__(self, other: candidateCombo) -> bool:
        return self.time >= other.time

async def search(ctx: commands.Context, *arr: str):
    if devModeMismatch(ctx):
        return

    inputString: str = " ".join(arr)
    if type(ctx) == commands.Context:
        print(f"\nreceived command: !eval {inputString}")

    numSequences: int = 1
    damageThreshold: int = 250
    timeFromDamage: bool = True
    allowedActions: list[str]

    comboQueue: list[candidateCombo] = [ candidateCombo("", 0, 0) ]
    successfulSequences: list[str] = []

    while len(successfulSequences) < numSequences:
        current: candidateCombo = heapq.heappop()
        sequence: str = current.sequence

        if current.damage >= damageThreshold:
            successfulSequences.append(sequence)
            if len(successfulSequences) >= numSequences:
                break

        for action in allowedActions:

            # don't chain swings or start a combo with a swing
            if (action in ["w", "a"]) and ((len(sequence) == 0) or (sequence[-1] in ["w", "a"])):
                continue

            newSequence: str = sequence + action
            warningList: list[str] = []

            try:
                actionList: list[str] = preEval(newSequence, warningList, advancedMode=True)
                newState: State = State(actionList)
                warningList += newState.getWarnings()

                if len(warningList) > 0:
                    continue

                # push to queue

            except Exception as e:
                continue