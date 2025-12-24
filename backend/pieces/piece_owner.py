from enum import Enum

class PieceOwner(Enum):
    NONE = "none"  # Added for empty tiles
    PLAYER1 = "player1"
    PLAYER2 = "player2"
    NEUTRAL = "neutral"
