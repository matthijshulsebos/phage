from .piece import Piece
from common.models.coordinate import Coord
from common.models.direction import Direction
from typing import List



class RedBloodCell(Piece):
    """
    Red Blood Cell piece - 2 or 3 points (Neutral piece)
    - Can be captured by bacteria and T cells
    - Both players can move red blood cells
    - Moves any number of spaces in a straight line
    """

    def __init__(self, owner=None, points=2):
        super().__init__(owner)
        self._points = points

    @property
    def name(self):
        return "Red Blood Cell"

    @property
    def symbol(self):
        return "R"

    @property
    def points(self):
        return self._points

    def valid_moves(self, board):
        """
        Return list of valid moves for the red blood cell.
        Red blood cells can move any number of spaces in a straight line.
        """
        if not self.position:
            return []

        valid_moves = []
        directions = [
            Direction.NORTH,
            Direction.SOUTH, 
            Direction.EAST,
            Direction.WEST
        ]
        for direction in directions:
            dx, dy = direction.value
            distance = 1
            while True:
                new_pos = Coord(
                    self.position.x + (dx * distance),
                    self.position.y + (dy * distance)
                )
                if not board.is_within_bounds(new_pos):
                    break
                target_tile = board.get_tile(new_pos)
                if not target_tile:
                    valid_moves.append(new_pos)
                    distance += 1
                    continue
                break
        return valid_moves