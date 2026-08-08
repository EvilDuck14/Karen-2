from karen.actions import *

class Combo:
    name: str
    comboString: str
    sequence: list

    def __init__(self, name : str, comboString: str):
        self.name = name
        self.sequence = Combo.fastParseCombo(comboString)

    @staticmethod
    def fastParseCombo(comboString : str) -> list[Action]:
        sequenceKeys = []
        
        while len(comboString) > 0:
            if comboString[0] == "+":
                sequenceKeys[-1] = sequenceKeys[-1] + "+" + comboString[1]
                comboString = comboString[2:]
            else:
                sequenceKeys.append(comboString[0])
                comboString = comboString[1:]

        return [ACTIONS[key] for key in sequenceKeys]


COMBOS : list[Combo] = {

    Combo (
        name = "BnB",
        comboString = "tGu"
    ),

    Combo (
        name = "Short Plink",
        comboString = "ao"
    ),

    Combo (
        name = "Long Plink",
        comboString = "wto"
    ),
    
    Combo (
        name = "Double Plink",
        comboString = "wtao"
    ),
    
    Combo (
        name = "U3H",
        comboString = "wpp+o"
    ),
    
    Combo (
        name = "Weave Combo",
        comboString = "tGwtuwt"
    ),
    
    Combo (
        name = "Panther Combo",
        comboString = "tGptu"
    ),
    
    Combo (
        name = "Melee Combo",
        comboString = "tptuwt"
    ),
    
    Combo (
        name = "Slam Combo",
        comboString = "totu"
    ),
    
    Combo (
        name = "Sekkombo",
        comboString = "tgptu"
    ),
    
    Combo (
        name = "Grip Kick Rip (GKR)",
        comboString = "tgktu"
    ),
    
    Combo (
        name = "FFAmestack Burst",
        comboString = "otG+u"
    ),
    
    Combo (
        name = "Overhead Burst",
        comboString = "otuwtg"
    ),
    
    Combo (
        name = "Master Manipulator",
        comboString = "otaptu"
    ),
    
    Combo (
        name = "Master Masher",
        comboString = "otgwtu"
    ),
    
    Combo (
        name = "",
        comboString = ""
    ),
    
    Combo (
        name = "",
        comboString = ""
    ),
    
    Combo (
        name = "",
        comboString = ""
    ),
    
    Combo (
        name = "",
        comboString = ""
    ),
    
    Combo (
        name = "",
        comboString = ""
    ),
    
    Combo (
        name = "",
        comboString = ""
    ),
}

COMBO_NAMES = {
    combo.name : combo for combo in COMBOS
}

# alternate combo names
COMBO_NAMES["B&B"] = COMBO_NAMES["BnB"]
COMBO_NAMES["Bread n Butter"] = COMBO_NAMES["BnB"]
COMBO_NAMES["Bread & Butter"] = COMBO_NAMES["BnB"]
COMBO_NAMES["Bread and Butter"] = COMBO_NAMES["BnB"]
# TO DO

# names work with and without "combo" at the end
for comboName in COMBO_NAMES:
    if comboName.len >= 6 and comboName[-6:] == " Combo":
        COMBO_NAMES[comboName[:-6]] = COMBO_NAMES[comboName]
    else:
        COMBO_NAMES[comboName + " Combo"] = COMBO_NAMES[comboName]

COMBO_NAMES_LOWER = {
    combo.name.lower() : combo for combo in COMBOS
}

COMBO_SEQUENCES = {
    combo.sequence : combo for combo in COMBOS
}

# ensures combos which canonically end with "whiff > tracer" are classified correctly, even when this ending is omitted
for comboSequence in COMBO_SEQUENCES:
    if comboSequence.len >= 2 and comboSequence[-2:] == [ACTIONS["w"], ACTIONS["t"]]:
        COMBO_SEQUENCES[comboSequence[:-2]] = COMBO_SEQUENCES[comboSequence]