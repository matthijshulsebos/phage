from enum import Enum

class TileType(Enum):
    VIRUS = "virus"
    BACTERIA = "bacteria"
    T_CELL = "t_cell"
    DENDRITIC_CELL = "dendritic_cell"
    RED_BLOOD_CELL = "red_blood_cell"
    DEBRIS = "debris"

class TileOwner(Enum):
    NONE = "none"
    PLAYER1 = "player1"
    PLAYER2 = "player2"
    NEUTRAL = "neutral"
