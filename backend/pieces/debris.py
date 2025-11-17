from .piece import Piece
from typing import List



class Debris(Piece):
    """
    Debris piece - 2 points
    - Can be removed by dendritic cells
    - Acts as an obstacle for all other pieces (cannot pass through)
    - Cannot be moved, only removed
    """

    @property
    def name(self):
        return "Debris"

    @property
    def symbol(self):
        return "X"

    @property
    def points(self):
        return 2

    def valid_moves(self, board):
        """
        Debris cannot move.
        Return empty list.
        """
        return []