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
    return tryLength

def logUnrecognised(unrecognised: str, warningList: list[str]) -> None:
    if unrecognised != "":
        warningList.append(f"unrecognised input \"{unrecognised}\"")
    unrecognised = ""

def parseComboString(comboString: str, warningList: list[str]) -> list[str]:
    actionSequence: list[str] = []

    # entirely ignore anything in parentheses
    while ("(" in comboString) and (")" in comboString[comboString.find("("):]):
        comboString = comboString[:comboString.find("(")] + comboString[(comboString.find("(") + comboString[comboString.find("("):].find(")") + 1):]
    comboString = comboString.replace("(", "").replace(")", "")

    # remove white space
    comboString = comboString.replace(" ", "")

    # store unrecognised sequences of characters, cuts off and resets when a recognised action is found
    unrecognised: str = ""

    while len(comboString) > 0:

        # wait inputs
        if comboString[0] == "[":
            logUnrecognised(unrecognised, warningList)
            if "]" in comboString:
                bracketContents = comboString[1:comboString.find("]")] # TO DO: implement
                comboString = comboString[(comboString.find("]") + 1):]
            else:
                warningList.append("bracket not closed")
                comboString = comboString[1:]
            continue

        if comboString[0] == ">":
            logUnrecognised(unrecognised, warningList)
            comboString = comboString[1:]
            continue

        # check the next input against known combo names
        tryLength: int = getMaxNextInputLength(comboString)
        while(tryLength > 1):
            if comboString[:tryLength].lower() in COMBO_NAMES.keys():
                logUnrecognised(unrecognised, warningList)
                actionSequence += COMBO_NAMES[comboString[:tryLength]]
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
                actionSequence += COMBO_ACTION_NAMES[comboString[:tryLength]]
                comboString = comboString[tryLength:]
                tryLength = 0
                break
            tryLength -= 1
        if tryLength == 0:
            continue

        # check if the next character is an action symbol
        if comboString[0] in COMBO_ACTION_SYMBOLS.keys():
            logUnrecognised(unrecognised, warningList)
            actionSequence += COMBO_ACTION_SYMBOLS[comboString[0]]
            comboString = comboString[1:]
            continue

        # failed to recognise any action - push the first character to the unrecognised string and move on
        else:
            unrecognised += comboString[0]
            comboString = comboString[1:]

    # join movestacks / early cancels
    tempActionSequence = actionSequence
    actionSequence = []
    while len(tempActionSequence) > 0:

        # movestacks
        if tempActionSequence[0] == "+":

            # no previous/following action
            if (len(actionSequence) == 0) or (len(tempActionSequence) == 1):
                break

            # movestack valid
            if (actionSequence[-1] + "+" + actionSequence[1]) in State.ApplyAction.keys():
                actionSequence[-1] += "+" + actionSequence[1]
                tempActionSequence = tempActionSequence[2:]

            # movestack invalid
            else:
                warningList.append(f"unrecognised movestack \"{actionSequence[-1]}+{actionSequence[1]}\"")
                tempActionSequence = tempActionSequence[1:]

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
                warningList.append(f"unrecognised early cancel \"{actionSequence[-1]}-{actionSequence[1]}\"")
                tempActionSequence = tempActionSequence[1:]

        else:
            actionSequence.append(tempActionSequence[0])
            tempActionSequence = tempActionSequence[1:]

    return actionSequence