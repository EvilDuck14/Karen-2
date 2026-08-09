from karen.actions.actionData import *
from karen.state import State

#=========================================================================================================#
#                                              Punch Cancel                                               #
#=========================================================================================================#

def applyPunchCancel(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["p"]) 

    # await kick expiration
    if state.meleeSequenceStep == "kick":
        state.pushLog("awaiting kick expiration", ["waiting"])
        state.pushLog("waiting for punch when kick cancel would be faster", ["sequence warning"])
        state.advanceTime(state.meleeSequenceTimer)

    # ANIMATION STARTS HERE
    state.pushLog("started punch cancel", ["action started"])

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
    
State.ApplyAction["p-"] = applyPunchCancel


#=========================================================================================================#
#                                               Kick Cancel                                               #
#=========================================================================================================#

def applyKickCancel(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["p"]) 

    # ANIMATION STARTS HERE
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

State.ApplyAction["k-"] = applyKickCancel


#=========================================================================================================#
#                                             Overhead Cancel                                             #
#=========================================================================================================#

def applyOverheadCancel(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["p"]) 

    # await swing whiff end
    if (state.fireRateTimers["s"] > 0) and (state.hasSwingOverhead != True):
        state.pushLog("used overhead slam after swing whiff - was U3H intended?", ["sequence warning"])

        # if an immediate overhead available, using it gives a faster overhead, otherwise await swing whiff end
        if not (state.hasDoubleJump or state.hasSwingOverhead == "unknown"):
            state.advanceTime(state.fireRateTimers["s"])

    # ANIMATION STARTS HERE
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

State.ApplyAction["o-"] = applyOverheadCancel


#=========================================================================================================#
#                                                 Nostick                                                 #
#=========================================================================================================#

def applyNostick(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["s"]) 

    # await action charge availability
    state.awaitCharge("s")

    # ANIMATION STARTS HERE
    state.pushLog("started no stick", ["action started"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = "error" if action in ILLEGAL_CANCELS["a"] else 1

    # set cooldown (fire rate)
    state.fireRateTimers["s"] = COOLDOWN_TIMES["a"]

    # cancel active abilities
    state.endActive("u")
    state.endActive("g")
    state.endActive("S")
    
State.ApplyAction["a-"] = applyNostick