from karen.actions.actionData import *
from typing import Literal, Callable
from karen.log import LogEntry

class State:
    log: list[LogEntry] # stores more information for debugging / advanced users
    actionLog: list[LogEntry] # stores actions and the times at which they occured, used to insert explosion timing into sequence readout

    timeElapsed: int # time from start of combo until current point in calculation
    lastDamageTime: int # time from start of combo until final queued hit
    firstDamageTime: int | Literal["unknown"] # time that first tick of damage registers
    damageDealt: int # cumulative damage counter
    bombDamageTime: int # tracks whether to remove the bomb damage from the dps calculation

    meleeSequenceStep: Literal["punch 1", "punch 2", "kick", "unknown", "not punch 1"] # tracks melee sequence)
    meleeSequenceTimer: int # timer for punch/kick tracking
    tagDelay: int # tracks time until tracer tag will be applied
    tagTimer: int # tracks time until tracer tag expires
    swingIsWhiff: bool # tracks whether the last used swing was a whiff to avoid consuming a swing charge
    GOHTAvaiableTimer: int # helps tracking availability of GOHT throughout overlapping tracers
    isTaggedBomb: bool = False # tracks whether peni web bomb is attached
    bombTimer: int # tracks time until the web bomb explodes
    awaitingExplosion: bool # tells actions that proc tracer to wait for the bomb to explode
    explosionWaitTimer: int # tracks how long the combo waited for the explosion, used to calculate time to wait if the combo starts with a clap
    lastTagProcPreExplosion: int # tracks the last frame that a tag was proced before the explosion was registered, used to calculate pre combo wait time range
    teatherTimer: int # tracks remaining duration that symbiote teather can stay active
    hasDoubleJump: bool # tracks whether double jump overhead can be used (doesn't force overhead)
    hasSwingOverhead: bool | Literal["unknown"] # tracks whether swing overhead can be used (does force overhead)

    charges: dict[str, int] # charges available for relevant actions
    activeTimers: dict[str, int] # time until action ends if not cancelled, cooldown is only taken afterwards
    rechargeTimers: dict[str, int] # time until respective charge is replenished
    fireRateTimers: dict[str, int] # time until charges can be used, regardless of availability   
    animationCancelTimes: dict[str, int] # time until current animation can be cancelled into each class of action

    # static variable holding functions which append actions to a state
    ApplyAction: dict[str, Callable[[State]], None] = {}

    # creates state and applies actions in the sequence
    def __init__(self, sequence: list[str]):
        self.log = []
        self.actionLog = []
        self.timeElapsed = 0 
        self.lastDamageTime = 0 
        self.firstDamageTime = "unknown"
        self.damageDealt = 0
        self.bombDamageTime = "unknown"
        self.meleeSequenceStep = "unknown" 
        self.meleeSequenceTimer = 0 
        self.tagDelay = 0 
        self.tagTimer = 0
        self.swingIsWhiff = False
        self.GOHTAvaiableTimer = 0
        self.isTaggedBomb = False 
        self.bombTimer = 0 
        self.awaitingExplosion = False
        self.explosionWaitTimer = 0
        self.lastTagProcPreExplosion = 0
        self.teatherTimer = 0 
        self.hasDoubleJump = True
        self.hasSwingOverhead = "unknown"

        self.charges = { 
            "t" : MAX_CHARGES["t"],
            "s" : MAX_CHARGES["s"],
            "g" : MAX_CHARGES["g"],
            "u" : MAX_CHARGES["u"],
            "S" : MAX_CHARGES["S"],
            "B" : MAX_CHARGES["B"]
        }
    
        self.activeTimers = {
            "s" : 0,
            "g" : 0,
            "u" : 0,
            "S" : 0
        }
    
        self.rechargeTimers = { 
            "t" : 0,
            "s" : 0,
            "g" : 0,
            "u" : 0,
            "S" : 0,
            "B" : 0
        }
    
        self.fireRateTimers = { 
            "t" : 0,
            "s" : 0,
            "u" : 0,
            "C" : 0
        }

        self.animationCancelTimes = { 
            "p" : 0,
            "o" : 0,
            "t" : 0,
            "s" : 0,
            "g" : 0,
            "u" : 0,
            "S" : 0,
            "C" : 0,
            "B" : 0
        }

        for action in sequence:
            self.applyAction(action)

        if self.awaitingExplosion and (self.bombTimer > 0):
            self.explosionWaitTimer = self.bombTimer
            self.advanceTime(self.bombTimer)

        if (self.activeTimers["S"] > 0) and (self.teatherTimer > SYMBIOTE_TEATHER_HIT_INTERVAL):
            self.pushLog("awaiting symbiote teather damage", ["cooldown"])
            self.advanceTime(self.teatherTimer - SYMBIOTE_TEATHER_HIT_INTERVAL)

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
                self.pushLog(f"{ACTION_NAMES["B"]} expired without firing", ["timer expired"], frameOffset=self.bombTimer)
                self.charges["t"] = MAX_CHARGES["t"]
                self.rechargeTimers["t"] = 0
        self.bombTimer = max(self.bombTimer - frames, 0)

        # tracer tag timer
        if frames >= self.tagTimer > 0:
            self.pushLog("tag expired", ["timer expired"], frameOffset=self.tagTimer)
        self.tagTimer = max(self.tagTimer - frames, 0)

        # GOHT availability timer
        if frames >= self.GOHTAvaiableTimer > 0:
            self.pushLog(f"{ACTION_NAMES["G"]} availability expired", ["timer expired"], frameOffset=self.GOHTAvaiableTimer)
        self.GOHTAvaiableTimer = max(self.GOHTAvaiableTimer - frames, 0)
        if self.tagTimer > self.GOHTAvaiableTimer and self.tagTimer <= TAG_DURATION - TAG_GOHT_DELAY:
            self.GOHTAvaiableTimer = self.tagTimer
            self.pushLog(f"{ACTION_NAMES["G"]} registered available target", ["cooldown"], frameOffset=(frames + self.tagTimer - (TAG_DURATION - TAG_GOHT_DELAY)))

        # symbiote teather damage over time
        framesToRemove: int = frames
        while (self.teatherTimer > 0) and framesToRemove > 0:
            batchFrames: int = min(framesToRemove, (SYMBIOTE_TEATHER_HIT_INTERVAL if self.teatherTimer % SYMBIOTE_TEATHER_HIT_INTERVAL == 0 else self.teatherTimer % SYMBIOTE_TEATHER_HIT_INTERVAL))
            self.teatherTimer -= batchFrames
            framesToRemove -= batchFrames
            if (self.teatherTimer % SYMBIOTE_TEATHER_HIT_INTERVAL == 0) and SYMBIOTE_TEATHER_DURATION >= self.teatherTimer > 0:
                self.dealDamage("T", frameOffset=(frames - framesToRemove))

        # active abilitiy timers
        for charge in self.activeTimers.keys():
            if frames >= self.activeTimers[charge] > 0:
                self.pushLog(f"active {ACTION_NAMES[charge]} ended", ["cooldown"], frameOffset=self.activeTimers[charge])

                # don't consume charge for swing whiff
                if (charge != "s") or (not self.swingIsWhiff):
                    self.charges[charge] -= 1
                    self.pushLog(f"consumed {ACTION_NAMES[charge]} charge", ["cooldown"], frameOffset=self.activeTimers[charge])

                # starts recharging
                if self.rechargeTimers[charge] == 0:
                    self.rechargeTimers[charge] = RECHARGE_TIMES[charge] + self.activeTimers[charge]
                elif self.rechargeTimers[charge] <= frames:
                    self.rechargeTimers[charge] += frames - self.activeTimers[charge]

                # triggers cooldown (fire rate limit)
                if charge in self.fireRateTimers.keys():
                    self.fireRateTimers[charge] = COOLDOWN_TIMES[charge] - self.activeTimers[charge]

                # swing overhead reward
                if charge == "s":
                    self.pushLog("awarded swing overhead", ["cooldown"], frameOffset=self.activeTimers[charge])
                    self.hasSwingOverhead = True

            self.activeTimers[charge] = max(self.activeTimers[charge] - frames, 0)

        # recharging charges (handles long wait times that last multiple charges)
        for charge in self.rechargeTimers.keys():
            while (frames >= self.rechargeTimers[charge] > 0) and (self.charges[charge] < MAX_CHARGES[charge]):
                self.charges[charge] += 1
                self.pushLog(f"regained {ACTION_NAMES[charge]} charge", ["cooldown"], frameOffset=self.rechargeTimers[charge])
                if self.charges[charge] < MAX_CHARGES[charge]:
                    self.rechargeTimers[charge] += RECHARGE_TIMES[charge]
            self.rechargeTimers[charge] = max(self.rechargeTimers[charge] - frames, 0)               

        # cooldowns / fire rate timers
        for charge in self.fireRateTimers.keys():
            if (frames > self.fireRateTimers[charge] > 0) and (charge != "C"):
                self.pushLog(f"{ACTION_NAMES[charge]} came off cooldown (fire rate limit)", ["cooldown"], frameOffset=self.fireRateTimers[charge])
            self.fireRateTimers[charge] = max(self.fireRateTimers[charge] - frames, 0)

        # animation cancel tracking
        for action in self.animationCancelTimes.keys():
            self.animationCancelTimes[action] = max(self.animationCancelTimes[action] - frames, 0)
        
        self.timeElapsed += frames
        
    # modifies state according to the next action taken
    def applyAction(self, action: str) -> None:

        # wait logic
        if action[0] == "[":

            # wait a number of frames
            if action[-2] == "f":
                waitTime: int = int(action[1:-2])
                self.pushLog(f"waiting {waitTime} frames", ["waiting"])
                self.pushActionLog(f"[{waitTime}f]")
                self.advanceTime(waitTime)

            # wait a number of seconds
            if action[-2] == "s":
                waitTime: int = round(60 * float(action[1:-2]))
                self.pushLog(f"waiting {round(waitTime / 60, 2)} seconds", ["waiting"])
                self.pushActionLog(f"[{waitTime}f]")
                self.advanceTime(waitTime)

            # wait for a number of teather hits
            if action[-2] == "T":
                waitTime: int = 0
                if int(action[1:-2]) > 0:
                    waitTime = max(waitTime, self.teatherTimer - SYMBIOTE_TEATHER_DURATION)
                    waitTime = max(waitTime, (SYMBIOTE_TEATHER_HIT_INTERVAL if (self.teatherTimer % SYMBIOTE_TEATHER_HIT_INTERVAL == 0) else self.teatherTimer % SYMBIOTE_TEATHER_HIT_INTERVAL))
                    waitTime += (int(action[1:-2]) - 1) * SYMBIOTE_TEATHER_HIT_INTERVAL
                    waitTime = min(waitTime, self.teatherTimer - SYMBIOTE_TEATHER_HIT_INTERVAL)
                self.pushLog(f"awaiting {max(0, min(10, int(action[1:-2])))} teather ticks", ["waiting"])
                self.pushActionLog(f"[{waitTime}f]")
                self.advanceTime(waitTime)

            # wait for the bomb to reach a certain remaining number of frames
            if action[-2] == "B":
                waitTime: int = self.bombTimer - int(action[1:-2])
                self.pushLog(f"waiting for bomb timer to reach {int(action[1:-2])} frames", ["waiting"])
                self.pushActionLog(f"[{waitTime}f]")
                self.advanceTime(waitTime)

            # wait amount given as a range (cannot be entered by user)
            if action[-2] == "R":
                waitTime: int = int(action[1:action.find("-")])
                self.pushLog(f"waiting {waitTime} frames", ["waiting"])
                self.pushActionLog(f"[{action[1:-2]}f]")
                self.advanceTime(waitTime)

        else:
            State.ApplyAction[action](self)

    # handles waiting for ability availability
    def awaitCharge(self, charge: str, frameOffset: int = 0) -> None:

        # await active usage
        if (charge in self.activeTimers.keys()) and (self.activeTimers[charge] > frameOffset):
            self.pushLog(f"has to wait {self.activeTimers[charge] - (frameOffset if (MAX_CHARGES[charge] > 1) else 0)} frames for overlapping {ACTION_NAMES[charge]} to end", ["waiting", "cooldown"])
            self.advanceTime(self.activeTimers[charge] - (frameOffset if (MAX_CHARGES[charge] > 1) else 0))
    
        # await charge
        if self.charges[charge] == 0:
            self.pushLog(f"has to wait {self.rechargeTimers[charge] - frameOffset} frames for {ACTION_NAMES[charge]} recharge", ["waiting", "cooldown"])
            self.advanceTime(self.rechargeTimers[charge] - frameOffset)
    
        # await fire rate
        if (charge in self.fireRateTimers.keys()) and (self.fireRateTimers[charge] > 0):
            self.pushLog(f"has to wait {self.fireRateTimers[charge] - frameOffset} frames for {ACTION_NAMES[charge]} fire rate", ["waiting", "cooldown"])
            self.advanceTime(self.fireRateTimers[charge] - frameOffset)

    # handles adding damage in a specified amount of time, properly tracking timers
    def dealDamage(self, source: str, frameOffset: int = 0) -> None:
        self.damageDealt += ACTION_DAMAGE[source]
        self.pushLog(f"{ACTION_NAMES[source]} dealt {ACTION_DAMAGE[source]} damage", ["damage"], frameOffset)

        # tracking first damage time
        if self.firstDamageTime == "unknown" or self.firstDamageTime > self.timeElapsed + frameOffset:
            if source != "B":
                self.firstDamageTime = self.timeElapsed + frameOffset
            elif self.bombDamageTime == "unknown":
                self.bombDamageTime = self.timeElapsed + frameOffset

        # tracking last damage time
        self.lastDamageTime = max(self.lastDamageTime, self.timeElapsed + frameOffset)

        # tracer tag proc
        if source in PROCS_TAG:
            self.procTag(frameOffset=frameOffset)

        # tracer tag application
        if source in APPLIES_TAG:
            self.tagTimer = TAG_DURATION + frameOffset
            self.pushLog("applied tag", ["cooldown"], frameOffset)

        # tracking explosion time
        if source == "E":
            self.pushActionLog("E", frameOffset=frameOffset)
            self.awaitingExplosion = False

    # tracer tag proc
    def procTag(self, frameOffset: int = 0):
    
        # handles web bomb exploding during frame offset
        if (frameOffset >= self.bombTimer > 0) and self.isTaggedBomb:
            self.dealDamage("E", frameOffset=self.bombTimer)
            self.isTaggedBomb = False

        # regular tracer proc
        if frameOffset < self.tagTimer:
            self.damageDealt += TAG_PROC_DAMAGE
            self.tagTimer = min(self.tagTimer, frameOffset)
            self.GOHTAvaiableTimer = min(self.GOHTAvaiableTimer, frameOffset)
            if TAG_DURATION - TAG_GOHT_DELAY + frameOffset >= self.tagTimer > self.GOHTAvaiableTimer:
                self.GOHTAvaiableTimer = self.tagTimer
            self.pushLog(f"proced tag, dealing {TAG_PROC_DAMAGE} damage", ["damage"], frameOffset)

        # tracking explosion window for calculating pre-wait time
        if ((self.bombTimer == 0) or (frameOffset < self.bombTimer)) and not ("E" in [entry.details for entry in self.actionLog if entry.frame <= self.timeElapsed + frameOffset]):
            self.lastTagProcPreExplosion = max(self.timeElapsed, self.timeElapsed + frameOffset)

    # reduces charge and sets relevant timers
    def endActive(self, charge: str):
        if self.activeTimers[charge] == 0:
            return
        self.pushLog(f"active {ACTION_NAMES[charge]} ended", ["cooldown"])

        # don't consume charge for swing whiff
        if (charge != "s") or (not self.swingIsWhiff):
            self.charges[charge] -= 1
            self.pushLog(f"consumed {ACTION_NAMES[charge]} charge", ["cooldown"])

        if self.rechargeTimers[charge] == 0:
            self.rechargeTimers[charge] = RECHARGE_TIMES[charge]
        if charge in self.fireRateTimers.keys():
            self.fireRateTimers[charge] = COOLDOWN_TIMES[charge]
        if charge in self.activeTimers.keys():
            self.activeTimers[charge] = 0

        # awarding swing overhead
        if charge == "s":
            self.hasSwingOverhead = True
            self.pushLog("awarded swing overhead", ["cooldown"])

        # canceling symbiote teather
        if charge == "S":
            self.teatherTimer = 0

    # major warning if ability charge is used currently but isn't available
    def warnIfNotReady(self, charge: str):
        if (charge in self.activeTimers.keys()) and (self.activeTimers[charge] > 0) and (charge != "S"):
            self.pushLog(f"used {ACTION_NAMES[charge]} while charge still in use", ["dev warning"])
        if (charge in self.charges.keys()) and (self.charges[charge] == 0):
            self.pushLog(f"used {ACTION_NAMES[charge]} without required charge", ["dev warning"])
        if (charge in self.fireRateTimers.keys()) and (self.fireRateTimers[charge] > 0):
            self.pushLog(f"used {ACTION_NAMES[charge]} faster than fire rate limit allows", ["dev warning"])

    def pushLog(self, details: str, flags: list[str] = [], frameOffset: int = 0):
        self.log.append(LogEntry(self.timeElapsed + frameOffset, details, flags))

    def pushActionLog(self, action: str, frameOffset: int = 0):
        self.actionLog.append(LogEntry(self.timeElapsed + frameOffset, action))

    # prints all info to console
    def printConsole(self):

        # print logs
        self.log.sort()
        for entry in self.log:
            entry.printConsole()

        # print state information
        print(
              f"\nDamage: {self.damageDealt}" +
              f"\nTime: {round(self.lastDamageTime / 60, 2)}s" +
              f"\nTime From First Hit: {round((0 if self.firstDamageTime == "unknown" else self.lastDamageTime - self.firstDamageTime) / 60, 2)}s"
        )

    def getSequence(self) -> list[str]:

        # move web bomb explosions to the correct point in the sequence
        explosionEntries: list[LogEntry] = []
        otherEntries: list[LogEntry] = []

        # separate explosions from other actions
        for entry in self.actionLog:
            if entry.details == "E":
                explosionEntries.append(entry)
            else:
                otherEntries.append(entry)

        # insert explosions in the correct positions
        for explosionEntry in explosionEntries:
            position: int = len(otherEntries)
            for index, entry in enumerate(otherEntries):
                if entry.frame >= explosionEntry.frame:
                    position = index
                    break

            # dont insert explosion if it's already accounted for in an explosion weave movestack
            if (position == 0) or not ("E" in otherEntries[position - 1].details):
                otherEntries = otherEntries[:position] + [explosionEntry] + otherEntries[position:]

        # return list of actions
        return [entry.details for entry in otherEntries]

    def getComboDetails(self) -> dict[str, str | int]:
        details: dict[str, str | int] = {}
        sequence: list[str] = self.getSequence()

        details["damage"] = self.damageDealt
        details["time frames"] = self.lastDamageTime
        details["time seconds"] = round(details["time frames"] / 60, 2)

        tfd: int = 0 if self.firstDamageTime == "unknown" else self.lastDamageTime - self.firstDamageTime
        details["time from damage frames"] = tfd
        details["time from damage seconds"] = round(tfd / 60, 2)

        dpsNumerator: int = 60 * (self.damageDealt - (ACTION_DAMAGE["B"] if ((self.bombDamageTime != "unknown") and (self.bombDamageTime < self.firstDamageTime)) else 0))
        details["dps"] = "NaN" if tfd == 0 else round(dpsNumerator / tfd, 2)

        details["sequence shorthand"] = "".join(sequence)

        actionNames: list[str] = []
        for action in sequence:
            if action[0] == "[":
                actionNames.append(f"Wait {action}")
            else:
                actionNames.append(ACTION_NAMES[action])
        details["sequence string"] = " > ".join(actionNames)

        return details

    def getWarnings(self) -> list[str]:
        warningList = []
        self.log.sort()
        for entry in self.log:
            for flag in entry.flags:
                if flag in ["dev warning", "major warning", "sequence warning"]:
                    warningList.append(entry.details)
                    break
        return warningList