from karen.actions.actionData import GOH_HIT_DISPLACE_DELAY

COMBO_ACTION_SYMBOLS = {
    "p" : ["p"],
    "k" : ["k"],
    "o" : ["o"],
    "t" : ["t"],
    "w" : ["w"],
    "s" : ["w"],
    "a" : ["a"],
    "g" : ["g"],
    "G" : ["G"],
    "u" : ["u"],
    "S" : ["S"],
    "V" : ["V"],
    "v" : ["V"],
    "C" : ["C"],
    "c" : ["C"],
    "B" : ["B"],
    "b" : ["B"],
    "E" : ["E"],
    "e" : ["E"],
    "+" : ["+"],
    "-" : ["-"],
    "f" : ["G", "+", "u"],
    "j" : ["u", "+", "w", "+", "G"]
}

COMBO_ACTION_NAMES = {
    "punch" : ["p"],
    "melee" : ["p"],
    "meleepunch" : ["p"],

    "kick" : ["k"],
    "meleekick" : ["k"],

    "overheadslam" : ["o"],
    "overhead" : ["o"],
    "over" : ["o"],
    "oh" : ["o"],
    "downslam" : ["o"],
    "slam" : ["o"],
    "meleeoverheadslam" : ["o"],
    "meleeoverhead" : ["o"],
    "meleeover" : ["o"],
    "meleeoh" : ["o"],
    "meleedownslam" : ["o"],
    "meleeslam" : ["o"],

    "tracer" : ["t"],
    "webtracer" : ["t"],
    "cluster" : ["t"],
    "webcluster" : ["t"],

    "swingwhiff" : ["w"],
    "webswingwhiff" : ["w"],
    "whiff" : ["w"],
    "webwhiff" : ["w"],
    "swing" : ["w"],
    "webswing" : ["w"],

    "autoswing" : ["a"],
    "autowebswing" : ["a"],
    "auto" : ["a"],
    "autoweb" : ["a"],
    "simpleswing" : ["a"],
    "simplewebswing" : ["a"],
    "simple" : ["a"],
    "simpleweb" : ["a"],
    "easyswing" : ["a"],
    "easywebswing" : ["a"],
    "easy" : ["a"],
    "easyweb" : ["a"],
    "highswing" : ["a"],
    "highwebswing" : ["a"],

    "getoverhere" : ["g"],
    "goh" : ["g"],
    "web pull" : ["g", f"[{GOH_HIT_DISPLACE_DELAY}f]"],
    "pull" : ["g", f"[{GOH_HIT_DISPLACE_DELAY}f]"],

    "getoverheretargeting" : ["G"],
    "getoverheretargetting" : ["G"],
    "goht" : ["G"],

    "uppercut" : ["u"],
    "upper" : ["u"],
    "amazingcombo" : ["u"],

    "symbiote" : ["S"],
    "symbiot" : ["S"],

    "venom" : ["V"],
    "venomsymbiote" : ["V"],
    "venomsymbiot" : ["V"],
    "upgradedsymbiote" : ["V"],
    "upgradedsymbiot" : ["V"],

    "clap" : ["C"],
    "peniclap" : ["C"],

    "webbomb" : ["B"],
    "bomb" : ["B"],
    "peniwebbomb" : ["B"],
    "penibomb" : ["B"],

    "explosion" : ["E"],
    "webexplosion" : ["E"],
    "exp" : ["E"],
    "peniexplosion" : ["E"],
    "peniwebexplosion" : ["E"],
    "peniexp" : ["E"],
}

COMBO_NAMES = {

}