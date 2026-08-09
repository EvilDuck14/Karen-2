from karen.actions.actionData import *
from karen.state import State

#=========================================================================================================#
#                                                  Punch                                                  #
#=========================================================================================================#

def awaitPunchReady(state: State, frameOffset: int = 0):

    # await kick expiration
    if (state.meleeSequenceStep == "kick") and (state.meleeSequenceTimer > frameOffset):
        state.pushLog("awaiting kick expiration", ["waiting"])
        if state.meleeSequenceTimer - frameOffset >= (ACTION_DAMAGE_TIME["k"] - ACTION_DAMAGE_TIME["p"]):
            state.pushLog("waiting for punch when kick would likely be faster", ["sequence warning"])
        state.advanceTime(state.meleeSequenceTimer - frameOffset)

def usePunch(state: State, keepGOHTAvailable: bool = False):
    state.pushLog("started punch", ["action started"])

    # major warning if punch started while kick was available
    if state.meleeSequenceStep == "kick":
        state.pushLog("used punch when kick was available", ["major warning"])

    # minor warning if swing overhead is available
    if state.hasSwingOverhead:
        state.pushLog("used punch when swing overhead was available", ["minor warning", "overhead warning"])

    # deal damage
    state.dealDamage("p", frameOffset=ACTION_DAMAGE_TIME["p"])
    state.procTag(frameOffset=ACTION_DAMAGE_TIME["p"], keepGOHTAvailable=keepGOHTAvailable)

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

def applyPunch(state: State):
    state.advanceTime(state.animationCancelTimes["p"]) 
    awaitPunchReady(state)
    usePunch(state)
      
State.ApplyAction["p"] = applyPunch


#=========================================================================================================#
#                                                  Kick                                                   #
#=========================================================================================================#

def useKick(state: State, keepGOHTAvailable: bool = False):
    state.pushLog("started kick", ["action started"])

    # major warning if kick is not available
    if state.meleeSequenceStep in ["punch 1", "punch 2"]:
        state.pushLog("used illegal kick", ["major warning"])

    # minor warning if swing overhead is available
    if state.hasSwingOverhead:
        state.pushLog("used kick when swing overhead was available", ["minor warning", "overhead warning"])

    # deal damage
    state.dealDamage("k", frameOffset=ACTION_DAMAGE_TIME["k"])
    state.procTag(frameOffset=ACTION_DAMAGE_TIME["k"], keepGOHTAvailable=keepGOHTAvailable)

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["k"][action]

    # tracking melee sequence
    state.meleeSequenceTimer = 0
    state.meleeSequenceStep = "punch 1"

    # cancel symbiote teather
    state.endActive("S")

def applyKick(state: State):
    state.advanceTime(state.animationCancelTimes["p"]) 
    useKick(state)
      
State.ApplyAction["k"] = applyKick


#=========================================================================================================#
#                                              Overhead Slam                                              #
#=========================================================================================================#

def awaitOverheadReady(state: State, frameOffset: int = 0):

    # await swing whiff end
    if (state.fireRateTimers["s"] > frameOffset) and (state.hasSwingOverhead != True):
        state.pushLog("used overhead slam after swing whiff - was U3H intended?", ["sequence warning"])

        # if an immediate overhead available, using it gives a faster overhead, otherwise await swing whiff end
        if not (state.hasDoubleJump or state.hasSwingOverhead == "unknown"):
            state.advanceTime(state.fireRateTimers["s"] - frameOffset)

def useOverhead(state: State, keepGOHTAvailable: bool = False):
    state.pushLog("started overhead slam", ["action started"])
    
    # minor warning if no overhead is available
    if (state.hasSwingOverhead == False) and (state.hasDoubleJump == False):
        state.pushLog("used potentially illegal overhead", ["minor warning", "overhead warning"])

    # deal damage
    state.dealDamage("o", frameOffset=ACTION_DAMAGE_TIME["o"])
    state.procTag(frameOffset=ACTION_DAMAGE_TIME["o"], keepGOHTAvailable=keepGOHTAvailable)

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

