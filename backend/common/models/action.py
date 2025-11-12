from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

class ActionType(Enum):
    FLIP = auto()
    MOVE = auto()
    SHOOT = auto()
    CUT = auto()

@dataclass(frozen=True)
class Action:
    type: ActionType
    target: Optional[object] = None
    source: Optional[object] = None
    direction: Optional[object] = None
    steps: int = 1
        