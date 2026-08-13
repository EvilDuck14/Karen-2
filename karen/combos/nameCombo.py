from karen.combos.parseComboString import COMBO_NAMES

def nameCombo(actionSequence: list[str]) -> str:
    comboString: str = ""
    for action in actionSequence:
        if action[0] != "[":
            comboString += action

    # formatting to match combos in database
    comboString = comboString.replace("V", "S")
    comboString = comboString.replace("a-", "a")
    comboString = comboString.replace("Ew", "wE").replace("Ea", "aE")
    comboString = comboString.replace("E+G", "G+E")
    comboString = comboString.replace("u+G", "u+w+G")
    comboString = comboString.replace("u+S+G", "u+S+w+G")

    # missing explosion at the end / clap at the start is still the same combo
    if "B" in comboString:
        if not ("C" in comboString):
            comboString = "C" + comboString
        if not ("E" in comboString):
            comboString += "E"

    if comboString in COMBO_NAMES.keys():
        return COMBO_NAMES[comboString]

    # extra swings/tracers at the end are still essentially the same combo
    shaveComboString: str = comboString
    while (len(shaveComboString) > 0):
        if shaveComboString[-1] in ["t", "w", "a"]:
            shaveComboString = shaveComboString[:-1]
        elif (len(shaveComboString) >= 2) and (shaveComboString[-1] == "E") and (shaveComboString[-2] in ["t", "w", "a"]):
            shaveComboString = shaveComboString[:-2] + "E"
        else:
            break
        if shaveComboString in COMBO_NAMES.keys():
            return COMBO_NAMES[shaveComboString]

    # (fast) variation for adding auto swings
    for index in range(len(comboString)):
        if comboString[index] == "a":

            # detect added autoswings
            name: str = nameCombo(comboString[:index] + comboString[(index + 1):])
            name = name.replace("(Fast) ", "")
            if name != "":
                return "(Fast) " + name

            # detect autoswings replacing whiffs
            name: str = nameCombo(comboString[:index] + "w" + comboString[(index + 1):])
            name = name.replace("(Fast) ", "")
            if name != "":
                return "(Fast) " + name

    # no name found
    return ""