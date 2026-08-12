from karen.state import State
from karen.actions.actionData import ACTION_NAMES, ANIMATION_CANCEL_TIMES, WEB_BOMB_DURATION

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

            # don't use a swing whiff to speed up tracer > tracer
            elif (improvedActionSequence[-1][-1] == "t") and (actionSequence[0] == "t"):
                pass

            # don't use a swing whiff to speed up symbiote > symbiote
            elif (improvedActionSequence[-1] in ["S", "V"] and actionSequence[0] in ["S", "V"]):
                pass

            # otherwise, insert swing whiff if it speeds up the combo
            else:
                nextActionType = actionSequence[0][0].replace("k", "p").replace("w", "s").replace("a", "s").replace("G", "g")
                if (ANIMATION_CANCEL_TIMES[improvedActionSequence[-1][-1]]["s"] + ANIMATION_CANCEL_TIMES["w"][nextActionType] < ANIMATION_CANCEL_TIMES[improvedActionSequence[-1][-1]][nextActionType]):
                    warningList.append(f"automatically weaved swing whiff between {ACTION_NAMES[improvedActionSequence[-1]]} and {ACTION_NAMES[actionSequence[0]]}")
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
    if (improvedActionSequence[0] == "C") and (len(improvedActionSequence) > 1) and (improvedActionSequence[1][0] != "[") and (True in ["E" in action for action in improvedActionSequence]):
        dummyState: State = State(improvedActionSequence)
        explosionWaitTimeMin: int = dummyState.explosionWaitTimer
        if explosionWaitTimeMin != 0:
            explosionWaitTimeMax: int = max(WEB_BOMB_DURATION - 1- dummyState.lastTagProcPreExplosion, 0)
            explosionWaitTime: str = f"[{explosionWaitTimeMin}-{explosionWaitTimeMax}R]" if explosionWaitTimeMax > explosionWaitTimeMin else f"[{explosionWaitTimeMax}f]"
            improvedActionSequence = improvedActionSequence[:1] + [explosionWaitTime] + improvedActionSequence[1:]

    return improvedActionSequence