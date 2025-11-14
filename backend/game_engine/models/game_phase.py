from enum import Enum

class GamePhase(Enum):
    """Represents the current stage of the game lifecycle."""

    """Players reveal tiles and move pieces until all tiles are revealed."""
    FLIP = "flip"
    """Final 5 rounds where pathogens try to escape and T cells try to stop them."""
    ESCAPE = "escape"
    """Game is over, scores are counted, and the winner is determined."""
    FINISHED = "finished"
