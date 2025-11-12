from tile.tile import Tile
from tile.tile_types import TileType, TileOwner
from common.models.coordinate import Coord
from typing import Optional
import random


class Board:
    def __init__(self):
        self.size = 7
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        # Forest exit positions (4 exits at board edges)
        # Positioned at middle of each edge with arrow indicators
        self.forest_exits = [
            Coord(3, 0),    # North exit (top edge, center)
            Coord(6, 3),    # East exit (right edge, center)  
            Coord(3, 6),    # South exit (bottom edge, center)
            Coord(0, 3),    # West exit (left edge, center)
        ]
        
        self._setup_initial_tiles()

    def _setup_initial_tiles(self):
        """Set up the game board with randomized piece placement."""
        
        # Correct piece distribution from game instructions:
        # 1 spelbord, 48 tegels onderverdeeld in:
        # - 2 beren en 6 vossen (blauwe achtergrond) 
        # - 2 houthakkers en 8 jagers (bruine achtergrond)
        # - 7 eenden, 8 fazanten en 15 bomen (groene achtergrond)
        piece_distribution = [
            # Animal team (Blue - Player 2)
            (TileType.BEAR, TileOwner.PLAYER2, 2),       # 2 bears
            (TileType.FOX, TileOwner.PLAYER2, 6),        # 6 foxes
            
            # Hunter team (Brown - Player 1)  
            (TileType.LUMBERJACK, TileOwner.PLAYER1, 2), # 2 lumberjacks
            (TileType.HUNTER, TileOwner.PLAYER1, 8),     # 8 hunters
            
            # Neutral pieces (Green - both players can move)
            (TileType.DUCK, TileOwner.NEUTRAL, 7),       # 7 ducks  
            (TileType.PHEASANT, TileOwner.NEUTRAL, 8),   # 8 pheasants
            (TileType.TREE, TileOwner.NEUTRAL, 15),      # 15 trees
        ]
        
        # Create list of all pieces to place
        pieces_to_place = []
        for tile_type, owner, count in piece_distribution:
            for _ in range(count):
                pieces_to_place.append((tile_type, owner))
        
        # Verify we have exactly the right number of pieces
        assert len(pieces_to_place) == 48, f"Expected 48 pieces, got {len(pieces_to_place)}"
        
        # Shuffle for random placement
        random.shuffle(pieces_to_place)
        
        # Place pieces on board (skip center position 3,3)
        piece_index = 0
        for x in range(self.size):
            for y in range(self.size):
                coord = Coord(x, y)
                
                # Skip center position (remains None - no tile)
                if x == 3 and y == 3:
                    continue
                
                # Get next piece from shuffled list
                tile_type, owner = pieces_to_place[piece_index]
                piece_index += 1
                
                # Create tile with the assigned piece
                tile = Tile(
                    position=coord, 
                    tile_type=tile_type, 
                    faction=owner,
                    points=self._get_piece_points(tile_type)
                )
                
                # All tiles start face-down
                tile.flipped = False
                
                self.grid[x][y] = tile
    
    def _get_piece_points(self, tile_type: TileType) -> int:
        """Return point value for each piece type."""
        point_values = {
            TileType.BEAR: 10,
            TileType.HUNTER: 5,
            TileType.LUMBERJACK: 5,
            TileType.FOX: 5,
            TileType.PHEASANT: 3,
            TileType.DUCK: 2,
            TileType.TREE: 2,
            # No EMPTY type anymore - empty means no tile
        }
        return point_values.get(tile_type, 0)

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

    def flip_tile(self, pos, player=None):
        tile = self.get_tile(pos)
        if tile and not tile.flipped:
            tile.flip(player)
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
        from_tile.move_to(to_pos, player)
        
        return points, captured_tile

    def shoot(self, player, source_pos, direction):
        """
        Hunter shooting action.
        Hunters shoot in a straight line in their fixed direction until they hit a target.
        """
        from common.models.direction import Direction
        
        # Get the hunter piece
        hunter_tile = self.get_tile(source_pos)
        if not hunter_tile or hunter_tile.tile_type != TileType.HUNTER:
            raise ValueError("No hunter at source position")
        
        # Determine shooting direction (for now, use provided direction)
        # TODO: In full implementation, hunters should have fixed shooting directions
        direction_map = {
            Direction.NORTH: (0, -1),
            Direction.SOUTH: (0, 1),
            Direction.EAST: (1, 0),
            Direction.WEST: (-1, 0)
        }
        
        if direction not in direction_map:
            raise ValueError("Invalid shooting direction")
        
        dx, dy = direction_map[direction]
        points = 0
        
        # Trace along shooting direction until we hit something
        distance = 1
        while True:
            target_pos = Coord(
                source_pos.x + (dx * distance),
                source_pos.y + (dy * distance)
            )
            
            # Stop if out of bounds
            if not self.is_within_bounds(target_pos):
                break
            
            target_tile = self.get_tile(target_pos)
            
            # If we hit a tile, check if hunter can capture it
            if target_tile:
                # Hunters can capture all animals
                if target_tile.tile_type in [TileType.BEAR, TileType.FOX, TileType.PHEASANT, TileType.DUCK]:
                    points = target_tile.points
                    target_tile.capture()
                    self.grid[target_pos.x][target_pos.y] = None
                    print(f"Hunter shot {target_tile.tile_type.name} for {points} points!")
                    break
                else:
                    # Shot blocked by non-capturable piece (tree, other hunter, etc.)
                    print(f"Hunter shot blocked by {target_tile.tile_type.name}")
                    break
            
            distance += 1
        
        return points

    def cut_tree(self, source_pos, player):
        """
        Lumberjack tree cutting action.
        Lumberjacks can cut trees in adjacent spaces (1 space away).
        """
        from common.models.direction import Direction
        
        # Get the lumberjack piece
        lumberjack_tile = self.get_tile(source_pos)
        if not lumberjack_tile or lumberjack_tile.tile_type != TileType.LUMBERJACK:
            raise ValueError("No lumberjack at source position")
        
        points = 0
        trees_cut = 0
        
        # Check all 4 adjacent directions for trees
        directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
        
        for direction in directions:
            dx, dy = direction.value
            target_pos = Coord(source_pos.x + dx, source_pos.y + dy)
            
            if self.is_within_bounds(target_pos):
                target_tile = self.get_tile(target_pos)
                
                # If there's a tree, cut it down
                if target_tile and target_tile.tile_type == TileType.TREE:
                    points += target_tile.points
                    target_tile.capture()
                    self.grid[target_pos.x][target_pos.y] = None
                    trees_cut += 1
                    print(f"Lumberjack cut down tree at ({target_pos.x}, {target_pos.y}) for {target_tile.points} points!")
        
        if trees_cut == 0:
            print("No trees adjacent to lumberjack to cut")
        else:
            print(f"Lumberjack cut down {trees_cut} tree(s) for {points} total points!")
        
        return points

    def is_forest_exit(self, pos: Coord) -> bool:
        """Check if a position is a forest exit."""
        return pos in self.forest_exits

    def escape_through_exit(self, source_pos: Coord, player) -> tuple[int, bool]:
        """
        Escape a piece through a forest exit during the end game phase.
        Returns (points, success).
        Only allowed during ESCAPE phase.
        """
        piece_tile = self.get_tile(source_pos)
        if not piece_tile:
            return 0, False
        
        # Remove the piece from the board and award points
        points = piece_tile.points
        piece_tile.capture()
        self.grid[source_pos.x][source_pos.y] = None
        
        print(f"{piece_tile.tile_type.name} escaped through forest exit for {points} points!")
        return points, True

    def get_valid_exit_moves(self, source_pos: Coord) -> list[Coord]:
        """
        Get valid forest exit moves from a position.
        Returns list of forest exits the piece can reach.
        """
        piece_tile = self.get_tile(source_pos)
        if not piece_tile or not piece_tile.flipped:
            return []
        
        valid_exits = []
        
        for exit_pos in self.forest_exits:
            # Check if piece can move to this exit
            if self._can_reach_exit(source_pos, exit_pos, piece_tile):
                valid_exits.append(exit_pos)
        
        return valid_exits

    def _can_reach_exit(self, source_pos: Coord, exit_pos: Coord, piece_tile) -> bool:
        """
        Check if a piece can reach a specific forest exit.
        Uses same movement rules as normal piece movement.
        """
        # Check if move is orthogonal (horizontal or vertical only)
        dx = abs(exit_pos.x - source_pos.x)
        dy = abs(exit_pos.y - source_pos.y)
        
        if dx != 0 and dy != 0:
            return False  # Diagonal moves not allowed
        
        # Check movement distance based on piece type
        total_distance = dx + dy
        
        if piece_tile.tile_type in [TileType.BEAR, TileType.LUMBERJACK]:
            # Can only move 1 space
            if total_distance != 1:
                return False
        elif piece_tile.tile_type in [TileType.FOX, TileType.HUNTER, TileType.DUCK, TileType.PHEASANT]:
            # Can move any number of spaces, but path must be clear
            if total_distance < 1:
                return False
                
            # Check if path is clear
            move_dx = 0 if exit_pos.x == source_pos.x else (1 if exit_pos.x > source_pos.x else -1)
            move_dy = 0 if exit_pos.y == source_pos.y else (1 if exit_pos.y > source_pos.y else -1)
            
            # Check each step along the path (excluding source and target)
            current = Coord(source_pos.x + move_dx, source_pos.y + move_dy)
            
            while current != exit_pos:
                tile = self.get_tile(current)
                if tile:
                    return False  # Path blocked
                current = Coord(current.x + move_dx, current.y + move_dy)
        
        return True
