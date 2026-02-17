class Action:
    name: str

    def __init__(self, name):
        self.name = name

ACTIONS = {
    "p" : Action (
        name = "Punch"
    ),

    "k" : Action (
        name = "Kick"
    ),

    "o" : Action (
        name = "Overhead"
    ),

    "t" : Action (
        name = "Tracer"
    ),

    "s" : Action (
        name = "Swing"
    ),

    "a" : Action (
        name = "Auto Swing"
    ),

    "w" : Action (
        name = "Whiff"
    ),

    "g" : Action (
        name = "Get Over Here"
    ),

    "G" : Action (
        name = "Get Over Here Targetting"
    ),

    "u" : Action (
        name = "Uppercut"
    ),

    "S" : Action (
        name = "Symbiote"
    ),

    "b" : Action (
        name = "Burn Tracer"
    ),

    "c" : Action (
        name = "Clap"
    ),

    "e" : Action (
        name = "Explosive Tracer"
    ),

    "E" : Action (
        name = "Explosion"
    )
}

# movestacks
# TO DO