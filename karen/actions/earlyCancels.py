from karen.actions.actionData import *
from karen.state import State
from karen.actions.basicActions import *

#=========================================================================================================#
#                                              Punch Cancel                                               #
#=========================================================================================================#

def usePunchCancel(state: State):
    state.pushLog("started punch cancel", ["action started"])

    # major warning if punch started while kick was available
    if state.meleeSequenceStep == "kick":
        state.pushLog("used punch when kick was available", ["major warning"])

    # minor warning if swing overhead is available
    if state.hasSwingOverhead:
        state.pushLog("used punch when swing overhead was available", ["minor warning", "overhead warning"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = "error" if action in ILLEGAL_CANCELS["p"] else 1

    # tracking melee sequence
    state.meleeSequenceTimer = MELEE_SEQUENCE_WINDOW
    if state.meleeSequenceStep == "punch 1":
        state.meleeSequenceStep = "punch 2"
    elif state.meleeSequenceStep in ["punch 2", "not punch 1"]:
        state.meleeSequenceStep == "kick"
    elif state.meleeSequenceStep == "unknown":
        state.meleeSequenceStep = "not punch 1"

    # cancel symbiote teather
    state.endActive("S")

def applyPunchCancel(state: State):
    state.advanceTime(state.animationCancelTimes["p"]) 
    awaitPunchReady(state)
    usePunchCancel(state)
    
State.ApplyAction["p-"] = applyPunchCancel


#=========================================================================================================#
#                                               Kick Cancel                                               #
#=========================================================================================================#

def useKickCancel(state: State):
    state.pushLog("started kick cancel", ["action started"])

    # major warning if kick is not available
    if state.meleeSequenceStep in ["punch 1", "punch 2"]:
        state.pushLog("used illegal kick", ["major warning"])

    # minor warning if swing overhead is available
    if state.hasSwingOverhead:
        state.pushLog("used kick when swing overhead was available", ["minor warning", "overhead warning"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = "error" if action in ILLEGAL_CANCELS["k"] else 1

    # tracking melee sequence
    state.meleeSequenceTimer = 0
    state.meleeSequenceStep = "punch 1"

    # cancel symbiote teather
    state.endActive("S")

def applyKickCancel(state: State):
    state.advanceTime(state.animationCancelTimes["p"]) 
    useKickCancel(state)

State.ApplyAction["k-"] = applyKickCancel


#=========================================================================================================#
#                                             Overhead Cancel                                             #
#=========================================================================================================#

def useOverheadCancel(state: State):
    state.pushLog("started overhead slam cancel", ["action started"])
    
    # minor warning if no overhead is available
    if (state.hasSwingOverhead == False) and (state.hasDoubleJump == False):
        state.pushLog("used potentially illegal overhead", ["minor warning", "overhead warning"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = "error" if action in ILLEGAL_CANCELS["o"] else 1

    # tracking overhead availability
    if state.hasSwingOverhead != False:
        state.hasSwingOverhead = False
    else:
        state.hasDoubleJump = False

    # cancel symbiote teather
    state.endActive("S")

def applyOverheadCancel(state: State):
    state.advanceTime(state.animationCancelTimes["p"])
    awaitOverheadReady(state)
    useOverheadCancel(state)

State.ApplyAction["o-"] = applyOverheadCancel


#=========================================================================================================#
#                                                 Nostick                                                 #
#=========================================================================================================#

def useNostick(state: State):
    state.pushLog("started no stick", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("s")

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = "error" if action in ILLEGAL_CANCELS["a"] else 1

    # set cooldown (fire rate)
    state.fireRateTimers["s"] = COOLDOWN_TIMES["a"]

    # cancel active abilities
    state.endActive("u")
    state.endActive("g")
    state.endActive("S")

def applyNostick(state: State):
    state.advanceTime(state.animationCancelTimes["s"]) 
    state.awaitCharge("s")
    useNostick(state)
    
State.ApplyAction["a-"] = applyNostick