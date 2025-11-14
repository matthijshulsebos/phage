import uuid
import threading
from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta
from game_engine.game_engine import GameEngine
from player.ai_player import AIPlayer
from player.human_player import HumanPlayer
from pieces.piece_owner import PieceOwner
from common.models.action import Action


class GameSession:
    """Represents a single game session with metadata."""
    
    def __init__(self, game_id: str, player1_name: str, player2_name: str = None):
        self.game_id = game_id
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.player1_name = player1_name
        self.player2_name = player2_name or "AI Bot"
        
        # Create players with proper factions
        # Player 1 gets the Immune System (T Cell/Dendritic Cell) faction (PLAYER1)
        # Player 2 gets the Blue/Animal faction (PLAYER2)
        player1 = HumanPlayer(self.player1_name, PieceOwner.PLAYER1)
        player2 = HumanPlayer(self.player2_name, PieceOwner.PLAYER2) if player2_name else AIPlayer(self.player2_name, PieceOwner.PLAYER2)
        
        # Create game engine
        self.game_engine = GameEngine([player1, player2])
        
        # Track game state
        self.is_active = True
        self.winner = None
        self.game_history = []  # Track all moves
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.now()
    
    def add_to_history(self, player_name: str, action: Action):
        """Add a move to the game history."""
        self.game_history.append({
            'timestamp': datetime.now(),
            'player': player_name,
            'action_type': action.type.name,
            'details': {
                'source': (action.source.x, action.source.y) if action.source else None,
                'target': (action.target.x, action.target.y) if action.target else None,
                'direction': action.direction.name if action.direction else None
            }
        })
    
    def is_expired(self, timeout_hours: int = 24) -> bool:
        """Check if session has expired."""
        expiry_time = self.last_activity + timedelta(hours=timeout_hours)
        return datetime.now() > expiry_time


class GameSessionManager:
    """
    Manages multiple game sessions for the API.
    Thread-safe for concurrent access.
    """
    
    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}
        self.lock = threading.RLock()  # Reentrant lock for thread safety
    
    def create_game(self, player1_name: str, player2_name: str = None) -> str:
        """
        Create a new game session.
        Returns the unique game ID.
        """
        with self.lock:
            game_id = str(uuid.uuid4())
            session = GameSession(game_id, player1_name, player2_name)
            self.sessions[game_id] = session
            
            from common.logging_config import logger
            logger.info(f"Created game {game_id}: {player1_name} vs {session.player2_name}")
            return game_id
    
    def get_game(self, game_id: str) -> Optional[GameSession]:
        """Get a game session by ID."""
        with self.lock:
            session = self.sessions.get(game_id)
            if session:
                session.update_activity()
            return session
    
    def apply_action(self, game_id: str, player_name: str, action: Action) -> Tuple[bool, str, int]:
        """
        Apply an action to a game session.
        Returns (success, message, points_gained).
        """
        with self.lock:
            session = self.get_game(game_id)
            if not session:
                return False, "Game not found", 0

            if not session.is_active:
                return False, "Game is not active", 0

            # Find the player
            player = next((p for p in session.game_engine.players if p.name == player_name), None)
            if not player:
                return False, "Player not found in this game", 0

            # Check if it's the player's turn
            current_player = session.game_engine.current_player
            if current_player.name != player_name:
                return False, f"Not your turn. Current player: {current_player.name}", 0

            try:
                # Apply the action
                points = session.game_engine.apply_action(player, action)

                # Add to history
                session.add_to_history(player_name, action)

                # Update scores
                session.game_engine.update_scores(player, points)

                # Advance turn
                session.game_engine.next_turn()

                # Check if game is over
                if session.game_engine.is_game_over:
                    session.is_active = False
                    session.winner = session.game_engine.winner.name if session.game_engine.winner else "Draw"

                return True, f"Action applied. Points gained: {points}", points

            except ValueError as e:
                return False, str(e), 0

    def get_game_state(self, game_id: str) -> Optional[Dict]:
        """Get the current state of a game."""
        session = self.get_game(game_id)
        if not session:
            return None
        
        game = session.game_engine
        
        # Build board state
        board_state = []
        for x in range(game.board.size):
            row = []
            for y in range(game.board.size):
                tile = game.board.get_tile(type('Coord', (), {'x': x, 'y': y})())
                if tile:
                    row.append({
                        'x': x,
                        'y': y,
                        'flipped': tile.flipped,
                        'tile_type': tile.tile_type.name if hasattr(tile, 'tile_type') else 'EMPTY',
                        'faction': tile.faction.name if hasattr(tile, 'faction') else 'NONE'
                    })
                else:
                    row.append({
                        'x': x,
                        'y': y,
                        'flipped': False,
                        'tile_type': 'EMPTY',
                        'faction': 'NONE'
                    })
            board_state.append(row)
        
        return {
            'game_id': game_id,
            'created_at': session.created_at.isoformat(),
            'last_activity': session.last_activity.isoformat(),
            'is_active': session.is_active,
            'winner': session.winner,
            'players': [p.name for p in game.players],
            'current_player': game.current_player.name,
            'current_turn': game.current_turn,
            'phase': game.phase.name,
            'scores': game.scores,
            'rounds_remaining': game.rounds_remaining,
            'board_size': game.board.size,
            'board_state': board_state,
            'face_down_tiles': game.board.face_down_tiles_count,
            'move_history': session.game_history[-10:]  # Last 10 moves
        }
    
    def list_games(self, include_inactive: bool = False) -> List[Dict]:
        """List all games with basic info."""
        with self.lock:
            games = []
            for game_id, session in self.sessions.items():
                if include_inactive or session.is_active:
                    games.append({
                        'game_id': game_id,
                        'players': [session.player1_name, session.player2_name],
                        'is_active': session.is_active,
                        'created_at': session.created_at.isoformat(),
                        'current_player': session.game_engine.current_player.name,
                        'phase': session.game_engine.phase.name,
                        'winner': session.winner
                    })
            
            return sorted(games, key=lambda x: x['created_at'], reverse=True)
    
    def cleanup_expired_games(self, timeout_hours: int = 24) -> int:
        """Remove expired game sessions. Returns number of games cleaned up."""
        from common.logging_config import logger
        with self.lock:
            expired_games = [game_id for game_id, session in self.sessions.items() 
                           if session.is_expired(timeout_hours)]

            for game_id in expired_games:
                del self.sessions[game_id]

            if expired_games:
                logger.info(f"Cleaned up {len(expired_games)} expired games")

            return len(expired_games)
    
    def delete_game(self, game_id: str) -> bool:
        """Delete a specific game session."""
        from common.logging_config import logger
        with self.lock:
            if game_id in self.sessions:
                del self.sessions[game_id]
                logger.info(f"Deleted game {game_id}")
                return True
            return False
    
    def get_stats(self) -> Dict:
        """Get overall statistics."""
        with self.lock:
            total_games = len(self.sessions)
            active_games = sum(bool(s.is_active) for s in self.sessions.values())
            
            return {
                'total_games': total_games,
                'active_games': active_games,
                'finished_games': total_games - active_games,
                'oldest_game': min((s.created_at for s in self.sessions.values()), default=None)
            }


# Global session manager instance
game_session_manager = GameSessionManager()
