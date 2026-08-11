from karen.ui.comboData import *
from karen.state import State
from karen.actions.actionData import EARLY_CANCELS_NOT_ENABLED_BY

# returns the length of the combo string up to a character that necesarrily splits actions
INPUT_BREAKERS = [">", "+", "-", "["]
def getMaxNextInputLength(comboString: str) -> int:
    tryLength: int = len(comboString)
    for breaker in INPUT_BREAKERS:
        if breaker in comboString[:tryLength]:
            tryLength = comboString.find(breaker)
    return max(1, tryLength)

def logUnrecognised(unrecognised: str, warningList: list[str]) -> None:
    if unrecognised != "":
        warningList.append(f"unrecognised input \"{unrecognised}\"")

# entirely ignore anything in parentheses
def removeParentheses(string: str) -> str:
    while ("(" in string) and (")" in string[string.find("("):]):
        string = string[:string.find("(")] + string[(string.find("(") + string[string.find("("):].find(")") + 1):]
    string = string.replace("(", "").replace(")", "")
    return string

def is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def parseComboString(comboString: str, warningList: list[str]) -> list[str]:
    actionSequence: list[str] = []
    comboString = removeParentheses(comboString)

    # remove white space
    comboString = comboString.replace(" ", "")

    # store unrecognised sequences of characters, cuts off and resets when a recognised action is found
    unrecognised: str = ""

    while len(comboString) > 0:

        # wait inputs
        if comboString[0] == "[":
            logUnrecognised(unrecognised, warningList)
            unrecognised = ""
            if "]" in comboString:
                bracketContents: str = comboString[1:comboString.find("]")]
                print(bracketContents)
                if bracketContents.isnumeric():
                    actionSequence.append(f"[{bracketContents}f]")
                elif bracketContents[:-1].isnumeric() and (len(bracketContents) > 0) and (bracketContents[-1] in ["f", "T", "B"]):
                    actionSequence.append(f"[{bracketContents}]")
                elif is_float(bracketContents[:-1]) and (len(bracketContents) > 0) and (bracketContents[-1] == "s"):
                    actionSequence.append(f"[{bracketContents}]")
                else:
                    warningList.append(f"invalid wait duration \"{bracketContents}\"")
                comboString = comboString[(comboString.find("]") + 1):]
            else:
                warningList.append("bracket not closed")
                comboString = comboString[1:]
            continue

        if comboString[0] == ">":
            logUnrecognised(unrecognised, warningList)
            unrecognised = ""
            comboString = comboString[1:]
            continue

        # check the next input against known combo names
        tryLength: int = getMaxNextInputLength(comboString)
        while(tryLength > 1):
            if comboString[:tryLength].lower() in COMBO_NAMES.keys():
                logUnrecognised(unrecognised, warningList)
                unrecognised = ""
                actionSequence += COMBO_NAMES[comboString[:tryLength].lower()]
                comboString = comboString[tryLength:]
                tryLength = 0
                break
            tryLength -= 1
        if tryLength == 0:
            continue

        # check the next input against known action names
        tryLength: int = getMaxNextInputLength(comboString)
        while(tryLength > 1):
            if comboString[:tryLength].lower() in COMBO_ACTION_NAMES.keys():
                logUnrecognised(unrecognised, warningList)
                unrecognised = ""
                actionSequence += COMBO_ACTION_NAMES[comboString[:tryLength].lower()]
                comboString = comboString[tryLength:]
                tryLength = 0
                break
            tryLength -= 1
        if tryLength == 0:
            continue

        # check if the next character is an action symbol
        if comboString[0] in COMBO_ACTION_SYMBOLS.keys():
            logUnrecognised(unrecognised, warningList)
            unrecognised = ""
            actionSequence += COMBO_ACTION_SYMBOLS[comboString[0]]
            comboString = comboString[1:]
            continue

        # failed to recognise any action - push the first character to the unrecognised string and move on
        else:
            unrecognised += comboString[0]
            comboString = comboString[1:]
    logUnrecognised(unrecognised, warningList)
    unrecognised = ""

    # join movestacks / early cancels
    tempActionSequence = actionSequence
    actionSequence = []
    while len(tempActionSequence) > 0:

        # movestacks
        if tempActionSequence[0] == "+":

            # no previous/following action
            if (len(actionSequence) == 0) or (len(tempActionSequence) == 1):
                break

            else:
                actionSequence[-1] += "+" + tempActionSequence[1]
                tempActionSequence = tempActionSequence[2:]

        # early cancels
        elif tempActionSequence[0] == "-":

            # no previous/following action
            if (len(actionSequence) == 0) or (len(tempActionSequence) == 1):
                break

            # early cancel valid
            if ((actionSequence[-1] + "-") in State.ApplyAction.keys()) and not (tempActionSequence[1] in EARLY_CANCELS_NOT_ENABLED_BY[actionSequence[-1]]):
                actionSequence[-1] += "-"
                tempActionSequence = tempActionSequence[1:]

            # early cancel invalid
            else:
                warningList.append(f"unrecognised early cancel \"{actionSequence[-1]}-{tempActionSequence[1]}\"")
                tempActionSequence = tempActionSequence[1:]

        else:
            actionSequence.append(tempActionSequence[0])
            tempActionSequence = tempActionSequence[1:]

    # extra pass to check that movestacks are valid
    tempActionSequence = actionSequence
    actionSequence = []
    for action in tempActionSequence:
        if (action in State.ApplyAction.keys()) or (action[0] == "["):
            actionSequence.append(action)

        else:
            warningList.append(f"unrecognised movestack \"{action}\"")
            actionSequence += action.split("+")

    return actionSequence

