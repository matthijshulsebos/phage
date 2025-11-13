import pytest
from api.models.game_manager import GameSessionManager
from common.models.action import Action, ActionType
from common.models.coordinate import Coord
from common.models.direction import Direction

@pytest.fixture
def game_manager():
    return GameSessionManager()

def test_create_and_play_game(game_manager):
    # Create a new game
    game_id = game_manager.create_game("Alice", None)  # Alice vs AI
    state = game_manager.get_game_state(game_id)
    assert state is not None
    assert state["players"][0] == "Alice"
    assert state["is_active"]

    # Flip a tile
    flip_action = Action(ActionType.FLIP, target=Coord(0, 0))
    success, msg, points = game_manager.apply_action(game_id, "Alice", flip_action)
    assert success
    assert "Action applied" in msg

    # Try invalid move (not Alice's turn)
    move_action = Action(ActionType.MOVE, source=Coord(0, 0), target=Coord(0, 1))
    success, msg, points = game_manager.apply_action(game_id, "Alice", move_action)
    assert not success
    assert "Not your turn" in msg

    # Simulate AI turn (should be handled internally, but for test, call next_turn)
    session = game_manager.get_game(game_id)
    session.game_engine.next_turn()

    # Now Alice's turn again, try a move
    success, msg, points = game_manager.apply_action(game_id, "Alice", move_action)
    # Move may or may not be valid depending on board, so just check no crash
    assert isinstance(success, bool)

    # End the game manually
    session.is_active = False
    session.winner = "Alice"
    state = game_manager.get_game_state(game_id)
    assert state["winner"] == "Alice"

    # Delete the game
    assert game_manager.delete_game(game_id)
    assert game_manager.get_game(game_id) is None

def test_cleanup_expired_games(game_manager):
    game_id = game_manager.create_game("Bob", None)
    session = game_manager.get_game(game_id)
    session.last_activity = session.last_activity.replace(year=2000)  # Force expiration
    cleaned = game_manager.cleanup_expired_games(timeout_hours=1)
    assert cleaned == 1
    assert game_manager.get_game(game_id) is None
