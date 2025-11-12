from common.models.action import Action, ActionType
from common.models.coordinate import Coord
from tile.tile_types import TileType, TileOwner
from typing import List, Optional, Tuple


class GameRulesValidator:
    """
    Validates game actions according to "De Beer is Los!" rules.
    """

    def __init__(self, game_engine):
        self.game_engine = game_engine

    def validate_action(self, player, action: Action) -> Tuple[bool, str]:
        """
        Validate if an action is legal for the given player.
        Returns (is_valid, error_message).
        """
        
        if action.type == ActionType.FLIP:
            return self._validate_flip(player, action)
        elif action.type == ActionType.MOVE:
            return self._validate_move(player, action)
        elif action.type == ActionType.SHOOT:
            return self._validate_shoot(player, action)
        elif action.type == ActionType.CUT:
            return self._validate_cut(player, action)
        
        return False, "Unknown action type"

    def _validate_flip(self, player, action: Action) -> Tuple[bool, str]:
        """Validate tile flip action."""
        
        # Can only flip during FLIP phase
        if self.game_engine.phase.name != "FLIP":
            return False, "Can only flip tiles during flip phase"
        
        # Check if position is valid
        if not self.game_engine.board.is_within_bounds(action.target):
            return False, "Position out of bounds"
        
        # Check if tile exists
        tile = self.game_engine.board.get_tile(action.target)
        if not tile:
            return False, "No tile at that position"
        
        # Check if tile is already flipped
        if tile.flipped:
            return False, "Tile is already flipped"
        
        return True, ""

    def _validate_move(self, player, action: Action) -> Tuple[bool, str]:
        """Validate piece movement action."""
        
        # Check positions are valid
        if not self.game_engine.board.is_within_bounds(action.source):
            return False, "Source position out of bounds"
        if not self.game_engine.board.is_within_bounds(action.target):
            return False, "Target position out of bounds"
        
        # Check if there's a piece to move
        from_tile = self.game_engine.board.get_tile(action.source)
        if not from_tile:
            return False, "No piece at source position"
        
        # Check if tile is flipped
        if not from_tile.flipped:
            return False, "Cannot move face-down piece"
        
        # Check ownership
        can_move, ownership_msg = self._check_piece_ownership(player, from_tile)
        if not can_move:
            return False, ownership_msg
        
        # Check if target position allows movement
        to_tile = self.game_engine.board.get_tile(action.target)
        if to_tile:
            # Check if we can capture this piece
            can_capture, capture_msg = self._check_capture_rules(from_tile, to_tile)
            if not can_capture:
                return False, capture_msg
        
        # Validate movement pattern for this piece type
        valid_move, movement_msg = self._check_movement_pattern(from_tile, action.source, action.target)
        if not valid_move:
            return False, movement_msg
        
        # Check path is clear (for pieces that move multiple spaces)
        path_clear, path_msg = self._check_movement_path(from_tile, action.source, action.target)
        if not path_clear:
            return False, path_msg
        
        return True, ""

    def _validate_shoot(self, player, action: Action) -> Tuple[bool, str]:
        """Validate shooting action."""
        # TODO: Implement shooting validation
        return False, "Shooting not yet implemented"

    def _validate_cut(self, player, action: Action) -> Tuple[bool, str]:
        """Validate tree cutting action."""
        # TODO: Implement tree cutting validation
        return False, "Tree cutting not yet implemented"

    def _check_piece_ownership(self, player, tile) -> Tuple[bool, str]:
        """
        Check if player can move this piece.
        
        Rules:
        - Brown cards can only be moved by the brown player (Player1)
        - Blue cards can only be moved by the blue player (Player2)  
        - Green cards (pheasants and ducks) can be moved by both players
        - A green card that was revealed or moved by opponent cannot be moved immediately after
        """
        
        if not hasattr(tile, 'tile_type'):
            return False, "Invalid piece"
        
        # Map players to factions (this is a simplification)
        # TODO: Add proper player faction system
        player_index = self.game_engine.players.index(player)
        
        if tile.tile_type in [TileType.HUNTER, TileType.LUMBERJACK]:
            # Brown pieces - only Player 1
            if player_index != 0:
                return False, "Cannot move opponent's hunter/lumberjack pieces"
        
        elif tile.tile_type in [TileType.BEAR, TileType.FOX]:
            # Blue pieces - only Player 2  
            if player_index != 1:
                return False, "Cannot move opponent's bear/fox pieces"
        
        elif tile.tile_type in [TileType.DUCK, TileType.PHEASANT]:
            # Green pieces - both players can move, but with restrictions
            # TODO: Add "recently moved by opponent" tracking
            pass
        
        elif tile.tile_type == TileType.TREE:
            return False, "Trees cannot be moved, only cut"
        
        return True, ""

    def _check_capture_rules(self, attacker_tile, target_tile) -> Tuple[bool, str]:
        """Check if attacker can capture target according to game rules."""
        
        if not hasattr(attacker_tile, 'tile_type') or not hasattr(target_tile, 'tile_type'):
            return False, "Invalid pieces for capture"
        
        attacker_type = attacker_tile.tile_type
        target_type = target_tile.tile_type
        
        # Define capture rules
        capture_rules = {
            TileType.BEAR: [TileType.HUNTER, TileType.LUMBERJACK],
            TileType.FOX: [TileType.PHEASANT, TileType.DUCK],
            TileType.HUNTER: [TileType.BEAR, TileType.FOX, TileType.PHEASANT, TileType.DUCK],
            TileType.LUMBERJACK: [TileType.TREE],
        }
        
        if attacker_type in capture_rules:
            if target_type in capture_rules[attacker_type]:
                return True, ""
            else:
                return False, f"{attacker_type.name} cannot capture {target_type.name}"
        
        return False, f"{attacker_type.name} cannot capture anything"

    def _check_movement_pattern(self, piece_tile, source: Coord, target: Coord) -> Tuple[bool, str]:
        """Check if the movement pattern is valid for this piece type."""
        
        if not hasattr(piece_tile, 'tile_type'):
            return False, "Invalid piece"
        
        piece_type = piece_tile.tile_type
        dx = abs(target.x - source.x)
        dy = abs(target.y - source.y)
        
        # Check if movement is orthogonal (horizontal or vertical)
        if dx != 0 and dy != 0:
            return False, "Can only move horizontally or vertically"
        
        total_distance = dx + dy
        
        # Movement rules by piece type
        if piece_type in [TileType.BEAR, TileType.LUMBERJACK]:
            # Can only move 1 space
            if total_distance != 1:
                return False, f"{piece_type.name} can only move 1 space"
        
        elif piece_type in [TileType.FOX, TileType.HUNTER, TileType.DUCK, TileType.PHEASANT]:
            # Can move any number of spaces in straight line
            if total_distance < 1:
                return False, "Must move at least 1 space"
        
        else:
            return False, f"Unknown piece type: {piece_type}"
        
        return True, ""

    def _check_movement_path(self, piece_tile, source: Coord, target: Coord) -> Tuple[bool, str]:
        """Check if the path from source to target is clear."""
        
        # Calculate direction
        dx = 0 if target.x == source.x else (1 if target.x > source.x else -1)
        dy = 0 if target.y == source.y else (1 if target.y > source.y else -1)
        
        # Check each step along the path (excluding source and target)
        current = Coord(source.x + dx, source.y + dy)
        
        while current != target:
            tile = self.game_engine.board.get_tile(current)
            if tile:
                return False, f"Path blocked by piece at ({current.x}, {current.y})"
            
            current = Coord(current.x + dx, current.y + dy)
        
        return True, ""