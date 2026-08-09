from karen.actions.actionData import *
from karen.state import State

#=========================================================================================================#
#                                                  Punch                                                  #
#=========================================================================================================#

def applyPunch(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["p"]) 

    # await kick expiration
    if state.meleeSequenceStep == "kick":
        state.pushLog("awaiting kick expiration", ["waiting"])
        if state.meleeSequenceTimer >= (ACTION_DAMAGE_TIME["k"] - ACTION_DAMAGE_TIME["p"]):
            state.pushLog("waiting for punch when kick would likely be faster", ["sequence warning"])
        state.advanceTime(state.meleeSequenceTimer)

    # ANIMATION STARTS HERE
    state.pushLog("started punch", ["action started"])

    # minor warning if swing overhead is available
    if state.hasSwingOverhead:
        state.pushLog("used punch when swing overhead was available", ["minor warning", "overhead warning"])

    # deal damage (function handles tag proc)
    state.dealDamage("p", ACTION_DAMAGE_TIME["p"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["p"][action]

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
      
State.ApplyAction["p"] = applyPunch


#=========================================================================================================#
#                                                  Kick                                                   #
#=========================================================================================================#

def applyKick(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["p"]) 

    # ANIMATION STARTS HERE
    state.pushLog("started kick", ["action started"])

    # major warning if kick is not available
    if state.meleeSequenceStep in ["punch 1", "punch 2"]:
        state.pushLog("used illegal kick", ["major warning"])

    # minor warning if swing overhead is available
    if state.hasSwingOverhead:
        state.pushLog("used kick when swing overhead was available", ["minor warning", "overhead warning"])

    # deal damage (function handles tag proc)
    state.dealDamage("k", ACTION_DAMAGE_TIME["k"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["k"][action]

    # tracking melee sequence
    state.meleeSequenceTimer = 0
    state.meleeSequenceStep = "punch 1"

    # cancel symbiote teather
    state.endActive("S")
      
State.ApplyAction["k"] = applyKick


#=========================================================================================================#
#                                              Overhead Slam                                              #
#=========================================================================================================#

def applyOverhead(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["p"]) 

    # await swing whiff end
    if (state.fireRateTimers["s"] > 0) and (state.hasSwingOverhead != True):
        state.pushLog("used overhead slam after swing whiff - was U3H intended?", ["sequence warning"])

        # if an immediate overhead available, using it gives a faster overhead, otherwise await swing whiff end
        if not (state.hasDoubleJump or state.hasSwingOverhead == "unknown"):
            state.advanceTime(state.fireRateTimers["s"])

    # ANIMATION STARTS HERE
    state.pushLog("started overhead slam", ["action started"])

    # minor warning if no overhead is available
    if (state.hasSwingOverhead == False) and (state.hasDoubleJump == False):
        state.pushLog("used potentially illegal overhead", ["minor warning", "overhead warning"])

    # deal damage (function handles tag proc)
    state.dealDamage("o", ACTION_DAMAGE_TIME["o"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["o"][action]

    # tracking overhead availability
    if state.hasSwingOverhead != False:
        state.hasSwingOverhead = False
    else:
        state.hasDoubleJump = False

    # cancel symbiote teather
    state.endActive("S")
      
State.ApplyAction["o"] = applyOverhead


#=========================================================================================================#
#                                                 Tracer                                                  #
#=========================================================================================================#

def applyTracer(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["t"]) 

    # await action charge availability
    state.awaitCharge("t")

    # ANIMATION STARTS HERE
    state.pushLog("started tracer", ["action started"])

    # deal damage (function handles tag application)
    state.dealDamage("t", ACTION_DAMAGE_TIME["t"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["t"][action]

    # cooldown tracking
    state.charges["t"] -= 1
    if state.rechargeTimers["t"] == 0:
        state.rechargeTimers["t"] = RECHARGE_TIMES["t"]
    state.fireRateTimers["t"] = COOLDOWN_TIMES["t"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("S")
      
State.ApplyAction["t"] = applyTracer


#=========================================================================================================#
#                                               Swing Whiff                                               #
#=========================================================================================================#

def applyWhiff(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["s"]) 

    # await action charge availability
    state.awaitCharge("s")

    # ANIMATION STARTS HERE
    state.pushLog("started swing whiff", ["action started"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["w"][action]

    # set ability to active state
    state.activeTimers["s"] = ACTIVE_TIMES["w"]

    # cancel active abilities
    state.endActive("u")
    state.endActive("g")
    state.endActive("S")
      
State.ApplyAction["w"] = applyWhiff


#=========================================================================================================#
#                                               Auto Swing                                                #
#=========================================================================================================#

def applyAutoswing(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["s"]) 

    # await action charge availability
    state.awaitCharge("s")

    # ANIMATION STARTS HERE
    state.pushLog("started auto swing", ["action started"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["a"][action]

    # set ability to active state
    state.activeTimers["s"] = ACTIVE_TIMES["a"]

    # cancel active abilities
    state.endActive("u")
    state.endActive("g")
    state.endActive("S")
      
State.ApplyAction["a"] = applyAutoswing


#=========================================================================================================#
#                                              Get Over Here                                              #
#=========================================================================================================#

def applyGOH(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["g"]) 

    # await action charge availability
    state.awaitCharge("g")

    # ANIMATION STARTS HERE
    state.pushLog("started get over here", ["action started"])

    # deal damage
    state.dealDamage("g", ACTION_DAMAGE_TIME["g"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["g"][action]

    # set ability to active state
    state.activeTimers["g"] = ACTIVE_TIMES["g"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("S")

State.ApplyAction["g"] = applyGOH


#=========================================================================================================#
#                                        Get Over Here (Targeting)                                        #
#=========================================================================================================#

def applyGOHT(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["g"]) 

    # await action charge availability
    state.awaitCharge("g")

    # await tag registring
    if (state.GOHTAvaiableTimer == 0) and (state.tagTimer > 0):
        state.pushLog("get over here (targetting) awaiting tracer registering", ["waiting"])
        state.advanceTime(state.tagTimer - (TAG_DURATION - TAG_GOHT_DELAY))

    # await web bomb explosion
    if (state.GOHTAvaiableTimer == 0) and state.isTaggedBomb:
        state.pushLog("get over here (targetting) awaiting web bomb explosion", ["waiting"])
        state.advanceTime(state.bombTimer + TAG_GOHT_DELAY)

    # ANIMATION STARTS HERE
    state.pushLog("started get over here (targeting)", ["action started"])

    # major warning if no tag is applied
    if state.tagTimer == 0:
        state.pushLog("used illegal get over here (targeting)", ["major warning"])

    # deal damage
    state.dealDamage("G", ACTION_DAMAGE_TIME["G"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["G"][action]

    # set ability to active state
    state.activeTimers["g"] = ACTIVE_TIMES["G"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("S")
      
State.ApplyAction["G"] = applyGOHT


#=========================================================================================================#
#                                                Uppercut                                                 #
#=========================================================================================================#

def applyUppercut(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["u"]) 

    # await action charge availability
    state.awaitCharge("u")

    # ANIMATION STARTS HERE
    state.pushLog("started uppercut", ["action started"])

    # deal damage
    state.dealDamage("u", ACTION_DAMAGE_TIME["u"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["u"][action]

    # set ability to active state
    state.activeTimers["u"] = ACTIVE_TIMES["u"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("S")
      
State.ApplyAction["u"] = applyUppercut


#=========================================================================================================#
#                                                Symbiote                                                 #
#=========================================================================================================#

def applySymbiote(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["S"]) 

    # await action charge availability
    state.awaitCharge("S")

    # ANIMATION STARTS HERE
    state.pushLog("started symbiote", ["action started"])

    # deal damage
    state.dealDamage("S", ACTION_DAMAGE_TIME["S"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["S"][action]

    # set ability to active state
    state.activeTimers["S"] = ACTIVE_TIMES["S"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("g")
    state.endActive("u")
      
State.ApplyAction["S"] = applySymbiote


#=========================================================================================================#
#                                            Symbiote Teather                                             #
#=========================================================================================================#

def applyTeather(state: State):
    applySymbiote(state)
    state.teatherTimer = SYMBIOTE_MAX_DURATION

State.ApplyAction["V"] = applyTeather


#=========================================================================================================#
#                                                  Clap                                                   #
#=========================================================================================================#

def applyClap(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["C"]) 

    # await action charge availability
    state.awaitCharge("B")

    # ANIMATION STARTS HERE
    state.pushLog("started clap", ["action started"])

    # start bomb timer
    state.bombTimer = WEB_BOMB_DURATION

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["C"][action]

    # cooldown tracking
    state.charges["B"] -= 1
    state.rechargeTimers["B"] = RECHARGE_TIMES["B"]

    # cancel active abilities
    state.endActive("g")
      
State.ApplyAction["C"] = applyClap


#=========================================================================================================#
#                                                Web Bomb                                                 #
#=========================================================================================================#

def applyBomb(state: State):

    # await previous animation
    state.advanceTime(state.animationCancelTimes["B"]) 

    # ANIMATION STARTS HERE
    state.pushLog("started clap", ["action started"])

    # major warning if bomb is not available
    if state.bombTimer == 0:
        state.pushLog("used illegal web bomb", ["major warning"])

    # deal damage
    state.dealDamage("B", ACTION_DAMAGE_TIME["B"])

    # set bomb timer to minimum allowed time after connecting
    state.isTaggedBomb = True
    state.bombTimer = max(state.bombTimer, ACTION_DAMAGE_TIME["B"] + WEB_BOMB_TAG_DURATION)

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["B"][action]

    # cancel active abilities
    state.endActive("s")
      
State.ApplyAction["B"] = applyBomb


#=========================================================================================================#
#                                           Web Bomb Explosion                                            #
#=========================================================================================================#

def applyExplosion(state: State):

    # major warning if bomb is not active
    if state.bombTimer == 0:
        state.log("used illegal explosion", ["major warning"])
        return

    # await explosion
    state.log("awaiting web bomb explosion", ["waiting"])
    state.advanceTime(state.bombTimer) 
      
State.ApplyAction["E"] = applyExplosion