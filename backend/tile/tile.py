
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
        
        # Movement restriction tracking
        self.previous_position = None
        self.last_moved_by = None  # Track which player last moved this piece
        self.last_revealed_by = None  # Track which player last revealed this piece


    def flip(self, revealed_by_player=None):
        """Reveal this tile."""
        self.flipped = True
        self.last_revealed_by = revealed_by_player

    def capture(self):
        """Mark this tile as captured/removed from play."""
        self.alive = False
        self.position = None

    def move_to(self, pos: Coord, moved_by_player=None):
        """Update position when moved on the board."""
        self.previous_position = self.position
        self.position = pos
        self.last_moved_by = moved_by_player


    def is_movable(self):
        """Return True if this tile can be moved by a player."""
        # Only debris cannot be moved (they can only be removed)
        return self.tile_type != TileType.DEBRIS

    def belongs_to(self, player_faction):
        """Check if this tile is controlled by a player."""
        return self.faction == player_faction
    