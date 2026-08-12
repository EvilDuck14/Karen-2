from karen.actions.actionData import *
from karen.state import State

#=========================================================================================================#
#                                                  Punch                                                  #
#=========================================================================================================#

def awaitPunchReady(state: State, frameOffset: int = 0):

    # await kick expiration
    if (state.meleeSequenceStep == "kick") and (state.meleeSequenceTimer > frameOffset):
        state.pushLog("awaiting melee sequence timer expiration", ["waiting"])
        if state.meleeSequenceTimer - frameOffset >= (ACTION_DAMAGE_TIME["k"] - ACTION_DAMAGE_TIME["p"]):
            state.pushLog(f"waiting for {ACTION_NAMES["p"]} when {ACTION_NAMES["k"]} would likely be faster", ["sequence warning"])
        state.advanceTime(state.meleeSequenceTimer - frameOffset)

    # await clap/bomb animation
    if state.fireRateTimers["C"] > frameOffset:
        state.pushLog(f"awaiting Peni team-up animation", ["waiting"])
        state.advanceTime(state.fireRateTimers["C"] - frameOffset)

    # await web bomb explosion
    if state.awaitingExplosion and (state.bombTimer > frameOffset + ACTION_DAMAGE_TIME["p"]):
        state.explosionWaitTimer = state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["p"])
        state.pushLog(f"awaiting {ACTION_NAMES["E"]}", ["waiting"])
        state.pushActionLog(f"[{state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["p"])}f]")
        state.advanceTime(state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["p"]))

def usePunch(state: State):
    state.pushLog(f"started {ACTION_NAMES["p"]}", ["action started"])

    # major warning if punch started while kick was available
    if state.meleeSequenceStep == "kick":
        state.pushLog(f"used {ACTION_NAMES["p"]} when {ACTION_NAMES["k"]} was expected", ["dev warning"])

    # minor warning if swing overhead is available
    if state.hasSwingOverhead == True:
        state.pushLog(f"used {ACTION_NAMES["p"]} when {ACTION_NAMES["o"]} was expected", ["minor warning", "overhead warning"])

    # deal damage
    state.dealDamage("p", frameOffset=ACTION_DAMAGE_TIME["p"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["p"][action]

    # tracking melee sequence
    state.meleeSequenceTimer = MELEE_SEQUENCE_WINDOW
    if state.meleeSequenceStep == "punch 1":
        state.meleeSequenceStep = "punch 2"
    elif state.meleeSequenceStep in ["punch 2", "not punch 1"]:
        state.meleeSequenceStep = "kick"
    elif state.meleeSequenceStep == "unknown":
        state.meleeSequenceStep = "not punch 1"

    # cancel symbiote teather
    state.endActive("S")

def applyPunch(state: State):
    state.advanceTime(state.animationCancelTimes["p"]) 
    awaitPunchReady(state)
    state.pushActionLog("p", frameOffset=ACTION_DAMAGE_TIME["p"])
    usePunch(state)
      
State.ApplyAction["p"] = applyPunch


#=========================================================================================================#
#                                                  Kick                                                   #
#=========================================================================================================#

def awaitKickReady(state: State, frameOffset: int = 0):

    # await clap/bomb animation
    if state.fireRateTimers["C"] > frameOffset:
        state.pushLog(f"awaiting Peni team-up animation", ["waiting"])
        state.advanceTime(state.fireRateTimers["C"] - frameOffset)

    # await web bomb explosion
    if state.awaitingExplosion and (state.bombTimer > frameOffset + ACTION_DAMAGE_TIME["k"]):
        state.explosionWaitTimer = state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["k"])
        state.pushLog(f"awaiting {ACTION_NAMES["E"]}", ["waiting"])
        state.pushActionLog(f"[{state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["k"])}f]")
        state.advanceTime(state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["k"]))

