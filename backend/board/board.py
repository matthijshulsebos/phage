from tile.tile import Tile
from tile.tile_types import TileType, TileOwner
from common.models.coordinate import Coord
from common.logging_config import logger
from typing import Optional
import random


class Board:
    def __init__(self):
        self.size = 7
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        # Forest exit positions (imaginary positions one step outside the board)
        self.forest_exits = [
            Coord(3, -1),   # North exit (one step north from edge)
            Coord(7, 3),    # East exit (one step east from edge)
            Coord(3, 7),    # South exit (one step south from edge)
            Coord(-1, 3),   # West exit (one step west from edge)
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
            # Pathogen team (Red - Player 2)
            (TileType.VIRUS, TileOwner.PLAYER2, 2),       # 2 viruses
            (TileType.BACTERIA, TileOwner.PLAYER2, 6),    # 6 bacteria

            # Immune system team (Blue - Player 1)
            (TileType.DENDRITIC_CELL, TileOwner.PLAYER1, 2), # 2 dendritic cells
            (TileType.T_CELL, TileOwner.PLAYER1, 8),          # 8 T cells

            # Neutral pieces (both players can move)
            (TileType.RED_BLOOD_CELL, TileOwner.NEUTRAL, 7),  # 7 red blood cells (2pt)
            (TileType.RED_BLOOD_CELL, TileOwner.NEUTRAL, 8),  # 8 red blood cells (3pt)
            (TileType.DEBRIS, TileOwner.NEUTRAL, 15),         # 15 debris
        ]
        
        # Create list of all pieces to place
        pieces_to_place = []
        for tile_type, owner, count in piece_distribution:
            pieces_to_place.extend([(tile_type, owner)] * count)
        
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
            TileType.VIRUS: 10,
            TileType.T_CELL: 5,
            TileType.DENDRITIC_CELL: 5,
            TileType.BACTERIA: 5,
            TileType.RED_BLOOD_CELL: 3,  # Default to 3, but can be 2 for some
            TileType.DEBRIS: 2,
        }
        return point_values.get(tile_type, 0)

    def get_tile(self, pos):
        return None if not self.is_within_bounds(pos) else self.grid[pos.x][pos.y]

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
        T cell shooting action.
        T cells shoot in a straight line in their fixed direction until they hit a target.
        """
        from common.models.direction import Direction
        
        # Get the T cell piece
        tcell_tile = self.get_tile(source_pos)
        if not tcell_tile or tcell_tile.tile_type != TileType.T_CELL:
            raise ValueError("No T cell at source position")
        
        # Determine shooting direction (for now, use provided direction)
        # TODO: In full implementation, T cells should have fixed shooting directions
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
            
            # If we hit a tile, check if T cell can capture it
            if target_tile:
                # T cells can capture all pathogens and red blood cells
                if target_tile.tile_type in [TileType.VIRUS, TileType.BACTERIA, TileType.RED_BLOOD_CELL]:
                    points = target_tile.points
                    target_tile.capture()
                    self.grid[target_pos.x][target_pos.y] = None
                    logger.info(f"T cell shot {target_tile.tile_type.name} for {points} points!")
                    break
                else:
                    # Shot blocked by non-capturable piece (debris, other T cell, etc.)
                    logger.info(f"T cell shot blocked by {target_tile.tile_type.name}")
                    break
            
            distance += 1
        
        return points

    def remove_debris(self, source_pos, player):
        """
        Dendritic cell debris removal action.
        Dendritic cells can remove debris in adjacent spaces (1 space away).
        """
        from common.models.direction import Direction
        
        # Get the dendritic cell piece
        dendritic_tile = self.get_tile(source_pos)
        if not dendritic_tile or dendritic_tile.tile_type != TileType.DENDRITIC_CELL:
            raise ValueError("No dendritic cell at source position")
        
        points = 0
        debris_removed = 0
        
        # Check all 4 adjacent directions for debris
        directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
        
        for direction in directions:
            dx, dy = direction.value
            target_pos = Coord(source_pos.x + dx, source_pos.y + dy)
            
            if self.is_within_bounds(target_pos):
                target_tile = self.get_tile(target_pos)
                
                # If there's debris, remove it
                if target_tile and target_tile.tile_type == TileType.DEBRIS:
                    points += target_tile.points
                    target_tile.capture()
                    self.grid[target_pos.x][target_pos.y] = None
                    debris_removed += 1
                    logger.info(f"Dendritic cell removed debris at ({target_pos.x}, {target_pos.y}) for {target_tile.points} points!")
        
        if debris_removed == 0:
            logger.info("No debris adjacent to dendritic cell to remove")
        else:
            logger.info(f"Dendritic cell removed {debris_removed} debris piece(s) for {points} total points!")

        return points

    def is_forest_exit(self, pos: Coord) -> bool:
        """Check if a position is a forest exit (imaginary position outside the board)."""
        return pos in self.forest_exits

    def can_exit_from_position(self, pos: Coord) -> bool:
        """Check if a piece at this position can exit the forest during ESCAPE phase."""
        # Pieces can exit from the 4 forest exit positions:
        # North exit: (3, 0) - center of top edge
        # East exit: (6, 3) - center of right edge  
        # South exit: (3, 6) - center of bottom edge
        # West exit: (0, 3) - center of left edge
        
        return (pos.x == 3 and pos.y == 0) or \
               (pos.x == 6 and pos.y == 3) or \
               (pos.x == 3 and pos.y == 6) or \
               (pos.x == 0 and pos.y == 3)

    def escape_from_position(self, pos: Coord, player) -> tuple[int, bool]:
        """
        Escape a piece from an edge position during the ESCAPE phase.
        Returns (points, success).
        """
        piece_tile = self.get_tile(pos)
        if not piece_tile:
            return 0, False
        
        # Check if piece can exit from this position
        if not self.can_exit_from_position(pos):
            return 0, False
        
        # Remove the piece from the board and award points
        points = piece_tile.points
        piece_tile.capture()
        self.grid[pos.x][pos.y] = None
        
        exit_direction = "North" if pos.y == 0 else \
                        "East" if pos.x == 6 else \
                        "South" if pos.y == 6 else "West"
        
        logger.info(f"{piece_tile.tile_type.name} escaped through {exit_direction} forest exit for {points} points!")
        return points, True

    def escape_to_exit_position(self, source_pos: Coord, exit_pos: Coord, player) -> tuple[int, bool]:
        """
        Escape a piece by moving it to a forest exit position (outside the board).
        Returns (points, success).
        """
        piece_tile = self.get_tile(source_pos)
        if not piece_tile:
            return 0, False
        
        # Validate that the piece can reach this exit position
        if not self._can_reach_exit_position(source_pos, exit_pos, piece_tile):
            return 0, False
        
        # Remove the piece from the board and award points
        points = piece_tile.points
        piece_tile.capture()
        self.grid[source_pos.x][source_pos.y] = None
        
        exit_direction = "North" if exit_pos.y == -1 else \
                        "East" if exit_pos.x == 7 else \
                        "South" if exit_pos.y == 7 else "West"
        
        logger.info(f"{piece_tile.tile_type.name} escaped through {exit_direction} forest exit for {points} points!")
        return points, True

    def _can_reach_exit_position(self, source_pos: Coord, exit_pos: Coord, piece_tile) -> bool:
        """
        Check if a piece can reach a specific forest exit position.
        Forest exits are one step outside the board boundaries.
        """
        # Check if move is orthogonal (horizontal or vertical only)
        dx = abs(exit_pos.x - source_pos.x)
        dy = abs(exit_pos.y - source_pos.y)
        
        if dx != 0 and dy != 0:
            return False  # Diagonal moves not allowed
        
        # Check movement distance based on piece type
        total_distance = dx + dy
        
        if piece_tile.tile_type in [TileType.VIRUS, TileType.DENDRITIC_CELL]:
            # Can only move 1 space - must be adjacent to board edge to exit
            # For viruses/dendritic cells to reach exit position, they must be at the board edge
            edge_distance = self._distance_to_board_edge(source_pos, exit_pos)
            if edge_distance > 1:
                return False
        elif piece_tile.tile_type in [TileType.BACTERIA, TileType.T_CELL, TileType.RED_BLOOD_CELL]:
            # Can move any number of spaces, check if path is clear
            if total_distance < 1:
                return False
                
            # Check if path is clear (only need to check path within the board)
            path_clear = self._check_path_to_exit(source_pos, exit_pos)
            if not path_clear:
                return False
        
        return True

    def _distance_to_board_edge(self, source_pos: Coord, exit_pos: Coord) -> int:
        """Calculate minimum distance from source to the board edge in the direction of the exit."""
        if exit_pos.y == -1:  # North exit
            return source_pos.y + 1  # Distance to top edge (y=0) + 1 to exit
        elif exit_pos.x == 7:  # East exit
            return (6 - source_pos.x) + 1  # Distance to right edge (x=6) + 1 to exit
        elif exit_pos.y == 7:  # South exit
            return (6 - source_pos.y) + 1  # Distance to bottom edge (y=6) + 1 to exit
        elif exit_pos.x == -1:  # West exit
            return source_pos.x + 1  # Distance to left edge (x=0) + 1 to exit
        return float('inf')

    def _check_path_to_exit(self, source_pos: Coord, exit_pos: Coord) -> bool:
        """Check if the path from source to exit is clear (within board boundaries)."""
        move_dx = 0 if exit_pos.x == source_pos.x else (1 if exit_pos.x > source_pos.x else -1)
        move_dy = 0 if exit_pos.y == source_pos.y else (1 if exit_pos.y > source_pos.y else -1)
        
        # Check each step along the path until we reach the board edge
        current = Coord(source_pos.x + move_dx, source_pos.y + move_dy)
        
        while self.is_within_bounds(current):
            if (tile := self.get_tile(current)):
                return False  # Path blocked
            current = Coord(current.x + move_dx, current.y + move_dy)
        
        return True

    def get_valid_exit_positions(self, source_pos: Coord) -> list[Coord]:
        """
        Get valid forest exit positions the piece can reach to escape.
        Returns list of edge positions the piece can move to and then escape from.
        """
        piece_tile = self.get_tile(source_pos)
        if not piece_tile or not piece_tile.flipped:
            return []
        
        valid_exits = []
        
        # Check all four edge exit positions
        edge_positions = [
            Coord(3, 0),  # North edge
            Coord(6, 3),  # East edge  
            Coord(3, 6),  # South edge
            Coord(0, 3),  # West edge
        ]
        
        return [edge_pos for edge_pos in edge_positions
                if self._can_reach_edge_position(source_pos, edge_pos, piece_tile)]

    def _can_reach_edge_position(self, source_pos: Coord, edge_pos: Coord, piece_tile) -> bool:
        """
        Check if a piece can reach a specific edge position to escape.
        Uses same movement rules as normal piece movement.
        """
        # If already at the edge position, can exit immediately
        if source_pos == edge_pos:
            return True
        
        # Check if move is orthogonal (horizontal or vertical only)
        dx = abs(edge_pos.x - source_pos.x)
        dy = abs(edge_pos.y - source_pos.y)
        
        if dx != 0 and dy != 0:
            return False  # Diagonal moves not allowed
        
        # Check movement distance based on piece type
        total_distance = dx + dy
        
        if piece_tile.tile_type in [TileType.VIRUS, TileType.DENDRITIC_CELL]:
            # Can only move 1 space - must be adjacent to edge to exit in one move
            if total_distance > 1:
                return False
        elif piece_tile.tile_type in [TileType.BACTERIA, TileType.T_CELL, TileType.RED_BLOOD_CELL]:
            # Can move any number of spaces, but path must be clear
            if total_distance < 1:
                return False
                
            # Check if path is clear
            move_dx = 0 if edge_pos.x == source_pos.x else (1 if edge_pos.x > source_pos.x else -1)
            move_dy = 0 if edge_pos.y == source_pos.y else (1 if edge_pos.y > source_pos.y else -1)
            
            # Check each step along the path (excluding source and target)
            current = Coord(source_pos.x + move_dx, source_pos.y + move_dy)
            
            while current != edge_pos:
                if (tile := self.get_tile(current)):
                    return False  # Path blocked
                current = Coord(current.x + move_dx, current.y + move_dy)
        
        return True