def applyOverhead(state: State):
    state.advanceTime(state.animationCancelTimes["o"])
    awaitOverheadReady(state)
    useOverhead(state)
      
State.ApplyAction["o"] = applyOverhead


#=========================================================================================================#
#                                                 Tracer                                                  #
#=========================================================================================================#

def useTracer(state: State):
    state.pushLog("started tracer", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("t")
    
    # deal damage (function handles tag application)
    state.dealDamage("t", frameOffset=ACTION_DAMAGE_TIME["t"])
    state.appplyTag(frameOffset=ACTION_DAMAGE_TIME["t"])

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

def applyTracer(state: State):
    state.advanceTime(state.animationCancelTimes["t"]) 
    state.awaitCharge("t")
    useTracer(state)
      
State.ApplyAction["t"] = applyTracer


#=========================================================================================================#
#                                               Swing Whiff                                               #
#=========================================================================================================#

def useWhiff(state: State):
    state.pushLog("started swing whiff", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("s")
    
    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["w"][action]

    # set ability to active state
    state.activeTimers["s"] = ACTIVE_TIMES["w"]

    # cancel active abilities
    state.endActive("u")
    state.endActive("g")
    state.endActive("S")

def applyWhiff(state: State):
    state.advanceTime(state.animationCancelTimes["s"]) 
    state.awaitCharge("s")
    useWhiff(state)
      
State.ApplyAction["w"] = applyWhiff


#=========================================================================================================#
#                                               Auto Swing                                                #
#=========================================================================================================#

def useAutoswing(state: State):
    state.pushLog("started auto swing", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("s")

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["a"][action]

    # set ability to active state
    state.activeTimers["s"] = ACTIVE_TIMES["a"]

    # cancel active abilities
    state.endActive("u")
    state.endActive("g")
    state.endActive("S")

def applyAutoswing(state: State):
    state.advanceTime(state.animationCancelTimes["s"]) 
    state.awaitCharge("s")
    useAutoswing(state)
      
State.ApplyAction["a"] = applyAutoswing


#=========================================================================================================#
#                                              Get Over Here                                              #
#=========================================================================================================#

def useGOH(state: State):
    state.pushLog("started get over here", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("g")

    # deal damage
    state.dealDamage("g", frameOffset=ACTION_DAMAGE_TIME["g"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["g"][action]

    # set ability to active state
    state.activeTimers["g"] = ACTIVE_TIMES["g"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("S")

def applyGOH(state: State):
    state.advanceTime(state.animationCancelTimes["g"]) 
    state.awaitCharge("g")
    useGOH(state)

State.ApplyAction["g"] = applyGOH


#=========================================================================================================#
#                                        Get Over Here (Targeting)                                        #
#=========================================================================================================#

def awaitGOHTReady(state: State, frameOffset: int = 0):
    state.awaitCharge("g")

    # tag applied but not yet registered
    if state.tagTimer > frameOffset + (TAG_DURATION - TAG_GOHT_DELAY):
        state.pushLog("get over here (targetting) awaiting tracer registering", ["waiting"])
        state.advanceTime(state.tagTimer - frameOffset - (TAG_DURATION - TAG_GOHT_DELAY))

    # awaiting bomb explosion
    if (state.GOHTAvaiableTimer <= frameOffset) and state.isTaggedBomb:
        state.pushLog("get over here (targetting) awaiting web bomb explosion", ["waiting"])
        state.advanceTime(state.bombTimer + TAG_GOHT_DELAY - frameOffset)

def useGOHT(state: State):
    state.pushLog("started get over here (targeting)", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("g")

    # major warning if no tag is applied
    if state.tagTimer == 0:
        state.pushLog("used illegal get over here (targeting)", ["major warning"])

    # deal damage
    state.dealDamage("G", frameOffset=ACTION_DAMAGE_TIME["G"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["G"][action]

    # set ability to active state
    state.activeTimers["g"] = ACTIVE_TIMES["G"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("S")

def applyGOHT(state: State):
    state.advanceTime(state.animationCancelTimes["g"]) 
    awaitGOHTReady(state)
    useGOHT(state)
      
State.ApplyAction["G"] = applyGOHT


#=========================================================================================================#
#                                                Uppercut                                                 #
#=========================================================================================================#

def useUppercut(state: State, keepGOHTAvailable: bool = False):
    state.pushLog("started uppercut", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("u")

    # deal damage
    state.dealDamage("u", frameOffset=ACTION_DAMAGE_TIME["u"])
    state.procTag(frameOffset=ACTION_DAMAGE_TIME["u"], keepGOHTAvailable=keepGOHTAvailable)

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["u"][action]

    # set ability to active state
    state.activeTimers["u"] = ACTIVE_TIMES["u"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("S")

def applyUppercut(state: State):
    state.advanceTime(state.animationCancelTimes["u"]) 
    state.awaitCharge("u")
    useUppercut("u")
      
State.ApplyAction["u"] = applyUppercut


#=========================================================================================================#
#                                                Symbiote                                                 #
#=========================================================================================================#

def useSymbiote(state: State):
    state.pushLog("started symbiote", ["action started"])
    
    # major warning if cooldown is not ready
    state.warnIfNotReady("S")

    # deal damage
    state.dealDamage("S", frameOffset=ACTION_DAMAGE_TIME["S"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["S"][action]

    # set ability to active state
    state.activeTimers["S"] = ACTIVE_TIMES["S"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("g")
    state.endActive("u")

def applySymbiote(state: State):
    state.advanceTime(state.animationCancelTimes["S"]) 
    state.awaitCharge("S")
      
State.ApplyAction["S"] = applySymbiote


#=========================================================================================================#
#                                            Symbiote Teather                                             #
#=========================================================================================================#

def useTeather(state: State):
    useSymbiote(state)
    state.teatherTimer = SYMBIOTE_MAX_DURATION

def applyTeather(state: State):
    applySymbiote(state)
    state.teatherTimer = SYMBIOTE_MAX_DURATION

State.ApplyAction["V"] = applyTeather


#=========================================================================================================#
#                                                  Clap                                                   #
#=========================================================================================================#

def useClap(state: State):
    state.pushLog("started clap", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("B")

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

def applyClap(state: State):
    state.advanceTime(state.animationCancelTimes["C"]) 
    state.awaitCharge("B")
    useClap(state)
      
State.ApplyAction["C"] = applyClap


#=========================================================================================================#
#                                                Web Bomb                                                 #
#=========================================================================================================#

def useBomb(state: State):
    state.pushLog("started clap", ["action started"])

    # major warning if bomb is not available
    if state.bombTimer == 0:
        state.pushLog("used illegal web bomb", ["major warning"])

    # deal damage
    state.dealDamage("B", frameOffset=ACTION_DAMAGE_TIME["B"])

    # set bomb timer to minimum allowed time after connecting
    state.isTaggedBomb = True
    state.bombTimer = max(state.bombTimer, ACTION_DAMAGE_TIME["B"] + WEB_BOMB_TAG_DURATION)

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["B"][action]

    # cancel active abilities
    state.endActive("s")

def applyBomb(state: State):
    state.advanceTime(state.animationCancelTimes["B"]) 
    useBomb(state)
      
State.ApplyAction["B"] = applyBomb


#=========================================================================================================#
#                                           Web Bomb Explosion                                            #
#=========================================================================================================#

def applyExplosion(state: State):

    # wait for queued attacks to hit
    state.advanceTime(state.lastDamageTime - state.timeElapsed)

    # major warning if bomb is not active
    if state.bombTimer == 0:
        state.log("used illegal explosion", ["major warning"])
        return

    # await explosion
    state.log("awaiting web bomb explosion", ["waiting"])
    state.advanceTime(state.bombTimer) 
      
State.ApplyAction["E"] = applyExplosion