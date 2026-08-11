from karen.actions.actionData import *
from karen.state import State
from karen.actions.basicActions import *

#=========================================================================================================#
#                                               FFAmestack                                                #
#=========================================================================================================#

def applyFFAmestack(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["g"]) 

    # awaiting actions availability
    awaitGOHTReady(state)
    awaitUppercutReady(state, frameOffset=1)

    # action sequence
    useGOHT(state)
    state.advanceTime(1)
    state.pushActionLog("G+u", frameOffset=ACTION_DAMAGE_TIME["u"])
    useUppercut(state)

    # following swing / symbiote must await goht finishing
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1

State.ApplyAction["G+u"] = applyFFAmestack


#=========================================================================================================#
#                                              Punch Saporen                                              #
#=========================================================================================================#

def applyPunchSaporen(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitPunchReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME))

    # action sequence
    state.pushActionLog("p+G", frameOffset=ACTION_DAMAGE_TIME["p"])
    usePunch(state)
    state.advanceTime(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)

State.ApplyAction["p+G"] = applyPunchSaporen


#=========================================================================================================#
#                                              Kick Saporen                                               #
#=========================================================================================================#

def applyKickSaporen(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitKickReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME))

    # action sequence
    state.pushActionLog("k+G", frameOffset=ACTION_DAMAGE_TIME["k"])
    useKick(state)
    state.advanceTime(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)

State.ApplyAction["k+G"] = applyKickSaporen


#=========================================================================================================#
#                                            Overhead Saporen                                             #
#=========================================================================================================#

