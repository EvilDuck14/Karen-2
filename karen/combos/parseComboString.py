from karen.state.state import State
from karen.combos.comboData import *
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

# separates parameters from the rest of the input
def extractParams(inputString: str, warningList: list[str]) -> tuple[str, dict[str, bool]]:

    # TO DO: load user prefs if no params given
    if not ("--" in inputString):
        pass

    # default parameters
    params: dict[str, bool] = {
        "a" : False, # advanced mode
        "b" : False, # breakdown mode
        "n" : False, # no warnings
        
        "t" : True, # display time
        "tfd" : True, # display time from damage
        "d" : True, # display damage
        "dps" : False # display damage per second
    }

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

            # parameter not recognised
            if not (word[2:] in params.keys()):
                warningList.append(f"parameter not recognised \"{word}\"")
                continue

            if (not displayChanged) and (word[2:] in ["t", "tfd", "d", "dps"]):
                displayChanged = True
                params["t"] = False
                params["tfd"] = False
                params["d"] = False
                params["dps"] = False

            params[word[2:]] = True
            
        else:
            filteredString += word

    return filteredString, params


def parseComboString(comboString: str, warningList: list[str]) -> tuple[list[str], dict[str, bool]]:
    actionSequence: list[str] = []
    params: dict[str, bool]

    comboString = removeParentheses(comboString)
    comboString, params = extractParams(comboString, warningList)

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
            if comboString[:tryLength].lower() in SEQUENCE_NAMES.keys():
                logUnrecognised(unrecognised, warningList)
                unrecognised = ""
                actionSequence += SEQUENCE_NAMES[comboString[:tryLength].lower()]
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
            if (len(actionSequence) > 0) and (len(tempActionSequence) >= 2):
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
        if (action in State.ApplyAction.keys()) or (action[0] in ["[", ","]):
            actionSequence.append(action)

        else:
            warningList.append(f"unrecognised movestack \"{action}\"")
            actionSequence += action.split("+")

    return actionSequence, params