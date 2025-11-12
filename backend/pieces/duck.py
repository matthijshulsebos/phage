from .piece import Piece
from common.models.coordinate import Coord
from common.models.direction import Direction
from typing import List


class Duck(Piece):
    """
    Duck piece - 2 points (Neutral piece)
    - Can be captured by foxes and hunters
    - Both players can move ducks
    - Moves any number of spaces in a straight line
    """

    @property
    def name(self):
        return "Duck"

    @property
    def symbol(self):
        return "D"

    @property
    def points(self):
        return 2

    def valid_moves(self, board):
        """
        Return list of valid moves for the duck.
        Ducks can move any number of spaces in a straight line.
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
                
                # Stop at any piece (ducks don't capture anything)
                break
        
        return valid_moves