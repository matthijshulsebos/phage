from abc import ABC, abstractmethod
from common.models.action import Action
from pieces.piece_owner import PieceOwner

class Player(ABC):
    def __init__(self, name: str, faction: PieceOwner = None):
        self.name = name
        self.faction = faction
        self.pieces = []
        self.score = 0

    @abstractmethod
    def choose_action(self, game_engine) -> Action:
        """Decide on an action to take during the player's turn."""
        pass
