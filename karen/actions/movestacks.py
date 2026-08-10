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
    state.awaitCharge("u", frameOffset=1)

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
    usePunch(state, keepGOHTAvailable=True)
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
    useKick(state, keepGOHTAvailable=True)
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
    useOverhead(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.GOHTAvaiableTimer = 0

State.ApplyAction["o+G"] = applyOverheadSaporen


#=========================================================================================================#
#                                        Punch Saporen FFAmestack                                         #
#=========================================================================================================#

def applyPunchSaporenFFAmestack(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitPunchReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME))
    state.awaitCharge("u", frameOffset=(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME + 1))

    # action sequence
    state.pushActionLog("p+G+u", frameOffset=ACTION_DAMAGE_TIME["p"])
    usePunch(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.advanceTime(1)
    useUppercut(state)

    # following swing / symbiote must await goht finishing
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1

State.ApplyAction["p+G+u"] = applyPunchSaporenFFAmestack


#=========================================================================================================#
#                                         Kick Saporen FFAmestack                                         #
#=========================================================================================================#

def applyKickSaporenFFAmestack(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitKickReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME))
    state.awaitCharge("u", frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME + 1))

    # action sequence
    state.pushActionLog("k+G+u", frameOffset=ACTION_DAMAGE_TIME["k"])
    useKick(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.advanceTime(1)
    useUppercut(state)

    # following swing / symbiote must await goht finishing
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1

State.ApplyAction["k+G+u"] = applyKickSaporenFFAmestack


#=========================================================================================================#
#                                       Overhead Saporen FFAmestack                                       #
#=========================================================================================================#

def applyOverheadSaporenFFAmestack(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["o"])

    # awaiting actions availability
    awaitOverheadReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME))
    state.awaitCharge("u", frameOffset=(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME + 1))

    # action sequence
    state.pushActionLog("o+G+u", frameOffset=ACTION_DAMAGE_TIME["o"])
    useOverhead(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.advanceTime(1)
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
    state.awaitCharge("u")
    state.awaitCharge("s", frameOffset=ANIMATION_CANCEL_TIMES["u"]["s"])
    awaitGOHTReady(state, frameOffset=(ANIMATION_CANCEL_TIMES["u"]["s"] + ANIMATION_CANCEL_TIMES["w"]["G"]))

    # action sequence
    state.pushActionLog("u+w+G", frameOffset=ACTION_DAMAGE_TIME["u"])
    useUppercut(state, keepGOHTAvailable=True)
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
    state.awaitCharge("u")
    state.awaitCharge("s", frameOffset=ANIMATION_CANCEL_TIMES["u"]["s"])
    awaitGOHTReady(state, frameOffset=(ANIMATION_CANCEL_TIMES["u"]["s"] + ANIMATION_CANCEL_TIMES["a"]["G"]))

    # action sequence
    state.pushActionLog("u+a+G", frameOffset=ACTION_DAMAGE_TIME["u"])
    useUppercut(state, keepGOHTAvailable=True)
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

def applyPunchU3H(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitPunchReady(state)

    # action sequence
    state.pushActionLog("p+o", frameOffset=ACTION_DAMAGE_TIME["p"])
    usePunch(state)
    state.advanceTime(state.activeTimers["s"])
    useOverhead(state)

State.ApplyAction["p+o"] = applyPunchU3H


#=========================================================================================================#
#                                            Unique X Hit Kick                                            #
#=========================================================================================================#

def applyKickU3H(state: State):

    # awaiting previous animation
    state.advanceTime(state.animationCancelTimes["p"])

    # awaiting actions availability
    awaitPunchReady(state)

    # action sequence
    state.pushActionLog("k+o", frameOffset=ACTION_DAMAGE_TIME["k"])
    useKick(state)
    state.advanceTime(state.activeTimers["s"])
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
        state.animationCancelTimes[action] = max(state.animationCancelTimes[action], ANIMATION_CANCEL_TIMES["g"][action] - 1) # TO DO: check

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
        state.animationCancelTimes[action] = max(state.animationCancelTimes[action], ANIMATION_CANCEL_TIMES["G"][action] - 1) # TO DO: check

State.ApplyAction["G+B"] = applyGOHTBomb