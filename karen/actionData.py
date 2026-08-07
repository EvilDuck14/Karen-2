ACTION_NAMES = {
    "p" : "Punch", 
    "k" : "Kick", 
    "o" : "Overhead Slam", 
    "t" : "Tracer", 
    "w" : "Swing Whiff", 
    "a" : "Auto Swing", 
    "g" : "Get Over Here", 
    "G" : "Get Over Here (Targetting)", 
    "u" : "Uppercut",
    "S" : "Symbiote",
    "C" : "Clap",
    "B" : "Web Bomb",
    "E" : "Explosion",
}

MAX_CHARGES = {
    "t" : 5,
    "s" : 3,
    "g" : 1,
    "u" : 2,
    "S" : 1,
    "B" : 1
}

RECHARGE_TIMES = {
    "t" : 2 * 60,
    "s" : 6 * 60,
    "g" : 8 * 60,
    "u" : 6 * 60,
    "S" : 15 * 60,
    "B" : 15 * 60
}

COOLDOWN_TIMES = {
    "t" : 30,
    "s" : 0, # TO DO: measure
    "u" : 2 * 60
}