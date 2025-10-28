from player.player import Player

class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def choose_action(self, game_engine):
        """Prompt the human player for an action."""
        pass