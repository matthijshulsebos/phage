
from .tile_types import TileType, TileOwner
from common.models.coordinate import Coord
from typing import Optional

class Tile:
    def __init__(self, position: Coord, tile_type: TileType, 
                 faction: TileOwner = TileOwner.NONE, points: int = 0):
        self.tile_type = tile_type
        self.faction = faction
        self.points = points
        self.flipped = False
        self.position = position
        self.alive = True


    def flip(self):
        """Reveal this tile."""
        self.flipped = True

    def capture(self):
        """Mark this tile as captured/removed from play."""
        self.alive = False
        self.position = None

    def move_to(self, pos: Coord):
        """Update position when moved on the board."""
        self.position = pos


    def is_movable(self):
        """Return True if this tile can be moved by a player."""
        # Only trees cannot be moved (they can only be cut)
        return self.tile_type != TileType.TREE

    def belongs_to(self, player_faction):
        """Check if this tile is controlled by a player."""
        return self.faction == player_faction
    