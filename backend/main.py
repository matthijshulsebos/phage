from game_engine.game_engine import GameEngine
from player.ai_player import AIPlayer
from player.human_player import HumanPlayer


if __name__ == '__main__':
    players = [
        HumanPlayer("Mat"),
        AIPlayer("Bot Bob"),
    ]
    game = GameEngine(players)
    game.start()
