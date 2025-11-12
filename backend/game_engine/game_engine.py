from player.player import Player
from .models.game_phase import GamePhase
from .game_rules_validator import GameRulesValidator
from common.models.action import ActionType
from board.board import Board


class GameEngine:
    """
    Represents the current game state and orchestrates turns.

    Attributes:

    """

    def __init__(self, players, board=None):
        self.board = board if board else Board()
        self.players = players
        self.current_turn = 0
        self.current_player_turn_index = 0
        self.turns_remaining = None
        self.phase = GamePhase.FLIP
        self.rounds_remaining = None
        self.winner = None
        self.scores = {player.name: 0 for player in players}
        self.rules_validator = GameRulesValidator(self)


    @property
    def current_player(self) -> 'Player':
        """Returns the player whose turn it is."""
        return self.players[self.current_player_turn_index]


    @property
    def is_game_over(self) -> bool:
        """Returns True if all tiles are flipped and scoring rounds finished."""
        return self.phase == GamePhase.FINISHED


    def start(self) -> None:
        """Starts the game loop."""

        print("Welcome to De Beer is Los!")
        self.run_game_loop()
        return None


    def run_game_loop(self) -> None:
        """Runs the game loop."""

        while self.phase != GamePhase.FINISHED:
            player = self.current_player
            action = player.choose_action(self)
            points = self.apply_action(player, action)
            self.next_turn()
            self.update_scores(player, points)


    def update_scores(self, player, points) -> None:
        """Update the player's score."""
        self.scores[player.name] += points


    def next_turn(self) -> None:
        """Switch to next player's turn and check phase transitions."""

        self.check_phase_transition()
        self.current_player_turn_index = (self.current_player_turn_index + 1) % len(self.players)
        pass


    def check_phase_transition(self) -> None:
        """Check if phase should transition based on game state."""

        if self.board.all_tiles_face_up and self.phase == GamePhase.FLIP:
            self.advance_phase()
        elif self.phase == GamePhase.ESCAPE and self.rounds_remaining <= 0:
            self.advance_phase()
        elif self.phase == GamePhase.FINISHED:
            self.end_game()
        
        return None


    def apply_action(self, player, action) -> int:
        """Apply the given action to the board/game state."""
        
        # Validate action first
        is_valid, error_msg = self.rules_validator.validate_action(player, action)
        if not is_valid:
            raise ValueError(f"Invalid action: {error_msg}")

        points = 0
        
        if action.type == ActionType.FLIP:
            self.board.flip_tile(action.target)
        elif action.type == ActionType.MOVE:
            points, captured = self.board.move_tile(action.source, action.target, player)
        elif action.type == ActionType.SHOOT:
            points = self.board.shoot(player, action.target, action.direction)
        elif action.type == ActionType.CUT:
            points = self.board.cut_tree(action.target, player)

        return points


    def advance_phase(self) -> None:
        if self.phase == GamePhase.FLIP:
            self.phase = GamePhase.ESCAPE
            self.rounds_remaining = 5
        elif self.phase == GamePhase.ESCAPE:
            self.rounds_remaining -= 1
            if self.rounds_remaining <= 0:
                self.phase = GamePhase.FINISHED


    def end_game(self) -> None:
        """Calculates final scores and declares the winner."""

        highest_score = -1
        
        for player in self.players:
            if player.score > highest_score:
                highest_score = player.score
                self.winner = player
        
        print(f"Game Over! The winner is {self.winner.name} with {highest_score} points.")
        