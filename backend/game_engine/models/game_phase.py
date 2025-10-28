from enum import Enum, auto

class GamePhase(Enum):
    """Represents the current stage of the game lifecycle."""

    """Players reveal tiles and move pieces until all tiles are revealed."""
    FLIP = auto()
    """Final 5 rounds where animals try to escape and hunters try to stop them."""
    ESCAPE = auto()
    """Game is over, scores are counted, and the winner is determined."""
    FINISHED = auto()
