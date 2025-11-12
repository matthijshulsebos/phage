from .piece import Piece
from common.models.coordinate import Coord
from common.models.direction import Direction
from typing import List


class Bear(Piece):
    """
    Bear piece - 10 points
    - Captures hunters and lumberjacks (not other animals)
    - Moves only 1 space horizontally or vertically per turn
    """

    @property
    def name(self):
        return "Bear"

    @property
    def symbol(self):
        return "B"

    @property
    def points(self):
        return 10

    def valid_moves(self, board):
        """
        Return list of valid moves for the bear.
        Bears can only move 1 space horizontally or vertically.
        """
        if not self.position:
            return []

        valid_moves = []
        
        # Check all 4 directions, but only 1 space
        directions = [
            Direction.NORTH,
            Direction.SOUTH, 
            Direction.EAST,
            Direction.WEST
        ]
        
        for direction in directions:
            dx, dy = direction.value
            new_pos = Coord(self.position.x + dx, self.position.y + dy)
            
            # Check if move is within bounds
            if board.is_within_bounds(new_pos):
                target_tile = board.get_tile(new_pos)
                
                # Bears can move to empty spaces or capture hunters/lumberjacks
                if not target_tile or self._can_capture(target_tile):
                    valid_moves.append(new_pos)
        
        return valid_moves

    def _can_capture(self, target_tile):
        """Check if bear can capture the target piece."""
        if not target_tile or not hasattr(target_tile, 'tile_type'):
            return False
        
        from tile.tile_types import TileType
        # Bears capture hunters and lumberjacks
        return target_tile.tile_type in [TileType.HUNTER, TileType.LUMBERJACK]