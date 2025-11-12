from .piece import Piece
from typing import List


class Tree(Piece):
    """
    Tree piece - 2 points
    - Can be chopped down by lumberjacks
    - Acts as an obstacle for all other pieces (cannot pass through)
    - Cannot be moved, only captured
    """

    @property
    def name(self):
        return "Tree"

    @property
    def symbol(self):
        return "T"

    @property
    def points(self):
        return 2

    def valid_moves(self, board):
        """
        Trees cannot move.
        Return empty list.
        """
        return []