from karen.actions.actionData import ACTION_NAMES, ANIMATION_CANCEL_TIMES

# replaces suboptimal inputs / typos and raises warnings for sequence errors
def preEval(actionSequence: list[str], warningList: list[str], advancedMode: bool = False):
    improvedActionSequence: list[str] = []

    while len(actionSequence) > 0:

        # automatic swing whiff insertion
        if (not advancedMode) and (len(improvedActionSequence) > 0):

            # skip for wait action
            if (improvedActionSequence[-1][0] == "[") or (actionSequence[0][0] == "["):
                pass   

            # skip if last animation was an early cancel
            elif (improvedActionSequence[-1][-1] == "-"):
                pass        

            # don't use a swing whiff if one action is explosion
            elif (improvedActionSequence[-1] == "E") or (actionSequence[0] == "E"):
                pass

            # don't use a swing whiff to speed up clap/bomb > melee or clap > bomb
            elif (improvedActionSequence[-1] in ["C", "B"]) and (actionSequence[0][0] in ["p", "k", "o", "B"]):
                pass

            # don't use a swing whiff to speed up symbiote > symbiote
            elif (improvedActionSequence[-1] in ["S", "V"] and actionSequence[0] in ["S", "V"]):
                pass

            # otherwise, insert swing whiff if it speeds up the combo
            else:
                nextActionType = actionSequence[0][0].replace("k", "p").replace("w", "s").replace("a", "s").replace("G", "g").replace("b", "B")
                if (ANIMATION_CANCEL_TIMES[improvedActionSequence[-1][-1]]["s"] + ANIMATION_CANCEL_TIMES["w"][nextActionType] < ANIMATION_CANCEL_TIMES[improvedActionSequence[-1][-1]][nextActionType]):
                    warningList.append(f"automatically weaved swing whiff between {ACTION_NAMES[improvedActionSequence[-1]]} and {ACTION_NAMES[actionSequence[0]]}")
                    improvedActionSequence.append("w")
        
        improvedActionSequence.append(actionSequence[0])
        actionSequence = actionSequence[1:]

    return improvedActionSequence