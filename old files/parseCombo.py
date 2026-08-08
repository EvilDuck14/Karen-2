from karen.actions import *
from karen.combos import *

# converts user input into a sequence of actions to be parsed by the calculator
def parseCombo(comboString : str, actionSet : list[Action]) -> list[Action]:

    comboActions = []
    
    while len(comboString) > 0:

        if comboString[0] == " ":
            comboString = comboString[1:]
            continue

        checkTo = len(comboString)
        if ">" in comboString:
            checkTo = comboString.index(">")

        while checkTo > 0:
            addActions = []

            # first attempt to add the largest combo name found
            if comboString[0:checkTo].lower() in COMBOS:
                addActions = COMBOS[comboString[0:checkTo].lower()]

            # otherwise, attempt to add actions
            elif comboString[0:checkTo] in ACTIONS:
                addActions = ACTIONS[comboString[0:checkTo]]
            elif comboString[0:checkTo].lower() in ACTIONS:
                addActions = ACTIONS[comboString[0:checkTo].lower()]

    return comboActions