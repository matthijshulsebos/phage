from player.player import Player
from pieces.piece_owner import PieceOwner
from common.models.action import Action, ActionType
from common.models.coordinate import Coord
import random


class AIPlayer(Player):
    def __init__(self, name: str, faction: PieceOwner = None):
        super().__init__(name, faction)

    def choose_action(self, game_engine):
        """AI chooses a random valid action."""
        from common.logging_config import logger
        logger.info(f"{self.name} is thinking...")

        # During FLIP phase, prioritize flipping tiles
        if game_engine.phase.name == "FLIP" and game_engine.board.has_hidden_tiles():
            return self._choose_random_flip(game_engine)

        # During ESCAPE phase, try to escape or move pieces
        if game_engine.phase.name == "ESCAPE":
            escape_action = self._choose_escape_action(game_engine)
            if escape_action:
                return escape_action
            # Try any valid move in escape phase
            move_action = self._choose_any_valid_move(game_engine)
            if move_action:
                return move_action
            # If no action possible, return a "pass" action (move to same position won't work, so we skip)
            logger.info(f"{self.name} has no valid moves, passing turn")
            return None

        # Otherwise, try to make a move
        move_action = self._choose_random_move(game_engine)
        if move_action:
            return move_action

        # If no moves possible, try to flip
        return self._choose_random_flip(game_engine)
    
    def _choose_random_flip(self, game_engine):
        """Choose a random tile to flip."""
        from common.logging_config import logger
        hidden_tiles = []
        
        for x in range(game_engine.board.size):
            for y in range(game_engine.board.size):
                coord = Coord(x, y)
                tile = game_engine.board.get_tile(coord)
                if tile and not tile.flipped:
                    hidden_tiles.append(coord)
        
        if hidden_tiles:
            target = random.choice(hidden_tiles)
            logger.info(f"{self.name} flips tile at ({target.x}, {target.y})")
            return Action(ActionType.FLIP, target=target)
        
        return None
    
    def _choose_escape_action(self, game_engine):
        """Choose an escape action during ESCAPE phase."""
        from common.logging_config import logger

        # Find pieces that can escape (are at edge exit positions)
        escapable_pieces = []

        for x in range(game_engine.board.size):
            for y in range(game_engine.board.size):
                coord = Coord(x, y)
                tile = game_engine.board.get_tile(coord)
                if tile and tile.flipped:
                    # Check if AI can move this piece
                    can_move, _ = game_engine.rules_validator._check_piece_ownership(self, tile)
                    if can_move and game_engine.board.can_exit_from_position(coord):
                        escapable_pieces.append(coord)

        if escapable_pieces:
            # Pick a random piece to escape
            source = random.choice(escapable_pieces)
            logger.info(f"{self.name} escapes piece from ({source.x}, {source.y})")
            return Action(ActionType.ESCAPE, source=source)

        # If no pieces can escape directly, try to move a piece toward an exit
        return self._choose_move_toward_exit(game_engine)

    def _choose_move_toward_exit(self, game_engine):
        """Try to move a piece toward an exit position."""
        from common.logging_config import logger

        exit_positions = [
            Coord(3, 0),  # North
            Coord(6, 3),  # East
            Coord(3, 6),  # South
            Coord(0, 3),  # West
        ]

        movable_pieces = []
        for x in range(game_engine.board.size):
            for y in range(game_engine.board.size):
                coord = Coord(x, y)
                tile = game_engine.board.get_tile(coord)
                if tile and tile.flipped:
                    can_move, _ = game_engine.rules_validator._check_piece_ownership(self, tile)
                    if can_move:
                        movable_pieces.append(coord)

        if not movable_pieces:
            return None

        # Try to move a random piece toward the nearest exit
        random.shuffle(movable_pieces)
        for source in movable_pieces:
            # Find closest exit
            closest_exit = min(exit_positions,
                               key=lambda e: abs(e.x - source.x) + abs(e.y - source.y))

            # Determine direction to move
            dx = 0 if closest_exit.x == source.x else (1 if closest_exit.x > source.x else -1)
            dy = 0 if closest_exit.y == source.y else (1 if closest_exit.y > source.y else -1)

            # Try moving in the primary direction first
            for move_dx, move_dy in [(dx, 0), (0, dy), (-dx, 0), (0, -dy)]:
                if move_dx == 0 and move_dy == 0:
                    continue
                target = Coord(source.x + move_dx, source.y + move_dy)
                if game_engine.board.is_within_bounds(target):
                    target_tile = game_engine.board.get_tile(target)
                    if not target_tile:  # Empty space
                        logger.info(f"{self.name} moves piece from ({source.x}, {source.y}) to ({target.x}, {target.y})")
                        return Action(ActionType.MOVE, source=source, target=target)

        return None

    def _choose_any_valid_move(self, game_engine):
        """Try to find any valid move for any piece."""
        from common.logging_config import logger

        for x in range(game_engine.board.size):
            for y in range(game_engine.board.size):
                coord = Coord(x, y)
                tile = game_engine.board.get_tile(coord)
                if tile and tile.flipped:
                    can_move, _ = game_engine.rules_validator._check_piece_ownership(self, tile)
                    if can_move:
                        # Try all directions
                        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            target = Coord(coord.x + dx, coord.y + dy)
                            if game_engine.board.is_within_bounds(target):
                                target_tile = game_engine.board.get_tile(target)
                                # Can move to empty space or capture opponent
                                if not target_tile or (target_tile.flipped and target_tile.faction != tile.faction):
                                    logger.info(f"{self.name} moves piece from ({coord.x}, {coord.y}) to ({target.x}, {target.y})")
                                    return Action(ActionType.MOVE, source=coord, target=target)
        return None

    def _choose_random_move(self, game_engine):
        """Choose a random piece to move."""
        from common.logging_config import logger
        movable_pieces = []

        for x in range(game_engine.board.size):
            for y in range(game_engine.board.size):
                coord = Coord(x, y)
                tile = game_engine.board.get_tile(coord)
                if tile and tile.flipped:
                    # Check if AI can move this piece based on ownership rules
                    can_move, _ = game_engine.rules_validator._check_piece_ownership(self, tile)
                    if can_move:
                        movable_pieces.append(coord)

        if movable_pieces:
            # Pick random piece
            source = random.choice(movable_pieces)

            # Pick random adjacent target
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                target = Coord(source.x + dx, source.y + dy)
                if game_engine.board.is_within_bounds(target):
                    logger.info(f"{self.name} moves piece from ({source.x}, {source.y}) to ({target.x}, {target.y})")
                    return Action(ActionType.MOVE, source=source, target=target)

        return None