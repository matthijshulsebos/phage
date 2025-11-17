from .piece import Piece
from common.models.coordinate import Coord
from common.models.direction import Direction
from typing import List



class Bacteria(Piece):
    """
    Bacteria piece - 5 points
    - Captures red blood cells
    - Can move any number of empty spaces in a straight line
    """

    @property
    def name(self):
        return "Bacteria"

    @property
    def symbol(self):
        return "B"

    @property
    def points(self):
        return 5

    def valid_moves(self, board):
        """
        Return list of valid moves for the bacteria.
        Bacteria can move any number of spaces in a straight line.
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
                if self._can_capture(target_tile):
                    valid_moves.append(new_pos)
                break
        return valid_moves

    def _can_capture(self, target_tile):
        """Check if bacteria can capture the target piece."""
        if not target_tile or not hasattr(target_tile, 'tile_type'):
            return False
        from tile.tile_types import TileType
        # Bacteria capture red blood cells
        return target_tile.tile_type == TileType.RED_BLOOD_CELL