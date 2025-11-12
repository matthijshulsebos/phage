from abc import ABC, abstractmethod
from common.models.direction import Direction


class Piece(ABC):
    """
    Base class for all piece types.
    """

    def __init__(self, owner=None):
        self.owner = owner
        self.position = None

    @property
    @abstractmethod
    def name(self):
        """Return the name of the pieces (e.g., 'Hunter')."""
        pass

    @property
    @abstractmethod
    def symbol(self):
        """Return a single-character symbol for display on the board."""
        pass

    @abstractmethod
    def valid_moves(self, board):
        """
        Return a list of valid moves (coordinates or directions)
        this pieces can make, given the current board state.
        """
        pass

    def move(self, new_position):
        """Update the pieces' position."""
        self.position = new_position
