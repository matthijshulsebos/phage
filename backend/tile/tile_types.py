from enum import Enum

class TileType(Enum):
    BEAR = "bear"
    FOX = "fox" 
    HUNTER = "hunter"
    LUMBERJACK = "lumberjack"
    DUCK = "duck"
    PHEASANT = "pheasant"
    TREE = "tree"

class TileOwner(Enum):
    NONE = "none"
    PLAYER1 = "player1"
    PLAYER2 = "player2"
    NEUTRAL = "neutral"
