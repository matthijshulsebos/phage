from tile.tile import Tile
from tile.tile_types import TileType, TileOwner
from common.models.coordinate import Coord
from typing import Optional


class Board:
    def __init__(self):
        self.size = 7
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self._setup_initial_tiles()

    def _setup_initial_tiles(self):
        for x in range(self.size):
            for y in range(self.size):
                coord = Coord(x, y)
                if x == 3 and y == 3:
                    continue
                tile = Tile(coord)
                self.grid[x][y] = tile

    def get_tile(self, pos):
        if not self.is_within_bounds(pos):
            return None
        return self.grid[pos.x][pos.y]

    def is_within_bounds(self, pos):
        return 0 <= pos.x < self.size and 0 <= pos.y < self.size

    @property
    def face_down_tiles_count(self):
        count = 0
        for row in self.grid:
            for tile in row:
                if tile and not tile.flipped:
                    count += 1
        return count

    @property
    def all_tiles_face_up(self):
        for row in self.grid:
            for tile in row:
                if tile and not tile.flipped:
                    return False
        return True

    def has_hidden_tiles(self):
        """Return True if any tile is still face-down."""
        return self.face_down_tiles_count > 0

    def flip_tile(self, pos):
        tile = self.get_tile(pos)
        if tile and not tile.flipped:
            tile.flip()
            return tile
        return None

    def move_tile(self, from_pos, to_pos, player):
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
            points = to_tile.points
            to_tile.capture()
        
        # Move the piece
        self.grid[to_pos.x][to_pos.y] = from_tile
        self.grid[from_pos.x][from_pos.y] = None
        from_tile.move_to(to_pos)
        
        return points, captured_tile
