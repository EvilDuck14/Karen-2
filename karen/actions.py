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

    "a" : Action (
        name = "Auto Swing"
    ),

    "w" : Action (
        name = "Swing Whiff"
    ),

    "g" : Action (
        name = "Get Over Here"
    ),

    "G" : Action (
        name = "Get Over Here Targetting"
    ),

    "u" : Action (
        name = "Uppercut"
    )
}

# TO DO
MOVESTACKS = {

}