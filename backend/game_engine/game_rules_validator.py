from common.models.action import Action, ActionType
from common.models.coordinate import Coord
from tile.tile_types import TileType, TileOwner
from pieces.piece_owner import PieceOwner
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
        elif action.type == ActionType.ESCAPE:
            return self._validate_escape(player, action)
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
        
        # Check source position is valid (must be on board)
        if not self.game_engine.board.is_within_bounds(action.source):
            return False, "Source position out of bounds"
        
        # Get the piece to move
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
        
        # Check if target is a forest exit (special case - outside bounds allowed)
        if self.game_engine.board.is_forest_exit(action.target):
            return self._validate_forest_exit_move(player, from_tile, action.source, action.target)
        
        # For normal moves, check if target position is valid (must be on board)
        if not self.game_engine.board.is_within_bounds(action.target):
            return False, "Target position out of bounds"
        if not self.game_engine.board.is_within_bounds(action.target):
            return False, "Target position out of bounds"
        
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
        
        # Check movement restrictions
        restriction_valid, restriction_msg = self._check_movement_restrictions(player, from_tile, action.source, action.target)
        if not restriction_valid:
            return False, restriction_msg
        
        return True, ""

    def _validate_shoot(self, player, action: Action) -> Tuple[bool, str]:
        """Validate shooting action."""
        
        # Check if position is valid
        if not self.game_engine.board.is_within_bounds(action.target):
            return False, "Position out of bounds"
        
        # Check if there's a T cell at the position
        tcell_tile = self.game_engine.board.get_tile(action.target)
        if not tcell_tile:
            return False, "No piece at that position"
        
        if not tcell_tile.flipped:
            return False, "Cannot shoot with face-down piece"
        
        if tcell_tile.tile_type != TileType.T_CELL:
            return False, "Only T cells can shoot"
        
        # Check ownership
        can_move, ownership_msg = self._check_piece_ownership(player, tcell_tile)
        if not can_move:
            return False, ownership_msg
        
        # Shooting direction validation would go here
        # For now, assume direction is provided and valid
        if not action.direction:
            return False, "Shooting direction required"
        
        return True, ""

    def _validate_cut(self, player, action: Action) -> Tuple[bool, str]:
        """Validate debris removal action."""
        
        # Check if position is valid
        if not self.game_engine.board.is_within_bounds(action.target):
            return False, "Position out of bounds"
        
        # Check if there's a dendritic cell at the position
        dendritic_tile = self.game_engine.board.get_tile(action.target)
        if not dendritic_tile:
            return False, "No piece at that position"
        
        if not dendritic_tile.flipped:
            return False, "Cannot cut with face-down piece"
        
        if dendritic_tile.tile_type != TileType.DENDRITIC_CELL:
            return False, "Only dendritic cells can remove debris"
        
        # Check ownership
        can_move, ownership_msg = self._check_piece_ownership(player, dendritic_tile)
        if not can_move:
            return False, ownership_msg
        
        # Check if there are adjacent debris to remove
        from common.models.direction import Direction
        has_adjacent_debris = False
        
        directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
        for direction in directions:
            dx, dy = direction.value
            adjacent_pos = type('Coord', (), {
                'x': action.target.x + dx, 
                'y': action.target.y + dy
            })()
            if self.game_engine.board.is_within_bounds(adjacent_pos):
                adjacent_tile = self.game_engine.board.get_tile(adjacent_pos)
                if adjacent_tile and adjacent_tile.tile_type == TileType.DEBRIS:
                    has_adjacent_debris = True
                    break
        if not has_adjacent_debris:
            return False, "No debris adjacent to dendritic cell"
        
        return True, ""

    def _check_piece_ownership(self, player, tile) -> Tuple[bool, str]:
        """
        Check if player can move this piece.
        
        Rules:
        - Immune system pieces (T cells/dendritic cells) can only be moved by PLAYER1
        - Pathogen pieces (viruses/bacteria) can only be moved by PLAYER2  
        - Neutral pieces (red blood cells) can be moved by both players
        - A green card that was revealed or moved by opponent cannot be moved immediately after
        """
        
        if not hasattr(tile, 'tile_type'):
            return False, "Invalid piece"
        
        if not hasattr(player, 'faction') or player.faction is None:
            return False, "Player has no faction assigned"
        
        # Check ownership based on player faction and tile faction
        if tile.tile_type in [TileType.T_CELL, TileType.DENDRITIC_CELL]:
            # Immune system pieces - only PLAYER1
            if player.faction != PieceOwner.PLAYER1:
                return False, "Cannot move opponent's T cell/dendritic cell pieces"
        elif tile.tile_type in [TileType.VIRUS, TileType.BACTERIA]:
            # Pathogen pieces - only PLAYER2
            if player.faction != PieceOwner.PLAYER2:
                return False, "Cannot move opponent's virus/bacteria pieces"
        elif tile.tile_type == TileType.RED_BLOOD_CELL:
            # Neutral pieces - both players can move them (restrictions checked separately)
            pass
        elif tile.tile_type == TileType.DEBRIS:
            return False, "Debris cannot be moved, only removed"
        
        return True, ""

    def _check_capture_rules(self, attacker_tile, target_tile) -> Tuple[bool, str]:
        """Check if attacker can capture target according to game rules."""
        
        if not hasattr(attacker_tile, 'tile_type') or not hasattr(target_tile, 'tile_type'):
            return False, "Invalid pieces for capture"
        
        attacker_type = attacker_tile.tile_type
        target_type = target_tile.tile_type
        
        # Define capture rules
        capture_rules = {
            TileType.VIRUS: [TileType.T_CELL, TileType.DENDRITIC_CELL],
            TileType.BACTERIA: [TileType.RED_BLOOD_CELL],
            TileType.T_CELL: [TileType.VIRUS, TileType.BACTERIA, TileType.RED_BLOOD_CELL],
            TileType.DENDRITIC_CELL: [TileType.DEBRIS],
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
        if piece_type in [TileType.VIRUS, TileType.DENDRITIC_CELL]:
            # Can only move 1 space
            if total_distance != 1:
                return False, f"{piece_type.name} can only move 1 space"
        elif piece_type in [TileType.BACTERIA, TileType.T_CELL, TileType.RED_BLOOD_CELL]:
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
    
    def _check_movement_restrictions(self, player, piece_tile, source: Coord, target: Coord) -> Tuple[bool, str]:
        """
        Check movement restrictions:
        1. Pieces cannot return to their previous position
        2. Green pieces moved/revealed by opponent cannot be moved immediately after
        """
        
        # Check if piece is trying to return to previous position
        if (hasattr(piece_tile, 'previous_position') and piece_tile.previous_position and 
            piece_tile.previous_position.x == target.x and piece_tile.previous_position.y == target.y):
            return False, "Cannot return to previous position"
        
        # For neutral pieces (red blood cells), check opponent restrictions
        if piece_tile.tile_type == TileType.RED_BLOOD_CELL:
            # Check if opponent was the last to move this piece
            if (hasattr(piece_tile, 'last_moved_by') and piece_tile.last_moved_by and 
                piece_tile.last_moved_by != player):
                return False, "Cannot move green piece that opponent just moved"
            
            # Check if opponent was the last to reveal this piece
            if (hasattr(piece_tile, 'last_revealed_by') and piece_tile.last_revealed_by and 
                piece_tile.last_revealed_by != player):
                return False, "Cannot move green piece that opponent just revealed"
        
        return True, ""
    
    def _validate_escape(self, player, action: Action) -> Tuple[bool, str]:
        """
        Validate forest escape action during ESCAPE phase.
        """
        
        # Can only escape during ESCAPE phase
        if self.game_engine.phase.name != "ESCAPE":
            return False, "Forest exits only available during escape phase"
        
        # Check if source position is valid
        if not self.game_engine.board.is_within_bounds(action.source):
            return False, "Source position out of bounds"
        
        # Get the piece to escape
        piece_tile = self.game_engine.board.get_tile(action.source)
        if not piece_tile:
            return False, "No piece at source position"
        
        # Check if tile is flipped
        if not piece_tile.flipped:
            return False, "Cannot escape with face-down piece"
        
        # Check ownership
        can_move, ownership_msg = self._check_piece_ownership(player, piece_tile)
        if not can_move:
            return False, ownership_msg
        
        # Check if piece is at an edge position where it can escape
        if not self.game_engine.board.can_exit_from_position(action.source):
            return False, "Can only escape from forest exit positions: (3,0), (6,3), (3,6), or (0,3)"
        
        return True, ""
    
    def _validate_forest_exit_move(self, player, piece_tile, source: Coord, exit_pos: Coord) -> Tuple[bool, str]:
        """
        Validate move to forest exit position during ESCAPE phase.
        """
        
        # Can only use forest exits during ESCAPE phase
        if self.game_engine.phase.name != "ESCAPE":
            return False, "Forest exits only available during escape phase"
        
        # Check if piece can reach the exit position with their movement rules
        can_reach = self.game_engine.board._can_reach_exit_position(source, exit_pos, piece_tile)
        if not can_reach:
            return False, "Cannot reach forest exit from this position"
        
        return True, ""