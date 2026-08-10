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
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME))

    # action sequence
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
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME))
    state.awaitCharge("u", frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME + 1))

    # action sequence
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
    pass
State.ApplyAction["p+t"] = applyPunchRT


#=========================================================================================================#
#                                          Kick Reverse Trigger                                           #
#=========================================================================================================#

def applyKickRT(state: State):
    pass
State.ApplyAction["k+t"] = applyKickRT


#=========================================================================================================#
#                                        Overhead Reverse Trigger                                         #
#=========================================================================================================#

def applyOverheadRT(state: State):
    pass
State.ApplyAction["k+t"] = applyOverheadRT


#=========================================================================================================#
#                                           Unique 3 Hit Punch                                            #
#=========================================================================================================#

def applyPunchU3H(state: State):
    pass
State.ApplyAction["p+o"] = applyPunchU3H


#=========================================================================================================#
#                                            Unique 3 Hit Kick                                            #
#=========================================================================================================#

def applyKickU3H(state: State):
    pass
State.ApplyAction["p+o"] = applyKickU3H


#=========================================================================================================#
#                                             GOH + Web Bomb                                              #
#=========================================================================================================#

def applyGOHBomb(state: State):
    pass
State.ApplyAction["g+B"] = applyGOHBomb


#=========================================================================================================#
#                                             GOHT + Web Bomb                                             #
#=========================================================================================================#

def applyGOHTBomb(state: State):
    pass
State.ApplyAction["g+B"] = applyGOHTBomb


#=========================================================================================================#
#                                           Clap + Swing Whiff                                            #
#=========================================================================================================#

def applyWhiffClap(state: State):
    pass
State.ApplyAction["w+C"] = applyWhiffClap


#=========================================================================================================#
#                                            Clap + Auto Swing                                            #
#=========================================================================================================#

def applyAutoswingClap(state: State):
    pass
State.ApplyAction["a+C"] = applyAutoswingClap


#=========================================================================================================#
#                                           Swing Whiff + Clap                                            #
#=========================================================================================================#

def applyClapAutoswing(state: State):
    pass
State.ApplyAction["C+a"] = applyClapAutoswing