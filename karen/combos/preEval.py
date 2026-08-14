from karen.state.state import State
from karen.actions.actionData import *

# replaces suboptimal inputs / typos and raises warnings for sequence errors
def preEval(actionSequence: list[str], warningList: list[str], advancedMode: bool = False):
    improvedActionSequence: list[str] = []

    # automatic movestack detection
    sequenceString = "".join(actionSequence)
    while len(sequenceString) > 0:

        if sequenceString[0] == "[":
            improvedActionSequence.append(sequenceString[:(sequenceString.find("]") + 1)])
            sequenceString = sequenceString[(sequenceString.find("]") + 1):]
            continue

        # automatic swing whiff insertion
        if (not advancedMode) and (len(improvedActionSequence) > 0) and (improvedActionSequence[-1][-1] == "u") and (sequenceString[0] in ["t", "g", "C", "B"]):
            warningList.append(f"automatically weaved swing whiff between {ACTION_NAMES["u"]} and {ACTION_NAMES[actionSequence[0]]}")
            improvedActionSequence.append("w")

        nostacks: str = sequenceString.replace("+", "")

        # automatic goh/bomb stack
        if nostacks[:2] in ["gB", "GB"]:
            improvedActionSequence.append(f"{nostacks[0]}+B")
            sequenceString = sequenceString[(sequenceString.find("B") + 1):]
            continue

        # automatic saporen detection
        if nostacks[:2] in ["pG", "kG", "oG"]:
            improvedActionSequence.append(f"{sequenceString[0]}+G")
            sequenceString = sequenceString[(sequenceString.find("G") + 1):]
            continue

        # automatic saporen detection
        if nostacks[:3] in ["uwG", "uaG"]:
            improvedActionSequence.append(f"u+{nostacks[1]}+G")
            sequenceString = sequenceString[(sequenceString.find("G") + 1):]
            continue
        if nostacks[:2] == ["uG"]:
            improvedActionSequence.append(f"u+G")
            sequenceString = sequenceString[(sequenceString.find("G") + 1):]
            continue

        # automatic symbiotic saporen detection
        if nostacks[:4] in ["uSwG", "uSaG", "uVwG", "uVaG"]:
            improvedActionSequence.append(f"u+{nostacks[1]}+{nostacks[2]}+G")
            sequenceString = sequenceString[(sequenceString.find("G") + 1):]
            continue
        if nostacks[:3] in ["uSG", "uVG"]:
            improvedActionSequence.append(f"u+S+G")
            sequenceString = sequenceString[(sequenceString.find("G") + 1):]
            continue

        if sequenceString[0] == "+":
            improvedActionSequence[-1] += sequenceString[:2]
            sequenceString = sequenceString[2:]
        else: 
            improvedActionSequence.append(sequenceString[0])
            sequenceString = sequenceString[1:]

    # automatic wait if the combo starts with a clap, doesn't specify any wait times, and includes an explosion
    if (len(improvedActionSequence) > 1) and (improvedActionSequence[0] == "C") and (not (True in [action[0] == "[" for action in improvedActionSequence])) and (True in ["E" in action for action in improvedActionSequence]):
        dummyState: State = State(improvedActionSequence)
        explosionWaitTimeMin: int = dummyState.explosionWaitTimer

        if len(improvedActionSequence) >= 2:
            secondActionType: str = improvedActionSequence[1][0].replace("k", "p").replace("w", "s").replace("a", "s").replace("V", "S").replace("E", "s")
            explosionWaitTimeMin += ANIMATION_CANCEL_TIMES["C"][secondActionType]

        explosionWaitTime: str = f"[{explosionWaitTimeMin}-R]"
        improvedActionSequence = improvedActionSequence[:1] + [explosionWaitTime] + improvedActionSequence[1:]

    return improvedActionSequence