def applyOverheadSaporen(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["o"])

    # awaiting actions availability
    awaitOverheadReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME))

    # action sequence
    state.pushActionLog("o+G", frameOffset=ACTION_DAMAGE_TIME["o"])
    useOverhead(state)
    state.advanceTime(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.GOHTAvaiableTimer = 0

State.ApplyAction["o+G"] = applyOverheadSaporen


#=========================================================================================================#
#                                        Punch Saporen FFAmestack                                         #
#=========================================================================================================#

def applyPunchSaporenFFAmestack(state: State, weaveExplosion: bool = False):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitPunchReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME))
    awaitUppercutReady(state, frameOffset=(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME + 1))

    # weave explosion variation
    if weaveExplosion:
        if state.bombTimer > ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME + 1 + ACTION_DAMAGE_TIME["u"]:
            state.pushLog(f"awaiting {ACTION_NAMES["B"]} explosion", ["waiting"])
            state.advanceTime(state.bombTimer - (ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME + 1 + ACTION_DAMAGE_TIME["u"]))

    # action sequence
    state.pushActionLog("p+G+E+u" if weaveExplosion else "p+G+u", frameOffset=ACTION_DAMAGE_TIME["p"])
    usePunch(state)
    state.advanceTime(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.advanceTime(1)

    # weave explosion test
    if weaveExplosion and not ((state.tagTimer > ACTION_DAMAGE_TIME["u"]) or (state.bombTimer <= ACTION_DAMAGE_TIME["u"])):
        state.pushLog("explosion weave failed", ["major warning"])

    useUppercut(state)

    # following swing / symbiote must await goht finishing
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1

State.ApplyAction["p+G+u"] = applyPunchSaporenFFAmestack


#=========================================================================================================#
#                                         Kick Saporen FFAmestack                                         #
#=========================================================================================================#

def applyKickSaporenFFAmestack(state: State, weaveExplosion: bool = False):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitKickReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME))
    awaitUppercutReady(state, frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME + 1))

    # weave explosion variation
    if weaveExplosion:
        if state.bombTimer > ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME + 1 + ACTION_DAMAGE_TIME["u"]:
            state.pushLog(f"awaiting {ACTION_NAMES["B"]} explosion", ["waiting"])
            state.advanceTime(state.bombTimer - (ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME + 1 + ACTION_DAMAGE_TIME["u"]))

    # action sequence
    state.pushActionLog("k+G+E+u" if weaveExplosion else "k+G+u", frameOffset=ACTION_DAMAGE_TIME["k"])
    useKick(state)
    state.advanceTime(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.advanceTime(1)

    # weave explosion test
    if weaveExplosion and not ((state.tagTimer > ACTION_DAMAGE_TIME["u"]) or (state.bombTimer <= ACTION_DAMAGE_TIME["u"])):
        state.pushLog("explosion weave failed", ["major warning"])

    useUppercut(state)

    # following swing / symbiote must await goht finishing
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1

State.ApplyAction["k+G+u"] = applyKickSaporenFFAmestack


#=========================================================================================================#
#                                       Overhead Saporen FFAmestack                                       #
#=========================================================================================================#

def applyOverheadSaporenFFAmestack(state: State, weaveExplosion: bool = False):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["o"])

    # awaiting actions availability
    awaitOverheadReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME))
    awaitUppercutReady(state, frameOffset=(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME + 1))

    # weave explosion variation
    if weaveExplosion:
        if state.bombTimer > ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME + 1 + ACTION_DAMAGE_TIME["u"]:
            state.pushLog(f"awaiting {ACTION_NAMES["B"]} explosion", ["waiting"])
            state.advanceTime(state.bombTimer - (ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME + 1 + ACTION_DAMAGE_TIME["u"]))

    # action sequence
    state.pushActionLog("o+G+E+u" if weaveExplosion else "o+G+u", frameOffset=ACTION_DAMAGE_TIME["o"])
    useOverhead(state)
    state.advanceTime(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.advanceTime(1)

    # weave explosion test
    if weaveExplosion and not ((state.tagTimer > ACTION_DAMAGE_TIME["u"]) or (state.bombTimer <= ACTION_DAMAGE_TIME["u"])):
        state.pushLog("explosion weave failed", ["major warning"])

    useUppercut(state)

    # following swing / symbiote must await goht finishing
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1

State.ApplyAction["o+G+u"] = applyOverheadSaporenFFAmestack


#=========================================================================================================#
#                                                Space Jam                                                #
#=========================================================================================================#

def applySpaceJam(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["o"])

    # awaiting actions availability
    awaitUppercutReady(state)
    state.awaitCharge("s", frameOffset=ANIMATION_CANCEL_TIMES["u"]["s"])
    awaitGOHTReady(state, frameOffset=(ANIMATION_CANCEL_TIMES["u"]["s"] + ANIMATION_CANCEL_TIMES["w"]["G"]))

    # action sequence
    state.pushActionLog("u+w+G", frameOffset=ACTION_DAMAGE_TIME["u"])
    useUppercut(state)
    state.advanceTime(ANIMATION_CANCEL_TIMES["u"]["s"])
    useWhiff(state)
    state.advanceTime(ANIMATION_CANCEL_TIMES["w"]["G"])
    useGOHT(state)

State.ApplyAction["u+w+G"] = applySpaceJam


#=========================================================================================================#
#                                         Space Jam (Auto Swing)                                          #
#=========================================================================================================#

def applyFastSpaceJam(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["o"])

    # awaiting actions availability
    awaitUppercutReady(state)
    state.awaitCharge("s", frameOffset=ANIMATION_CANCEL_TIMES["u"]["s"])
    awaitGOHTReady(state, frameOffset=(ANIMATION_CANCEL_TIMES["u"]["s"] + ANIMATION_CANCEL_TIMES["a"]["G"]))

    # action sequence
    state.pushActionLog("u+a+G", frameOffset=ACTION_DAMAGE_TIME["u"])
    useUppercut(state)
    state.advanceTime(ANIMATION_CANCEL_TIMES["u"]["s"])
    useAutoswing(state)
    state.advanceTime(ANIMATION_CANCEL_TIMES["a"]["G"])
    useGOHT(state)

State.ApplyAction["u+a+G"] = applyFastSpaceJam


#=========================================================================================================#
#                                          Punch Reverse Trigger                                          #
#=========================================================================================================#

def applyPunchRT(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitPunchReady(state)
    state.awaitCharge("t", ACTION_DAMAGE_TIME["p"] - RT_PRE_HIT_TIME)

    # action sequence
    state.pushActionLog("p+t", frameOffset=ACTION_DAMAGE_TIME["p"])
    usePunch(state)
    state.advanceTime(ACTION_DAMAGE_TIME["p"] - RT_PRE_HIT_TIME)
    useTracer(state)
    state.procTag(frameOffset=ACTION_DAMAGE_TIME["t"])

State.ApplyAction["p+t"] = applyPunchRT


#=========================================================================================================#
#                                          Kick Reverse Trigger                                           #
#=========================================================================================================#

def applyKickRT(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitKickReady(state)
    state.awaitCharge("t", ACTION_DAMAGE_TIME["k"] - RT_PRE_HIT_TIME)

    # action sequence
    state.pushActionLog("k+t", frameOffset=ACTION_DAMAGE_TIME["k"])
    useKick(state)
    state.advanceTime(ACTION_DAMAGE_TIME["k"] - RT_PRE_HIT_TIME)
    useTracer(state)
    state.procTag(frameOffset=ACTION_DAMAGE_TIME["t"])

State.ApplyAction["k+t"] = applyKickRT


#=========================================================================================================#
#                                        Overhead Reverse Trigger                                         #
#=========================================================================================================#

def applyOverheadRT(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["o"])

    # awaiting actions availability
    awaitOverheadReady(state)
    state.awaitCharge("t", ACTION_DAMAGE_TIME["o"] - RT_PRE_HIT_TIME)

    # action sequence
    state.pushActionLog("o+t", frameOffset=ACTION_DAMAGE_TIME["o"])
    useOverhead(state)
    state.advanceTime(ACTION_DAMAGE_TIME["o"] - RT_PRE_HIT_TIME)
    useTracer(state)
    state.procTag(frameOffset=ACTION_DAMAGE_TIME["t"])

State.ApplyAction["o+t"] = applyOverheadRT


#=========================================================================================================#
#                                           Unique X Hit Punch                                            #
#=========================================================================================================#

def applyPunchU3H(state: State, weaveExplosion: bool = False):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitPunchReady(state)

    # weave explosion variation
    if weaveExplosion:
        if state.bombTimer > state.activeTimers["s"] + ACTION_DAMAGE_TIME["o"]:
            state.pushLog(f"awaiting {ACTION_NAMES["B"]} explosion", ["waiting"])
            state.advanceTime(state.bombTimer - (state.activeTimers["s"] + ACTION_DAMAGE_TIME["o"]))

    # action sequence
    state.pushActionLog("p+E+o" if weaveExplosion else "p+o", frameOffset=ACTION_DAMAGE_TIME["p"])
    usePunch(state)
    state.advanceTime(state.activeTimers["s"])

    # weave explosion test
    if weaveExplosion and not ((state.tagTimer > ACTION_DAMAGE_TIME["o"]) or (state.bombTimer <= ACTION_DAMAGE_TIME["o"])):
        state.pushLog("explosion weave failed", ["major warning"])

    useOverhead(state)

State.ApplyAction["p+o"] = applyPunchU3H


#=========================================================================================================#
#                                            Unique X Hit Kick                                            #
#=========================================================================================================#

def applyKickU3H(state: State, weaveExplosion: bool = False):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitPunchReady(state)

    # weave explosion variation
    if weaveExplosion:
        if state.bombTimer > state.activeTimers["s"] + ACTION_DAMAGE_TIME["o"]:
            state.pushLog(f"awaiting {ACTION_NAMES["B"]} explosion", ["waiting"])
            state.advanceTime(state.bombTimer - (state.activeTimers["s"] + ACTION_DAMAGE_TIME["o"]))

    # action sequence
    state.pushActionLog("k+E+o" if weaveExplosion else "k+o", frameOffset=ACTION_DAMAGE_TIME["k"])
    useKick(state)
    state.advanceTime(state.activeTimers["s"])

    # weave explosion test
    if weaveExplosion and not ((state.tagTimer > ACTION_DAMAGE_TIME["o"]) or (state.bombTimer <= ACTION_DAMAGE_TIME["o"])):
        state.pushLog("explosion weave failed", ["major warning"])

    useOverhead(state)

State.ApplyAction["k+o"] = applyKickU3H


#=========================================================================================================#
#                                             GOH + Web Bomb                                              #
#=========================================================================================================#

def applyGOHBomb(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["g"])

    # awaiting actions availability
    state.awaitCharge("g")

    # action sequence
    state.pushActionLog("g+B")
    useGOH(state)
    state.advanceTime(1)
    useBomb(state)

    # ensure GOH isn't cancelled early
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["g"][action] - 1

State.ApplyAction["g+B"] = applyGOHBomb


#=========================================================================================================#
#                                             GOHT + Web Bomb                                             #
#=========================================================================================================#

def applyGOHTBomb(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["g"])

    # awaiting actions availability
    awaitGOHTReady(state)

    # action sequence
    state.pushActionLog("G+B")
    useGOHT(state)
    state.advanceTime(1)
    useBomb(state)

    # ensure GOHT isn't cancelled early
    for action in state.animationCancelTimes.keys():
        state.animationCancelTimes[action] = ANIMATION_CANCEL_TIMES["G"][action] - 1

State.ApplyAction["G+B"] = applyGOHTBomb


#=========================================================================================================#
#                                       Explosion Weave Movestacks                                        #
#=========================================================================================================#

def applyPunchExplosionSaporenFFAmestack(state: State):
    applyPunchSaporenFFAmestack(state, weaveExplosion=True)
State.ApplyAction["p+G+E+u"] = applyPunchExplosionSaporenFFAmestack
State.ApplyAction["p+E+G+u"] = applyPunchExplosionSaporenFFAmestack

def applyKickExplosionSaporenFFAmestack(state: State):
    applyKickSaporenFFAmestack(state, weaveExplosion=True)
State.ApplyAction["k+G+E+u"] = applyKickExplosionSaporenFFAmestack
State.ApplyAction["k+E+G+u"] = applyKickExplosionSaporenFFAmestack

def applyOverheadExplosionSaporenFFAmestack(state: State):
    applyOverheadSaporenFFAmestack(state, weaveExplosion=True)
State.ApplyAction["o+G+E+u"] = applyOverheadExplosionSaporenFFAmestack
State.ApplyAction["o+E+G+u"] = applyOverheadExplosionSaporenFFAmestack

def applyUniquePunchExplosionOverhead(state: State):
    applyPunchU3H(state, weaveExplosion=True)
State.ApplyAction["p+E+o"] = applyUniquePunchExplosionOverhead

def applyUniqueKickExplosionOverhead(state: State):
    applyKickU3H(state, weaveExplosion=True)
State.ApplyAction["k+E+o"] = applyUniqueKickExplosionOverhead