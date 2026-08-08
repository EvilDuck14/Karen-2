from karen.actionData import *
from typing import Literal, Callable
from karen.log import LogEntry

class State:
    sequence: list[str] = [] # list of actions that have been applied to the state
    log: list[LogEntry] = [] # stores more information for debugging / advanced users

    timeElapsed: int = 0 # time from start of combo until current point in calculation
    lastDamageTime: int = 0 # time from start of combo until final queued hit
    firstDamageTime: int | Literal["unknown"] = "unknown" # time that first tick of damage registers
    damageDealt: int = 0 # cumulative damage counter

    meleeSequenceStep: Literal["punch 1", "punch 2", "kick", "unknown", "not punch 1"] = "unknown" # tracks melee sequence)
    meleeSequenceTimer: int = 0 # timer for punch/kick tracking
    tagDelay: int = 0 # tracks time until tracer tag will be applied
    tagTimer: int = 0 # tracks time until tracer tag expires
    GOHTAvaiableTimer: int = 0 # helps tracking availability of GOHT throughout overlapping tracers
    isTaggedBomb: bool = False # tracks whether peni web bomb is attached
    bombTimer: int = 0 # tracks time until the web bomb explodes
    teatherTimer: int = 0 # tracks remaining duration that symbiote teather can stay active
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

    # time until action ends if not cancelled, cooldown is only taken afterwards
    activeTimers: dict[str, int] = {
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0
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
    fireRateTimers: dict[str, int] = { 
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
        "C" : 0,
        "B" : 0
    }

    # static variable holding functions which append actions to a state
    ApplyAction: dict[str, Callable[[State]], None] = {}

    # creates state and applies actions in the sequence
    def __init__(self, sequence: list[str]):
        for action in sequence:
            self.applyAction(action)

    # increments timers as time passes during combo
    def advanceTime(self, frames: int) -> None:
        if frames == 0:
            return

        # melee sequence
        if frames >= self.meleeSequenceTimer > 0:
            self.meleeSequenceStep = "punch 1"
            self.pushLog("melee sequence expired", ["timer expired"], frameOffset=self.meleeSequenceTimer)
        self.meleeSequenceTimer = max(self.meleeSequenceTimer - frames, 0)

        # peni web bomb timer
        if frames >= self.bombTimer > 0:
            if self.isTaggedBomb:
                self.dealDamage("E", frameOffset=self.bombTimer)
                self.isTaggedBomb = False
            else:
                self.pushLog("web bomb expired without firing", ["timer expired"], frameOffset=self.bombTimer)
                self.charges["t"] = MAX_CHARGES["t"]
                self.rechargeTimers["t"] = 0
        self.bombTimer = max(self.bombTimer - frames, 0)

        # tracer tag timer
        if frames >= self.tagTimer > 0:
            self.pushLog("tracer tag expired", ["timer expired"], frameOffset=self.tagTimer)
        self.tagTimer = max(self.tagTimer - frames, 0)

        # GOHT availability timer
        if frames >= self.GOHTAvaiableTimer > 0:
            self.pushLog("GOHT availability expired", ["timer expired"], frameOffset=self.GOHTAvaiableTimer)
        if self.tagTimer > self.GOHTAvaiableTimer and self.tagTimer <= TAG_DURATION - TAG_GOHT_DELAY:
            self.GOHTAvaiableTimer - self.tagTimer
            self.pushLog("GOHT registered available target", ["cooldown"], frameOffset=(self.tagTimer - (TAG_DURATION - TAG_GOHT_DELAY)))

        # symbiote teather damage over time
        if self.teatherTimer > 0:
            framesToFirstHit: int = ((self.teatherTimer - 1) % SYMBIOTE_TEATHER_HIT_INTERVAL) + 1
            teatherTicks: int = max((frames - framesToFirstHit) // SYMBIOTE_TEATHER_HIT_INTERVAL, 1 + ((self.teatherTimer - 1) // SYMBIOTE_TEATHER_HIT_INTERVAL))
            for i in range(teatherTicks):
                self.dealDamage("T", frameOffset=(framesToFirstHit + SYMBIOTE_TEATHER_HIT_INTERVAL * i))
            self.teatherTimer = max(self.teatherTimer - frames, 0)

        # active abilitiy timers
        for charge in self.activeTimers.keys():
            if frames >= self.rechargeTimers[charge] > 0:
                self.charges[charge] -= 1
                self.pushLog(f"consumed {ACTION_NAMES[charge]} charge", ["cooldown"], frameOffset=self.rechargeTimers[charge])

                # starts recharging
                if self.rechargeTimers[charge] == 0:
                    self.rechargeTimers[charge] = RECHARGE_TIMES[charge] + self.activeTimers[charge]
                elif self.rechargeTimers[charge] <= frames:
                    self.rechargeTimers[charge] += frames - self.activeTimers[charge]

                # triggers cooldown (fire rate limit)
                if charge in self.fireRateTimers.keys():
                    self.fireRateTimers[charge] = COOLDOWN_TIMES[charge] - self.rechargeTimers[charge]

                # swing overhead reward
                if charge == "s":
                    self.pushLog("awarded swing overhead", ["cooldown"], frameOffset=self.fireRateTimers[charge])
                    self.hasSwingOverhead = True

            self.activeTimers[charge] = max(self.activeTimers[charge] - frames, 0)

        # recharging charges (handles long wait times that last multiple charges)
        for charge in self.rechargeTimers.keys():
            while frames >= self.rechargeTimers[charge] > 0:
                self.charges = min(self.charges + 1, MAX_CHARGES[charge])
                self.pushLog(f"regained {ACTION_NAMES[charge]} charge", ["cooldown"], frameOffset=self.rechargeTimers[charge])
                if self.charges[charge] < MAX_CHARGES[charge]:
                    self.rechargeTimers[charge] += RECHARGE_TIMES[charge]
            self.rechargeTimers[charge] = max(self.rechargeTimers[charge] - frames, 0)               

        # cooldowns / fire rate timers
        for charge in self.fireRateTimers.keys():
            self.fireRateTimers[charge] = max(self.fireRateTimers[charge], 0)
            self.pushLog(f"{ACTION_NAMES[charge]} came off cooldown (fire rate limit)", ["cooldown"], frameOffset=self.fireRateTimers[charge])
        
        self.timeElapsed += frames
        
    # modifies state according to the next action taken
    def applyAction(self, action: str) -> None:
        State.ApplyAction[action](self)

    # handles adding damage in a specified amount of time, properly tracking timers
    def dealDamage(self, source: str, frameOffset: int = 0) -> None:
        self.damageDealt += ACTION_DAMAGE[source]
        self.pushLog(f"{ACTION_NAMES[source]} dealt {ACTION_DAMAGE[source]} damage", ["damage"], frameOffset)

        # tracking first damage time
        if self.firstDamageTime == "unknown" or self.firstDamageTime > self.timeElapsed + frameOffset:
            self.firstDamageTime = self.timeElapsed + frameOffset

        # tracking last damage time
        self.lastDamageTime = max(self.lastDamageTime, self.timeElapsed + frameOffset)

        # tracer tag proc
        if source in PROCS_TAG and self.tagTimer > 0 and frameOffset < self.tagTimer:
            self.damageDealt += TAG_PROC_DAMAGE
            self.tagTimer = 0
            self.pushLog(f"{ACTION_NAMES[source]} proced tag dealing {TAG_PROC_DAMAGE} damage", ["damage"], frameOffset)

        # tracer tag application
        if source in APPLIES_TAG:
            self.tagTimer = TAG_DURATION + frameOffset

    # reduces charge and sets relevant timers
    def endActive(self, charge: str):
        if self.activeTimers[charge] == 0:
            return
        self.charges[charge] -= 1
        if self.rechargeTimers[charge] == 0:
            self.rechargeTimers[charge] = RECHARGE_TIMES[charge]
        if charge in self.fireRateTimers.keys():
            self.fireRateTimers[charge] = COOLDOWN_TIMES[charge]
        if charge in self.activeTimers.keys():
            self.activeTimers[charge] = 0
        self.log(f"active {ACTION_NAMES[charge]} cancelled", ["cooldown"])

        # awarding swing overhead
        if charge == "s":
            self.hasSwingOverhead = True
            self.log("awarded swing overhead", ["cooldown"])

    # creates a log entry at the current time
    def pushLog(self, details: str, flags: list[str] = [], frameOffset: int = 0):
        self.log.append(LogEntry(self.timeElapsed + frameOffset, details, flags))