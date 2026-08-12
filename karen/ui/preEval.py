from karen.state import State
from karen.actions.actionData import ACTION_NAMES, ANIMATION_CANCEL_TIMES, WEB_BOMB_DURATION

# replaces suboptimal inputs / typos and raises warnings for sequence errors
def preEval(actionSequence: list[str], warningList: list[str], advancedMode: bool = False):
    improvedActionSequence: list[str] = []

    while len(actionSequence) > 0:

        # automatic swing whiff insertion
        if (not advancedMode) and (len(improvedActionSequence) > 0) and (improvedActionSequence[-1][-1] == "u") and (actionSequence[0][0] in ["t", "g", "C", "B"]):
            warningList.append(f"automatically weaved swing whiff between {ACTION_NAMES["u"]} and {ACTION_NAMES[actionSequence[0]]}")
            improvedActionSequence.append("w")

        # automatic saporen/spacejam detection
        if (len(actionSequence) >= 2) and (actionSequence[0] in ["p", "k", "o", "u"]) and (actionSequence[1] == "G"):
            improvedActionSequence.append(f"{actionSequence[0]}+G")
            actionSequence = actionSequence[2:]
            continue

        if (len(actionSequence) >= 3) and (actionSequence[0] == "u") and (actionSequence[1] in ["w", "a"]) and (actionSequence[2] == "G"):
            improvedActionSequence.append(f"u+{actionSequence[1]}+G")
            actionSequence = actionSequence[3:]
            continue
        
        improvedActionSequence.append(actionSequence[0])
        actionSequence = actionSequence[1:]

    # automatic wait if the combo starts with a clap, doesn't specify a wait time right after, and includes an explosion
    if (len(improvedActionSequence) > 1) and (improvedActionSequence[0] == "C") and (improvedActionSequence[1][0] != "[") and (True in ["E" in action for action in improvedActionSequence]):
        dummyState: State = State(improvedActionSequence)
        explosionWaitTimeMin: int = dummyState.explosionWaitTimer
        if explosionWaitTimeMin != 0:
            explosionWaitTimeMax: int = max(WEB_BOMB_DURATION - 1- dummyState.lastTagProcPreExplosion, 0)
            explosionWaitTime: str = f"[{explosionWaitTimeMin}-{explosionWaitTimeMax}R]" if explosionWaitTimeMax > explosionWaitTimeMin else f"[{explosionWaitTimeMax}f]"
            improvedActionSequence = improvedActionSequence[:1] + [explosionWaitTime] + improvedActionSequence[1:]

    return improvedActionSequence