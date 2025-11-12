from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ActionType(Enum):
    FLIP = "flip"
    MOVE = "move"
    SHOOT = "shoot"
    CUT = "cut"

@dataclass(frozen=True)
class Action:
    type: ActionType
    target: Optional[object] = None
    source: Optional[object] = None
    direction: Optional[object] = None
    steps: int = 1
        