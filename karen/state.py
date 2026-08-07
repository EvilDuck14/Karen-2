class State:
    sequence = [] # list of actions that have been applied to the state
    detailedLog = [] # stores more information for debugging / advanced users

    timeElapsed = 0 # time from start of combo until current point in calculation
    sequenceTime = 0 # time from start of combo until final queued hit
    firstDamageTime = "unknown" # time that first tick of damage registers
    damageDealt = 0 # cumulative damage counter

    meleeSequenceStep = "punch 1" # tracks whether next melee is a punch or kick
    meleeSequenceTimer = 0 # timer for punch/kick tracking
    isTagged = False # tracks whether regular tracer tag is applied
    isTaggedBomb = False # tracks whether peni web bomb is attached
    bombTimer = 0 # tracks time until the web bomb explodes
    symbioteTimer = 0 # tracks remaining duration that symbiote can stay active
    hasDoubleJump = True # tracks whether double jump overhead can be used (doesn't force overhead)
    hasSwingOverhead = "unknown" # tracks whether swing overhead can be used (does force overhead)

    # charges available for relevant actions
    charges = { 
        "t" : 5,
        "s" : 3,
        "g" : 1,
        "u" : 2,
        "S" : 1,
        "B" : 1
    }

    # time until respective charge is replenished
    rechargeTimers = { 
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "B" : 0
    }

    # time until charges can be used, regardless of availability
    cooldownTimers = { 
        "t" : 0,
        "s" : 0,
        "u" : 0
    }

    # time until current animation can be cancelled into each class of action
    animationCancelTimes = { 
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "B" : 0
    }

    # creates state and applies actions in the sequence
    def __init__(self, sequence):
        self.inferInitialState(sequence)
        for action in sequence:
            self.applyAction(action)

    # infers initial conditions to avoid raising errors for sensible inputs
    def inferInitialState(self, sequence):
        pass

    # TO DO: increments timers as time passes during combo
    def advanceTime(self, frames):
        pass
        
    # TO DO: modifies state according to the next action taken
    def applyAction(self, action):
        pass