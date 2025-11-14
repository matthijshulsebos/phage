from .piece import Piece
from common.models.coordinate import Coord
from common.models.direction import Direction
from typing import List



class DendriticCell(Piece):
    """
    Dendritic Cell piece - 5 points
    - Can remove all debris
    - Moves only 1 space horizontally or vertically per turn
    """

    @property
    def name(self):
        return "Dendritic Cell"

    @property
    def symbol(self):
        return "D"

    @property
    def points(self):
        return 5

    def valid_moves(self, board):
        """
        Return list of valid moves for the dendritic cell.
        Dendritic cells can only move 1 space horizontally or vertically.
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
            new_pos = Coord(self.position.x + dx, self.position.y + dy)
            if board.is_within_bounds(new_pos):
                target_tile = board.get_tile(new_pos)
                # Dendritic cells can move to empty spaces or remove debris
                if not target_tile or self._can_capture(target_tile):
                    valid_moves.append(new_pos)
        return valid_moves

    def _can_capture(self, target_tile):
        """Check if dendritic cell can remove the target piece (debris)."""
        if not target_tile or not hasattr(target_tile, 'tile_type'):
            return False
        from tile.tile_types import TileType
        # Dendritic cells remove debris
        return target_tile.tile_type == TileType.DEBRIS