
class Tile:
    def __init__(self, tile_type: TileType, faction: TileOwner = TileOwner.NONE, points: int = 0):
        self.tile_type = tile_type
        self.faction = faction
        self.points = points
        self.flipped = False
        self.position = None
        self.alive = True

    # -------------------------
    # State changes
    # -------------------------
    def flip(self):
        """Reveal this tile."""
        self.flipped = True

    def capture(self):
        """Mark this tile as captured/removed from play."""
        self.alive = False
        self.position = None

    def move_to(self, pos):
        """Update position when moved on the board."""
        self.position = pos

    # -------------------------
    # Helpers
    # -------------------------
    def is_movable(self):
        """Return True if this tile can be moved by a player."""
        return self.tile_type not in (TileType.TREE, TileType.EMPTY)

    def belongs_to(self, player_faction):
        """Check if this tile is controlled by a player."""
        return self.faction == player_faction