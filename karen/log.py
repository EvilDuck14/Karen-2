from colorama import Fore, Style

EVENT_TYPES = [
    "action started",
    "damage",
    "timer expired",
    "cooldown",
    "waiting",

    "minor warning",
    "major warning",
    "overhead warning",
    "sequence warning"
]

EVENT_COLOURS = {
    "major warning" : Fore.RED,
    "minor warning" : Fore.LIGHTRED_EX,
    "sequence warning" : Fore.LIGHTRED_EX,
    "overhead warning" : Fore.YELLOW,
    "waiting" : Fore.LIGHTYELLOW_EX,
    "timer expired" : Fore.MAGENTA,
    "cooldown" : Fore.LIGHTMAGENTA_EX,
    "action started" : Fore.CYAN,
    "damage" : Fore.LIGHTCYAN_EX
}

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

    def printConsole(self) -> None:
        colour: str = Fore.WHITE
        for flag in EVENT_COLOURS.keys():
            if flag in self.flags:
                colour = EVENT_COLOURS[flag]
                break
        print(f"{colour}[{self.frame}f] {self.details}{Style.RESET_ALL}")

    # comparison operators for sorting list by time
    def __lt__(self, other: LogEntry) -> bool:
            return self.frame < other.frame
    def __le__(self, other: LogEntry) -> bool:
            return self.frame <= other.frame
    def __gt__(self, other: LogEntry) -> bool:
            return self.frame > other.frame
    def __ge__(self, other: LogEntry) -> bool:
        return self.frame >= other.frame