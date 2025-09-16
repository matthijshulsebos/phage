from enum import Enum, auto

class ActionType(Enum):
    FLIP = auto()
    MOVE = auto()
    SHOOT = auto()
    CUT = auto()

class Action:
    def __init__(self, type: ActionType, target=None, direction=None, steps=1):
        self.type = type
        self.target = target
        self.direction = direction
        self.steps = steps