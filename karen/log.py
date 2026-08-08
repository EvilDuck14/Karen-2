class LogEntry:
    frame: int = 0
    details: str = ""
    flags: list[str] = []

    def __init__(self, frame: int, details: str, flags : list[str] = []):
        self.frame = frame
        self.details = details
        self.flags = flags

        for flag in flags:
            if not flag in EVENT_TYPES:
                raise(f"event type {flag} not recognised")

EVENT_TYPES = {
    "action started"
    "damage",
    "timer expired",
    "cooldown",
    "waiting",

    "minor warning",
    "major warning",
    "overhead warning",
    "sequence warning"
}