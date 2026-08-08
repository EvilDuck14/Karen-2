ACTION_NAMES = {
    "p" : "Punch", 
    "k" : "Kick", 
    "o" : "Overhead Slam", 
    "t" : "Tracer", 
    "s" : "Swing", # only used for ability charges
    "w" : "Swing Whiff", 
    "a" : "Auto Swing", 
    "g" : "Get Over Here", 
    "G" : "Get Over Here (Targetting)", 
    "u" : "Uppercut",
    "S" : "Symbiote",
    "V" : "Symbiote (Upgraded)",
    "T" : "Symbiote Teather", # only used for logging damage source
    "C" : "Clap",
    "B" : "Web Bomb",
    "E" : "Web Bomb Explosion",
}

ACTION_DAMAGE = {
    "p" : 25,
    "k" : 40,
    "o" : 55,
    "t" : 30,
    "g" : 25,
    "G" : 55,
    "u" : 70,
    "S" : 25,
    "T" : 1,
    "B" : 1,
    "E" : 50
}

ACTION_DAMAGE_TIME = { # TO DO: measure
    "p" : 0,
    "k" : 0,
    "o" : 0,
    "t" : 0,
    "g" : 0,
    "G" : 0,
    "u" : 0,
    "S" : 0,
    "B" : 0,
    "E" : 0
}

MELEE_SEQUENCE_WINDOW = 3 * 60 # TO DO: measure

TAG_PROC_DAMAGE = 45
TAG_DURATION = 3 * 60
TAG_GOHT_DELAY = 3
PROCS_TAG = [ "p", "k", "o", "u" ]
APPLIES_TAG = [ "t", "E" ]

WEB_BOMB_DURATION = 2 * 60 # TO DO: check
WEB_BOMB_TAG_DURATION = 0 # minum time that the bomb can explode in after landing 
# TO DO: check ^

SYMBIOTE_MAX_DURATION = 1 * 60
SYMBIOTE_TEATHER_HIT_INTERVAL = 6

MAX_CHARGES = {
    "t" : 5,
    "s" : 3,
    "g" : 1,
    "u" : 2,
    "S" : 1,
    "B" : 1
}

# when an action is in use, the associated recharge/cooldown doesn't start its timer until the action ends
ACTIVE_TIMES = { # TO DO: measure
    "w" : 0,
    "a" : 0,
    "g" : 0,
    "G" : 0,
    "u" : 0,
    "S" : 0,
    "C" : 0,
    "B" : 0
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

ANIMATION_CANCEL_TIMES = { # TO DO: measure
    "p" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "k" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "o" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "t" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "w" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "a" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "g" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "G" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "u" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "S" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "C" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "B" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "E" : {
        "p" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

}