def useKick(state: State):
    state.pushLog(f"started {ACTION_NAMES["k"]}", ["action started"])

    # major warning if kick is not available
    if state.meleeSequenceStep in ["punch 1", "punch 2"]:
        state.pushLog(f"used illegal {ACTION_NAMES["k"]}", ["major warning"])

    # minor warning if swing overhead is available
    if state.hasSwingOverhead == True:
        state.pushLog(f"used {ACTION_NAMES["k"]} when {ACTION_NAMES["o"]} was expected", ["minor warning", "overhead warning"])

    # deal damage
    state.dealDamage("k", frameOffset=ACTION_DAMAGE_TIME["k"])

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
    awaitKickReady(state)
    state.pushActionLog("k", frameOffset=ACTION_DAMAGE_TIME["k"])
    useKick(state)
      
State.ApplyAction["k"] = applyKick


#=========================================================================================================#
#                                              Overhead Slam                                              #
#=========================================================================================================#

def awaitOverheadReady(state: State, frameOffset: int = 0):

    # await swing whiff end
    if (state.activeTimers["s"] > frameOffset) and (state.hasSwingOverhead != True):
        state.pushLog(f"used {ACTION_NAMES["o"]} after {ACTION_NAMES["w"]} - was U3H intended?", ["sequence warning"])

        # if an immediate overhead available, using it gives a faster overhead, otherwise await swing whiff end
        if not (state.hasDoubleJump or state.hasSwingOverhead == "unknown"):
            state.advanceTime(state.activeTimers["s"] - frameOffset)

    # await clap/bomb animation
    if state.fireRateTimers["C"] > frameOffset:
        state.pushLog(f"awaiting Peni team-up animation", ["waiting"])
        state.advanceTime(state.fireRateTimers["C"] - frameOffset)

    # await web bomb explosion
    if state.awaitingExplosion and (state.bombTimer > frameOffset + ACTION_DAMAGE_TIME["o"]):
        state.explosionWaitTimer = state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["o"])
        state.pushLog(f"awaiting {ACTION_NAMES["E"]}", ["waiting"])
        state.pushActionLog(f"[{state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["o"])}f]")
        state.advanceTime(state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["o"]))

def useOverhead(state: State):
    state.pushLog(f"started {ACTION_NAMES["o"]}", ["action started"])
    
    # minor warning if no overhead is available
    if (state.hasSwingOverhead == False) and (state.hasDoubleJump == False):
        state.pushLog(f"used unexpected {ACTION_NAMES["o"]}", ["minor warning", "overhead warning"])

    # deal damage
    state.dealDamage("o", frameOffset=ACTION_DAMAGE_TIME["o"])

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
    state.pushActionLog("o", frameOffset=ACTION_DAMAGE_TIME["o"])
    useOverhead(state)
      
State.ApplyAction["o"] = applyOverhead


#=========================================================================================================#
#                                                 Tracer                                                  #
#=========================================================================================================#

