from abc import ABC, abstractmethod
from common.models.action import Action

class Player(ABC):
    @abstractmethod
    def __init__(self, name: str):
        self.name = name
        self.pieces = []
        self.score = 0

    @abstractmethod
    def choose_action(self) -> Action:
        """Decide on an action to take during the player's turn."""
        pass
