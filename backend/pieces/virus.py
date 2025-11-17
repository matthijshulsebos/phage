from .piece import Piece
from common.models.coordinate import Coord
from common.models.direction import Direction
from typing import List



class Virus(Piece):
    """
    Virus piece - 10 points
    - Captures T cells and dendritic cells (not other pathogens)
    - Moves only 1 space horizontally or vertically per turn
    """

    @property
    def name(self):
        return "Virus"

    @property
    def symbol(self):
        return "V"

    @property
    def points(self):
        return 10

    def valid_moves(self, board):
        """
        Return list of valid moves for the virus.
        Viruses can only move 1 space horizontally or vertically.
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
                # Viruses can move to empty spaces or capture T cells/dendritic cells
                if not target_tile or self._can_capture(target_tile):
                    valid_moves.append(new_pos)
        return valid_moves

    def _can_capture(self, target_tile):
        """Check if virus can capture the target piece."""
        if not target_tile or not hasattr(target_tile, 'tile_type'):
            return False
        from tile.tile_types import TileType
        # Viruses capture T cells and dendritic cells
        return target_tile.tile_type in [TileType.T_CELL, TileType.DENDRITIC_CELL]