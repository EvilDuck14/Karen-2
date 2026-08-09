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
    "E" : "Web Bomb Explosion"
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

ACTION_DAMAGE_TIME = { # TO DO: check
    "p" : 14,
    "k" : 24,
    "o" : 38,
    "t" : 12,
    "g" : 17,
    "G" : 37,
    "u" : 23,
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

GOH_DISPLACEMENT_TIME = 1 # TO DO: measure

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
ACTIVE_TIMES = { # TO DO: check
    "w" : 30,
    "a" : 1,
    "g" : 102,
    "G" : 61,
    "u" : 70,
    "S" : 0
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
    "s" : 19, # TO DO: check
    "u" : 2 * 60
}

ANIMATION_CANCEL_TIMES = {
    "p" : { # TO DO: check
        "p" : 23,
        "o" : 11,
        "t" : 11,
        "s" : 11,
        "g" : 11,
        "u" : 11,
        "S" : 11,
        "C" : 11,
        "B" : 11
    },

    "k" : { # TO DO: check
        "p" : 49,
        "o" : 22,
        "t" : 22,
        "s" : 22,
        "g" : 22,
        "u" : 22,
        "S" : 22,
        "C" : 22,
        "B" : 22
    },

    "o" : { # TO DO: check
        "p" : 53,
        "o" : 53,
        "t" : 33,
        "s" : 33,
        "g" : 33,
        "u" : 33,
        "S" : 33,
        "C" : 33,
        "B" : 33
    },

    "t" : { # TO DO: check
        "p" : 30,
        "o" : 30,
        "t" : 6,
        "s" : 6,
        "g" : 6,
        "u" : 6,
        "S" : 6,
        "C" : 6,
        "B" : 6
    },

    "w" : { # TO DO: check
        "p" : 27,
        "o" : 27,
        "t" : 10, 
        "s" : 1,
        "g" : 1,
        "u" : 1,
        "S" : 1,
        "C" : 1,
        "B" : 1
    },

    "a" : {
        "p" : 1,
        "o" : 1,
        "t" : 1,
        "s" : 1,
        "g" : 1,
        "u" : 1,
        "S" : 1,
        "C" : 1,
        "B" : 1
    },

    "g" : { # TO DO: CHECK
        "p" : 50,
        "o" : 50,
        "t" : 46,
        "s" : 14,
        "g" : 14,
        "u" : 47,
        "S" : 14,
        "C" : 14,
        "B" : 1
    },

    "G" : { # TO DO: check
        "p" : 61,
        "o" : 61,
        "t" : 61,
        "s" : 28,
        "g" : 28,
        "u" : 32,
        "S" : 28,
        "C" : 28,
        "B" : 1
    },

    "u" : { # TO DO: check
        "p" : 48,
        "o" : 48,
        "t" : 56,
        "s" : 19,
        "g" : 48,
        "u" : 19,
        "S" : 19,
        "C" : 0,
        "B" : 0
    },

    "S" : { # TO DO: check
        "p" : 0,
        "o" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "C" : { # TO DO: check
        "p" : 0,
        "o" : 0,
        "t" : 0,
        "s" : 0,
        "g" : 0,
        "u" : 0,
        "S" : 0,
        "C" : 0,
        "B" : 0
    },

    "B" : { # TO DO: check
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
}