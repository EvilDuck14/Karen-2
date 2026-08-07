from karen.actionData import *
from typing import Literal, Callable

class LogEntry:
    frame: int = 0
    details: str = ""
    flags: list[str] = []

class State:
    sequence: list[str] = [] # list of actions that have been applied to the state
    log: list[LogEntry] = [] # stores more information for debugging / advanced users

    timeElapsed: int = 0 # time from start of combo until current point in calculation
    sequenceTime: int = 0 # time from start of combo until final queued hit
    firstDamageTime: int | Literal["unknown"] = "unknown" # time that first tick of damage registers
    damageDealt: int = 0 # cumulative damage counter

    meleeSequenceStep: Literal["punch 1", "punch 2", "kick", "unknown", "not punch 1"] = "unknown" # tracks melee sequence)
    meleeSequenceTimer: int = 0 # timer for punch/kick tracking
    isTagged: bool = False # tracks whether regular tracer tag is applied
    tagDelay: int = 0 # tracks time until tracer tag will be applied
    tagTimer: int = 0 # tracks time until tracer tag expires
    isTaggedBomb: bool = False # tracks whether peni web bomb is attached
    bombTimer: int = 0 # tracks time until the web bomb explodes
    symbioteTimer: int = 0 # tracks remaining duration that symbiote can stay active
    hasDoubleJump: bool = True # tracks whether double jump overhead can be used (doesn't force overhead)
    hasSwingOverhead: bool | Literal["unknown"] = "unknown" # tracks whether swing overhead can be used (does force overhead)

    # charges available for relevant actions
    charges: dict[str, int] = { 
        "t" : MAX_CHARGES["t"],
        "s" : MAX_CHARGES["s"],
        "g" : MAX_CHARGES["g"],
        "u" : MAX_CHARGES["u"],
        "S" : MAX_CHARGES["S"],
        "B" : MAX_CHARGES["B"]
    }

    # time until respective charge is replenished
    rechargeTimers: dict[str, int] = { 
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "B" : 0
    }

    # time until charges can be used, regardless of availability
    cooldownTimers: dict[str, int] = { 
        "t" : 0,
        "s" : 0,
        "u" : 0
    }

    # time until current animation can be cancelled into each class of action
    animationCancelTimes: dict[str, int] = { 
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "B" : 0
    }

    # static variable holding functions which append actions to a state
    ApplyAction: dict[str, Callable[[State]], None] = {}

    # creates state and applies actions in the sequence
    def __init__(self, sequence: list[str]):
        for action in sequence:
            self.applyAction(action)

    # reduces individual timers and returns a flag for whether they hit zero
    @staticmethod
    def reduceTimer(timer: int, frames: int) -> tuple[int, bool]:
        if timer == 0:
            return timer, False
        timer = max(timer - frames, 0)
        return timer, timer == 0

    # increments timers as time passes during combo
    def advanceTime(self, frames: int) -> None:
        self.timeElapsed += frames

        # melee sequence
        self.meleeSequenceTimer, flagComplete = State.reduceTimer(self.meleeSequenceTimer, frames)
        if flagComplete:
            self.meleeSequenceStep = "punch 1"

        # tracer tag timer
        self.tagTimer, flagComplete = State.reduceTimer(self.tagTimer, frames)
        if flagComplete:
            self.isTagged = False

        # peni web bomb timer
        if frames > self.bombTimer > 0:
            pass # TO DO: handle explosion/tracer refund
        self.bombTimer, flagComplete = State.reduceTimer(self.bombTimer, frames)

        # symbiote damage over time
        self.symbioteTimer, flagComplete = State.reduceTimer(self.symbioteTimer, frames)
        # TO DO: handle symbiote damage over time (1 damage every 6 frames, keeping time aligned)

        # recharging charges
        for charge in self.rechargeTimers.keys():
            self.rechargeTimers[charge], flagComplete = State.reduceTimer(self.rechargeTimers[charge], frames)
            if flagComplete:
                self.charges = min(self.charges + 1, MAX_CHARGES[charge])

                # start recharging next charge if not full
                if self.charges[charge] < MAX_CHARGES[charge]:
                    self.rechargeTimers[charge] = RECHARGE_TIMES[charge]

        # cooldowns
        for charge in self.cooldownTimers.keys():
            self.cooldownTimers[charge], flagComplete = State.reduceTimer(self.cooldownTimers[charge], frames) 
        
    # TO DO: modifies state according to the next action taken
    def applyAction(self, action: str) -> None:
        pass