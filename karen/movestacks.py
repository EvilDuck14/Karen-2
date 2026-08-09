from karen.actionData import *
from karen.state import State

#=========================================================================================================#
#                                               FFAmestack                                                #
#=========================================================================================================#

def applyFFAmestack(state: State):
    pass
State.ApplyAction["G+u"] = applyFFAmestack


#=========================================================================================================#
#                                                 Saporen                                                 #
#=========================================================================================================#

def applyPunchSaporen(state: State):
    pass
State.ApplyAction["p+G"] = applyPunchSaporen

def applyKickSaporen(state: State):
    pass
State.ApplyAction["p+G"] = applyKickSaporen

def applyOverheadSaporen(state: State):
    pass
State.ApplyAction["p+G"] = applyOverheadSaporen


#=========================================================================================================#
#                                           Saporen FFAmestack                                            #
#=========================================================================================================#

def applyPunchSaporenFFAmestack(state: State):
    pass
State.ApplyAction["p+G+u"] = applyPunchSaporenFFAmestack

def applyKickSaporenFFAmestack(state: State):
    pass
State.ApplyAction["p+G+u"] = applyKickSaporenFFAmestack

def applyOverheadSaporenFFAmestack(state: State):
    pass
State.ApplyAction["p+G+u"] = applyOverheadSaporenFFAmestack


#=========================================================================================================#
#                                                Space Jam                                                #
#=========================================================================================================#

def applySpaceJam(state: State):
    pass
State.ApplyAction["u+w+G"] = applySpaceJam

def applyFastSpaceJam(state: State):
    pass
State.ApplyAction["u+a+G"] = applyFastSpaceJam


#=========================================================================================================#
#                                             Reverse Trigger                                             #
#=========================================================================================================#

def applyPunchRT(state: State):
    pass
State.ApplyAction["p+t"] = applyPunchRT

def applyKickRT(state: State):
    pass
State.ApplyAction["k+t"] = applyKickRT

def applyOverheadRT(state: State):
    pass
State.ApplyAction["k+t"] = applyOverheadRT


#=========================================================================================================#
#                                              Unique X Hit                                               #
#=========================================================================================================#

def applyPunchU3H(state: State):
    pass
State.ApplyAction["p+o"] = applyPunchU3H

def applyKickU3H(state: State):
    pass
State.ApplyAction["p+o"] = applyKickU3H

def applyPunchU2H(state: State):
    pass
State.ApplyAction["a+p+o"] = applyPunchU2H

def applyKickU2H(state: State):
    pass
State.ApplyAction["a+p+o"] = applyKickU2H