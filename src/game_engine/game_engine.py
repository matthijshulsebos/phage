from .models.game_phase import GamePhase
from common.models.actions import ActionType, Action

class GameEngine:
    """
    Represents the current game state and orchestrates turns.

    Attributes:

    """

    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.current_turn = 0
        self.current_player_turn_index = 0
        self.phase = GamePhase.FLIP
        self.scores = {player.name: 0 for player in players}
        self.rounds_remaining = None
        self.winner = None


    @property
    def current_player(self):
        return self.players[self.current_player_turn_index]

    @property
    def is_game_over(self):
        """Returns True if all tiles are flipped and scoring rounds finished."""
        return False

    def start(self):
        """Starts the game loop."""

        # TODO: Put a cool opening animation here and optionally a game explanation.

        print("Welcome to De Beer is Los!")
        self.run_game_loop()
        return None

    def run_game_loop(self):
        """Runs the game loop."""

        while self.phase != GamePhase.FINISHED:
            player = self.current_player
            action = player.choose_action(self)
            points = self.apply_action(player, action)
            self.next_turn()
            self.update_scores(player, points)
            self.check_phase_transition()

    def update_scores(self, player, points):
        """Update the player's score."""
        self.scores[player.name] += points

    def next_turn(self):
        """Switch to next player's turn and check phase transitions."""

        self.check_phase_transition()
        pass

    def check_phase_transition(self):
        """"""
        # TODO: Check if we should move to the next game phase.
        pass

    def apply_action(self, player, action):
        """Apply the given action to the board/game state."""

        points = 0  # default if no points earned

        if action.type == ActionType.FLIP:
            self.board.flip_tile(action.target)
        elif action.type == ActionType.MOVE:
            self.board.move_piece(player, action.target, action.direction, action.steps)
        elif action.type == ActionType.SHOOT:
            points = self.board.shoot(player, action.target, action.direction)
        elif action.type == ActionType.CUT:
            points = self.board.cut_tree(action.target)

        return points

    def advance_phase(self):
        if self.phase == GamePhase.FLIP:
            self.phase = GamePhase.ESCAPE
            self.rounds_remaining = 5
        elif self.phase == GamePhase.ESCAPE:
            self.rounds_remaining -= 1
            if self.rounds_remaining <= 0:
                self.phase = GamePhase.FINISHED

    def end_game(self):
        """Calculates final scores and declares the winner."""
        pass
