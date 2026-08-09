from karen.actions.actionData import *
from karen.state import State
from karen.actions.basicActions import *

#=========================================================================================================#
#                                               FFAmestack                                                #
#=========================================================================================================#

def applyFFAmestack(state: State):
    state.advanceTime(state.animationCancelTimes["g"]) 
    awaitGOHTReady(state)
    state.awaitCharge("u", frameOffset=1)
    useGOHT(state)
    state.advanceTime(1)
    useUppercut(state)
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1
State.ApplyAction["G+u"] = applyFFAmestack


#=========================================================================================================#
#                                              Punch Saporen                                              #
#=========================================================================================================#

def applyPunchSaporen(state: State):
    state.advanceTime(state.animationCancelTimes["p"])
    awaitPunchReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME))
    usePunch(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.GOHTAvaiableTimer = 0
State.ApplyAction["p+G"] = applyPunchSaporen


#=========================================================================================================#
#                                              Kick Saporen                                               #
#=========================================================================================================#

def applyKickSaporen(state: State):
    state.advanceTime(state.animationCancelTimes["p"])
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME))
    useKick(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.GOHTAvaiableTimer = 0
State.ApplyAction["k+G"] = applyKickSaporen


#=========================================================================================================#
#                                            Overhead Saporen                                             #
#=========================================================================================================#

def applyOverheadSaporen(state: State):
    state.advanceTime(state.animationCancelTimes["o"])
    awaitOverheadReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME))
    useOverhead(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.GOHTAvaiableTimer = 0
State.ApplyAction["o+G"] = applyOverheadSaporen


#=========================================================================================================#
#                                        Punch Saporen FFAmestack                                         #
#=========================================================================================================#

def applyPunchSaporenFFAmestack(state: State):
    state.advanceTime(state.animationCancelTimes["p"])
    awaitPunchReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME))
    state.awaitCharge("u", frameOffset=(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME + 1))
    usePunch(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["p"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.GOHTAvaiableTimer = 0
    state.advanceTime(1)
    useUppercut(state)
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1
State.ApplyAction["p+G+u"] = applyPunchSaporenFFAmestack


#=========================================================================================================#
#                                         Kick Saporen FFAmestack                                         #
#=========================================================================================================#

def applyKickSaporenFFAmestack(state: State):
    state.advanceTime(state.animationCancelTimes["p"])
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME))
    state.awaitCharge("u", frameOffset=(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME + 1))
    useKick(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["k"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.GOHTAvaiableTimer = 0
    state.advanceTime(1)
    useUppercut(state)
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1
State.ApplyAction["k+G+u"] = applyKickSaporenFFAmestack


#=========================================================================================================#
#                                       Overhead Saporen FFAmestack                                       #
#=========================================================================================================#

def applyOverheadSaporenFFAmestack(state: State):
    state.advanceTime(state.animationCancelTimes["o"])
    awaitOverheadReady(state)
    awaitGOHTReady(state, frameOffset=(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME))
    state.awaitCharge("u", frameOffset=(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME + 1))
    useOverhead(state, keepGOHTAvailable=True)
    state.advanceTime(ACTION_DAMAGE_TIME["o"] - SAPOREN_PRE_HIT_TIME)
    useGOHT(state)
    state.GOHTAvaiableTimer = 0
    state.advanceTime(1)
    useUppercut(state)
    state.animationCancelTimes["s"] = ANIMATION_CANCEL_TIMES["G"]["s"] - 1
    state.animationCancelTimes["S"] = ANIMATION_CANCEL_TIMES["G"]["S"] - 1
State.ApplyAction["o+G+u"] = applyOverheadSaporenFFAmestack


#=========================================================================================================#
#                                                Space Jam                                                #
#=========================================================================================================#

def applySpaceJam(state: State):
    pass
State.ApplyAction["u+w+G"] = applySpaceJam


#=========================================================================================================#
#                                         Space Jam (Auto Swing)                                          #
#=========================================================================================================#

def applyFastSpaceJam(state: State):
    pass
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
#                                           Unique 2 Hit Punch                                            #
#=========================================================================================================#

def applyPunchU2H(state: State):
    pass
State.ApplyAction["a+p+o"] = applyPunchU2H


#=========================================================================================================#
#                                            Unique 2 Hit Kick                                            #
#=========================================================================================================#

def applyKickU2H(state: State):
    pass
State.ApplyAction["a+p+o"] = applyKickU2H


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
State.ApplyAction["C+a"]