def useTracer(state: State):
    state.pushLog(f"started {ACTION_NAMES["t"]}", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("t")
    
    # deal damage
    state.dealDamage("t", frameOffset=ACTION_DAMAGE_TIME["t"])

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
    state.fireRateTimers["C"] = 0

def applyTracer(state: State):
    state.advanceTime(state.animationCancelTimes["t"]) 
    state.awaitCharge("t")
    state.pushActionLog("t")
    useTracer(state)
      
State.ApplyAction["t"] = applyTracer


#=========================================================================================================#
#                                               Swing Whiff                                               #
#=========================================================================================================#

def useWhiff(state: State):
    state.pushLog(f"started {ACTION_NAMES["w"]}", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("s")
 
    # ensures swing charge is not consumed
    state.swingIsWhiff = True

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
    state.pushActionLog("w")
    useWhiff(state)
      
State.ApplyAction["w"] = applyWhiff


#=========================================================================================================#
#                                               Auto Swing                                                #
#=========================================================================================================#

def useAutoswing(state: State):
    state.pushLog(f"started {ACTION_NAMES["a"]}", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("s")

    # ensures swing charge is consumed
    state.swingIsWhiff = False

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
    state.pushActionLog("a")
    useAutoswing(state)
      
State.ApplyAction["a"] = applyAutoswing


#=========================================================================================================#
#                                              Get Over Here                                              #
#=========================================================================================================#

def useGOH(state: State):
    state.pushLog(f"started {ACTION_NAMES["g"]}", ["action started"])

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
    state.fireRateTimers["C"] = 0

def applyGOH(state: State):
    state.advanceTime(state.animationCancelTimes["g"]) 
    state.awaitCharge("g")
    state.pushActionLog("g")
    useGOH(state)

State.ApplyAction["g"] = applyGOH


#=========================================================================================================#
#                                        Get Over Here (Targeting)                                        #
#=========================================================================================================#

def awaitGOHTReady(state: State, frameOffset: int = 0):
    state.awaitCharge("g")

    # tag applied but not yet registered
    if state.tagTimer > frameOffset + (TAG_DURATION - TAG_GOHT_DELAY):
        state.pushLog(f"{ACTION_NAMES["G"]} awaiting tag registering", ["waiting"])
        state.advanceTime(state.tagTimer - frameOffset - (TAG_DURATION - TAG_GOHT_DELAY))

    # awaiting bomb explosion
    if (state.GOHTAvaiableTimer <= frameOffset) and state.isTaggedBomb:
        state.pushLog(f"{ACTION_NAMES["G"]} awaiting {ACTION_NAMES["B"]} explosion", ["waiting"])
        state.advanceTime(state.bombTimer + TAG_GOHT_DELAY - frameOffset)

def useGOHT(state: State):
    state.pushLog(f"started {ACTION_NAMES["G"]}", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("g")

    # major warning if no tag is available
    if state.GOHTAvaiableTimer == 0:
        state.pushLog(f"used illegal {ACTION_NAMES["G"]}", ["major warning"])

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
    state.pushActionLog("G")
    useGOHT(state)
      
State.ApplyAction["G"] = applyGOHT


#=========================================================================================================#
#                                                Uppercut                                                 #
#=========================================================================================================#

def awaitUppercutReady(state: State, frameOffset: int = 0):
    state.awaitCharge("u")

    # await web bomb explosion
    if state.awaitingExplosion and (state.bombTimer > frameOffset + ACTION_DAMAGE_TIME["u"]):
        state.explosionWaitTimer = state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["u"])
        state.pushLog(f"awaiting {ACTION_NAMES["E"]}", ["waiting"])
        state.pushActionLog(f"[{state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["u"])}f]")
        state.advanceTime(state.bombTimer - (frameOffset + ACTION_DAMAGE_TIME["u"]))

def useUppercut(state: State):
    state.pushLog(f"started {ACTION_NAMES["u"]}", ["action started"])

    # major warning if cooldown is not ready
    state.warnIfNotReady("u")

    # deal damage
    state.dealDamage("u", frameOffset=ACTION_DAMAGE_TIME["u"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["u"][action]

    # set ability to active state
    state.activeTimers["u"] = ACTIVE_TIMES["u"]

    # refresh double jump
    if not state.hasDoubleJump:
        state.hasDoubleJump = True
        state.pushLog("refreshed double jump", ["cooldown"])

    # cancel active abilities
    state.endActive("s")
    state.endActive("S")

def applyUppercut(state: State):
    state.advanceTime(state.animationCancelTimes["u"]) 
    awaitUppercutReady(state)
    state.pushActionLog("u", frameOffset=ACTION_DAMAGE_TIME["u"])
    useUppercut(state)
      
State.ApplyAction["u"] = applyUppercut


#=========================================================================================================#
#                                                Symbiote                                                 #
#=========================================================================================================#

def awaitSymbioteReady(state: State, frameOffset: int = 0):

    # allow multiple hits with single usage
    if state.activeTimers["S"] > frameOffset:
        state.advanceTime(state.animationCancelTimes["S"] - frameOffset)
        if state.activeTimers["S"] > frameOffset:
            return

    state.awaitCharge("S", frameOffset=frameOffset)

def useSymbiote(state: State):
    state.pushLog(f"started {ACTION_NAMES["S"]}", ["action started"])
    
    # major warning if cooldown is not ready
    state.warnIfNotReady("S")

    # deal damage
    state.dealDamage("S", frameOffset=ACTION_DAMAGE_TIME["S"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["S"][action]

    # set ability to active state
    if state.activeTimers["S"] == 0:
        state.activeTimers["S"] = ACTIVE_TIMES["S"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("g")
    state.endActive("u")

def applySymbiote(state: State):
    state.advanceTime(state.animationCancelTimes["S"]) 
    awaitSymbioteReady(state)
    state.pushActionLog("S")
    useSymbiote(state)
      
State.ApplyAction["S"] = applySymbiote


#=========================================================================================================#
#                                            Symbiote Teather                                             #
#=========================================================================================================#

def useTeather(state: State):
    state.pushLog(f"started {ACTION_NAMES["V"]}", ["action started"])
        
    # major warning if cooldown is not ready
    state.warnIfNotReady("S")

    # deal damage
    state.dealDamage("S", frameOffset=ACTION_DAMAGE_TIME["S"])

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["S"][action]

    # set ability to active state
    if state.activeTimers["S"] == 0:
        state.activeTimers["S"] = ACTIVE_TIMES["S"]

    # cancel active abilities
    state.endActive("s")
    state.endActive("g")
    state.endActive("u")

    # attach teather - don't reset timer on multiple symbiote hits
    if state.teatherTimer == 0:
        state.teatherTimer = SYMBIOTE_TEATHER_DURATION + ACTION_DAMAGE_TIME["S"]

def applyTeather(state: State):
    state.advanceTime(state.animationCancelTimes["S"]) 
    awaitSymbioteReady(state)
    state.pushActionLog("V")
    useTeather(state)

State.ApplyAction["V"] = applyTeather


#=========================================================================================================#
#                                                  Clap                                                   #
#=========================================================================================================#

def useClap(state: State):
    state.pushLog(f"started {ACTION_NAMES["C"]}", ["action started"])

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

    # fire rate timer stops punch from coming out faster via swing weave
    state.fireRateTimers["C"] = ANIMATION_CANCEL_TIMES["C"]["p"]

    # cancel active abilities
    state.endActive("g")

def applyClap(state: State):
    state.advanceTime(state.animationCancelTimes["C"]) 
    state.awaitCharge("B")
    state.pushActionLog("C")
    useClap(state)
      
State.ApplyAction["C"] = applyClap


#=========================================================================================================#
#                                                Web Bomb                                                 #
#=========================================================================================================#

def useBomb(state: State):
    state.pushLog(f"started {ACTION_NAMES["B"]}", ["action started"])

    # major warning if bomb is not available
    if state.bombTimer == 0:
        state.pushLog(f"used illegal {ACTION_NAMES["B"]}", ["major warning"])

    # deal damage
    state.dealDamage("B", frameOffset=ACTION_DAMAGE_TIME["B"])

    # set bomb timer to minimum allowed time after connecting
    state.isTaggedBomb = True
    state.bombTimer = max(state.bombTimer, ACTION_DAMAGE_TIME["B"] + WEB_BOMB_TAG_DURATION)

    # prepare animation cancel times
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["B"][action]

    # fire rate timer stops punch from coming out faster via swing weave
    state.fireRateTimers["C"] = ANIMATION_CANCEL_TIMES["B"]["p"]

    # cancel active abilities
    state.endActive("s")

def applyBomb(state: State):
    state.advanceTime(state.animationCancelTimes["B"]) 
    state.pushActionLog("B")
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
        state.pushLog(f"used illegal {ACTION_NAMES["E"]}", ["major warning"])
        return

    # await explosion
    state.awaitingExplosion = True
      
State.ApplyAction["E"] = applyExplosion