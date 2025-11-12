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