from .piece import Piece
from common.models.coordinate import Coord
from common.models.direction import Direction
from typing import List


class Fox(Piece):
    """
    Fox piece - 5 points
    - Captures pheasants and ducks
    - Can move any number of empty spaces in a straight line
    """

    @property
    def name(self):
        return "Fox"

    @property
    def symbol(self):
        return "F"

    @property
    def points(self):
        return 5

    def valid_moves(self, board):
        """
        Return list of valid moves for the fox.
        Foxes can move any number of spaces in a straight line.
        """
        if not self.position:
            return []

        valid_moves = []
        
        # Check all 4 directions
        directions = [
            Direction.NORTH,
            Direction.SOUTH, 
            Direction.EAST,
            Direction.WEST
        ]
        
        for direction in directions:
            dx, dy = direction.value
            
            # Keep moving in this direction until blocked
            distance = 1
            while True:
                new_pos = Coord(
                    self.position.x + (dx * distance),
                    self.position.y + (dy * distance)
                )
                
                # Stop if out of bounds
                if not board.is_within_bounds(new_pos):
                    break
                
                target_tile = board.get_tile(new_pos)
                
                # If empty, can move here and continue
                if not target_tile:
                    valid_moves.append(new_pos)
                    distance += 1
                    continue
                
                # If can capture, add this position and stop
                if self._can_capture(target_tile):
                    valid_moves.append(new_pos)
                
                # Stop at any piece (capturable or not)
                break
        
        return valid_moves

    def _can_capture(self, target_tile):
        """Check if fox can capture the target piece."""
        if not target_tile or not hasattr(target_tile, 'tile_type'):
            return False
        
        from tile.tile_types import TileType
        # Foxes capture pheasants and ducks
        return target_tile.tile_type in [TileType.PHEASANT, TileType.DUCK]