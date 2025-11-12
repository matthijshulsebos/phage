from backend.tile.tile_types import TileType
from tile.tile import Tile
from common.models.coordinate import Coord
from typing import Optional, List

class Board:
    def __init__(self):
        self.size = 7
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self._setup_initial_tiles()


    @property
    def face_down_tiles_count(self) -> int:
        count = 0
        for row in self.grid:
            for tile in row:
                if tile and not tile.flipped:
                    count += 1
        return count

    @property
    def all_tiles_face_up(self) -> bool:
        for row in self.grid:
            for tile in row:
                if tile and not tile.flipped:
                    return False
        return True


    def _setup_initial_tiles(self) -> None:
        """Place all tiles face-down and leaving the center empty."""
        
        # For now, just place empty tiles
        for x in range(self.size):
            for y in range(self.size):
                coord = Coord(x, y)
                # Center tile (3,3) stays empty
                if x == 3 and y == 3:
                    continue
                # Create a basic tile for now
                tile = Tile(coord)
                self.grid[x][y] = tile


    def get_tile(self, pos: Coord) -> Optional[Tile]:
        """Return the Tile object at pos or None."""

        if not self.is_within_bounds(pos):
            return None
        return self.grid[pos.x][pos.y]


    def flip_tile(self, pos: Coord) -> Optional[Tile]:
        """Flip a hidden tile at pos. Returns the tile revealed."""

        tile = self.get_tile(pos)
        if tile and not tile.flipped:
            tile.flip()
            return tile
        return None


    def move_tile(self, from_pos: Coord, to_pos: Coord, player) -> tuple[int, Optional[Tile]]:
        """
        Move a tile belonging to Player (or neutral tile).
        Validate per movement rules (step/range, allowed directions).
        Return (points, captured_tile or None).
        """

        # Basic validation
        if not self.is_within_bounds(from_pos) or not self.is_within_bounds(to_pos):
            raise ValueError("Move positions out of bounds")
        
        from_tile = self.get_tile(from_pos)
        to_tile = self.get_tile(to_pos)
        
        if not from_tile:
            raise ValueError("No tile at starting position")
        
        points = 0
        captured_tile = None
        
        # If there's a tile at destination, capture it
        if to_tile:
            captured_tile = to_tile
            points = to_tile.points if hasattr(to_tile, 'points') else 0
            to_tile.capture()
        
        # Move the piece
        self.grid[to_pos.x][to_pos.y] = from_tile
        self.grid[from_pos.x][from_pos.y] = None
        from_tile.move_to(to_pos)
        
        return points, captured_tile

    def shoot(self, player, pos: Coord, direction) -> int:
        """
        Handle hunter shooting in a given direction.
        Return points scored if an animal is hit.
        """
        
        # TODO: Implement shooting logic
        # This will need to check direction and find first target
        return 0

    def cut_tree(self, pos: Coord, player) -> int:
        """
        Handle lumberjack cutting down a tree.
        Return points scored.
        """
        
        tile = self.get_tile(pos)
        if tile and tile.tile_type == TileType.TREE:
            tile.capture()
            return tile.points if hasattr(tile, 'points') else 2  # Trees are worth 2 points
        return 0

    def move_off_board(self, pos: Coord, player) -> int:
        """
        Handle moving a tile off the board during escape phase.
        Return points scored for saving that pieces.
        """

        tile = self.get_tile(pos)
        if tile:
            points = tile.points if hasattr(tile, 'points') else 0
            tile.capture()
            self.grid[pos.x][pos.y] = None
            return points
        return 0


    def is_within_bounds(self, pos: Coord) -> bool:
        """Return True if pos is inside board limits."""
        return 0 <= pos.x < self.size and 0 <= pos.y < self.size


    def has_hidden_tiles(self) -> bool:
        """Return True if any tile is still face-down."""
        return self.face_down_tiles_count > 0