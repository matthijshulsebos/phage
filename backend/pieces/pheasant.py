from .piece import Piece
from common.models.coordinate import Coord
from common.models.direction import Direction
from typing import List


class Pheasant(Piece):
    """
    Pheasant piece - 3 points (Neutral piece)
    - Can be captured by foxes and hunters
    - Both players can move pheasants
    - Moves any number of spaces in a straight line
    """

    @property
    def name(self):
        return "Pheasant"

    @property
    def symbol(self):
        return "P"

    @property
    def points(self):
        return 3

    def valid_moves(self, board):
        """
        Return list of valid moves for the pheasant.
        Pheasants can move any number of spaces in a straight line.
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
                
                # Stop at any piece (pheasants don't capture anything)
                break
        
        return valid_moves