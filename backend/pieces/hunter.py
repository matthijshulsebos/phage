from .piece import Piece
from common.models.coordinate import Coord
from common.models.direction import Direction
from typing import List


class Hunter(Piece):
    """
    Hunter piece - 5 points
    - Captures all animals (bears, foxes, pheasants, and ducks) but only in shooting direction
    - Shooting direction cannot be changed (gun barrel determines capture direction)
    - Can move in all directions, but can only capture in the direction the gun points
    """

    def __init__(self, owner=None, shooting_direction=Direction.NORTH):
        super().__init__(owner)
        self.shooting_direction = shooting_direction

    @property
    def name(self):
        return "Hunter"

    @property
    def symbol(self):
        return "H"

    @property
    def points(self):
        return 5

    def valid_moves(self, board):
        """
        Return list of valid moves for the hunter.
        Hunters can move any number of spaces in any direction.
        """
        if not self.position:
            return []

        valid_moves = []
        
        # Check all 4 directions for movement
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
                
                # If can capture (only in shooting direction), add this position
                if direction == self.shooting_direction and self._can_capture(target_tile):
                    valid_moves.append(new_pos)
                
                # Stop at any piece
                break
        
        return valid_moves

    def valid_shots(self, board):
        """
        Return list of positions the hunter can shoot at.
        Hunters can only shoot in their fixed shooting direction.
        """
        if not self.position:
            return []

        valid_shots = []
        dx, dy = self.shooting_direction.value
        
        # Keep checking in shooting direction until we find a target
        distance = 1
        while True:
            target_pos = Coord(
                self.position.x + (dx * distance),
                self.position.y + (dy * distance)
            )
            
            # Stop if out of bounds
            if not board.is_within_bounds(target_pos):
                break
            
            target_tile = board.get_tile(target_pos)
            
            # If we find a piece, check if we can capture it
            if target_tile:
                if self._can_capture(target_tile):
                    valid_shots.append(target_pos)
                # Stop at any piece (shot is blocked)
                break
            
            distance += 1
        
        return valid_shots

    def _can_capture(self, target_tile):
        """Check if hunter can capture the target piece."""
        if not target_tile or not hasattr(target_tile, 'tile_type'):
            return False
        
        from tile.tile_types import TileType
        # Hunters capture all animals
        return target_tile.tile_type in [
            TileType.BEAR, TileType.FOX, TileType.PHEASANT, TileType.DUCK
        ]