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

    # Early Cancels
    "p-" : "Punch (Burn)",
    "k-" : "Kick (Burn)",
    "o-" : "Overhead (Burn)",
    "a-" : "No Stick",

    # Movestacks
    "G+u" : "FFAmestack",
    "p+G" : "Punch Saporen",
    "k+G" : "Kick Saporen",
    "o+G" : "Overhead Saporen",
    "p+G+u" : "Punch Saporen FFAmestack",
    "k+G+u" : "Kick Saporen FFAmestack",
    "o+G+u" : "Overhead Saporen FFAmestack",
    "u+w+G" : "Space Jam",
    "u+a+G" : "Space Jam (Auto Swing)",
    "p+t" : "Punch Reverse Trigger",
    "k+t" : "Kick Reverse Trigger",
    "p+o" : "Unique Punch Overhead Stack",
    "k+o" : "Unique Kick Overhaed Stack",
    "g+B" : "GOH Bomb Stack",
    "G+B" : "GOHT Bomb Stack"
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

ACTION_DAMAGE_TIME = {
    "p" : 14,
    "k" : 27,
    "o" : 36,
    "t" : 12,
    "g" : 17,
    "G" : 35,
    "u" : 23,
    "S" : 7,
    "B" : 12,
    "E" : 0
}

MELEE_SEQUENCE_WINDOW = 90

TAG_PROC_DAMAGE = 45
TAG_DURATION = 3 * 60
TAG_GOHT_DELAY = 3
PROCS_TAG = [ "p", "k", "o", "u" ]
APPLIES_TAG = [ "t", "E" ]

WEB_BOMB_DURATION = (2 * 60) + 5
WEB_BOMB_TAG_DURATION = 15

GOH_HIT_DISPLACE_DELAY = 7

# TO DO: figure out symbiote timing
SYMBIOTE_STARTUP_TIME = 21 # symbiote duration past one second
SYMBIOTE_ACTIVE_DURATION = 1 * 60
SYMBIOTE_TEATHER_HIT_INTERVAL = 6

SAPOREN_PRE_HIT_TIME = 5
RT_PRE_HIT_TIME = ACTION_DAMAGE_TIME["t"]

MAX_CHARGES = {
    "t" : 5,
    "s" : 3,
    "g" : 1,
    "u" : 2,
    "S" : 1,
    "B" : 1
}

# when an action is in use, the associated recharge/cooldown doesn't start its timer until the action ends
ACTIVE_TIMES = {
    "w" : 30,
    "a" : 1,
    "g" : 58,
    "G" : 60,
    "u" : 50,
    "S" : 81
}

RECHARGE_TIMES = {
    "t" : 2 * 60,
    "s" : 6 * 60,
    "g" : 8 * 60,
    "u" : 6 * 60,
    "S" : 15 * 60,
    "B" : 15 * 60
}

EARLY_CANCELS_NOT_ENABLED_BY = {
    "p" : [ "p", "k" ],
    "k" : [ "p", "k" ],
    "o" : [ "p", "k", "o" ],
    "a" : []
}

ANIMATION_CANCEL_TIMES = {
    "p" : {
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

    "k" : {
        "p" : 49,
        "o" : 23,
        "t" : 23,
        "s" : 23,
        "g" : 23,
        "u" : 23,
        "S" : 23,
        "C" : 23,
        "B" : 23
    },

    "o" : {
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

    "t" : {
        "p" : 30,
        "o" : 30,
        "t" : 30,
        "s" : 6,
        "g" : 6,
        "u" : 6,
        "S" : 6,
        "C" : 6,
        "B" : 1
    },

    "w" : {
        "p" : 27,
        "o" : 27,
        "t" : 10, 
        "s" : 29,
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

    "g" : {
        "p" : 47,
        "o" : 47,
        "t" : 47,
        "s" : 15,
        "g" : 15,
        "u" : 47,
        "S" : 14,
        "C" : 14,
        "B" : 1
    },

    "G" : {
        "p" : 61,
        "o" : 61,
        "t" : 61,
        "s" : 30,
        "g" : 30,
        "u" : 30,
        "S" : 30,
        "C" : 20,
        "B" : 1
    },

    "u" : {
        "p" : 48,
        "o" : 48,
        "t" : 48,
        "s" : 20,
        "g" : 51,
        "u" : 20,
        "S" : 19,
        "C" : 51,
        "B" : 51
    },

    "S" : {
        "p" : 31,
        "o" : 31,
        "t" : 31,
        "s" : 1,
        "g" : 31,
        "u" : 31,
        "S" : 60,
        "C" : 31,
        "B" : 31
    },

    "C" : {
        "p" : 23,
        "o" : 23,
        "t" : 1,
        "s" : 1,
        "g" : 1,
        "u" : 1,
        "S" : 1,
        "C" : 1,
        "B" : 3
    },

    "B" : {
        "p" : 20,
        "o" : 20,
        "t" : 6,
        "s" : 6,
        "g" : 1,
        "u" : 1,
        "S" : 1,
        "C" : 1,
        "B" : 1
    }
}

COOLDOWN_TIMES = {
    "t" : 30,
    "s" : 19, 
    "u" : 2 * 60,
    "C" : ANIMATION_CANCEL_TIMES["C"]["p"]
}