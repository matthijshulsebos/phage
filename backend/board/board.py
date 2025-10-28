from tile.tile import Tile

class Board:
    def __init__(self):
        self.size = 7
        self.tiles = self._setup_initial_tiles()

    # === Properties ===

    @property
    def face_down_tiles_count(self) -> int:
        count = 0
        for tile in self.tiles:
            if not tile.is_face_up:
                count += 1
        return count

    @property
    def all_tiles_face_up(self) -> bool:
        for tile in self.tiles:
            if not tile.is_face_up:
                return False
        return True


    # === Tile management ===

    def _setup_initial_tiles(self) -> list[Tile]:
        """Place all tiles face-down and leaving the center empty."""

        tiles = []
        for x in range(self.size):
            for y in range(self.size):
                # Center tile is empty
                if x == 4 and y == 4:
                    pass
                tiles.append(Tile(x, y))

        return tiles

    def get_tile(self, pos):
        """Return the Tile object at pos or None."""
        pass

    def flip_tile(self, pos):
        """Flip a hidden tile at pos. Returns the tile revealed."""
        pass


    # === Movement & actions ===

    def move_tile(self, from_pos, to_pos, player):
        """
        Move a tile belonging to Player (or neutral tile).
        Validate per movement rules (step/range, allowed directions).
        Return (points, captured_tile or None).
        """
        pass

    def shoot(self, player, pos, direction):
        """
        Handle hunter shooting in a given direction.
        Return points scored if an animal is hit.
        """
        pass

    def cut_tree(self, pos, player):
        """
        Handle lumberjack cutting down a tree.
        Return points scored.
        """
        pass

    def move_off_board(self, pos, player):
        """
        Handle moving a tile off the board during escape phase.
        Return points scored for saving that pieces.
        """
        pass


    # === Helpers ===

    def is_within_bounds(self, pos):
        """Return True if pos is inside board limits."""
        pass

    def has_hidden_tiles(self):
        """Return True if any tile is still face-down."""
        pass