import copy

from karen.actions import *
from karen.combos import *

def classifyCombo(sequence: list[Action], recursivePass : bool = False) -> str:
    workingSequence : list[Action] = copy.deepcopy(sequence)
    
    # swings and autoswings are equivalent for classification
    if not recursivePass:
        for i in range(len(workingSequence)):
            if workingSequence[i] == ACTIONS["s"]:
                workingSequence[i] = ACTIONS["a"]

    # trailing swings and tracers don't affect classification
    if not recursivePass:
        while len(sequence) > 0 and sequence[-1] in [ACTIONS["t"], ACTIONS["w"], ACTIONS["a"]]:
            sequence = sequence[:-1]

    # classifying combo which is only swings and tracers
    if len(workingSequence == 0):
        match sequence.count(ACTIONS["t"]):
            case 0:
                return "Nothing"
            case 1:
                return "Tracer"
            case 2:
                return "Double Tracer"
            case 3:
                return "Triple Tracer"
            case _:
                return "Tracer Spam"
    
    # excessive swings and tracers before combo are ignored
    if not recursivePass:
        leadingTracers = 0
        for action in workingSequence:
            if action == ACTIONS["t"]:
                leadingTracers += 1
            if not action in [ACTIONS["t"], ACTIONS["w"], ACTIONS["a"]]:
                break
        while leadingTracers > 1:
            if workingSequence[0] == ACTIONS["t"]:
                leadingTracers -= 1
            workingSequence = workingSequence[1:]

    # classifying combo which is only one action
    if len(workingSequence == 1):
        return workingSequence[0].name

    # classifying bnb openers
    if len(workingSequence) >= 3 and workingSequence[:3] == COMBO_NAMES["BnB"].sequence:
        followUp : str = classifyCombo(workingSequence[3:], recursivePass=True)
        if followUp == "Nothing":
            return "BnB"
        else:
            return "BnB " + followUp
    
    # classifying combo from standard list
    if workingSequence in COMBO_SEQUENCES:
        return COMBO_SEQUENCES[workingSequence].name
    
    # classifying combo as "fast" if it speeds up an existing combo with autoswings
    # TO DO

    # classifying combo as "wasteful" if it uses swing cooldowns in place of whiffs
    # TO DO

    # classifying combo as "slow" if it omits autoswings
    # TO DO

    # classifying combo as "unoptimised" if it omits whiffs
    # TO DO

    # classifying combo as "heavy" if it uses kicks or overheads in place of punches
    # TO DO