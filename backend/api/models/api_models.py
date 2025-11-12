from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Import existing enums from core models
from common.models.action import ActionType
from game_engine.models.game_phase import GamePhase
from tile.tile_types import TileType, TileOwner
from pieces.piece_owner import PieceOwner


# Request Models
class CreateGameRequest(BaseModel):
    player1_name: str
    # If none then AI will be player 2
    player2_name: Optional[str] = None


class CoordinateRequest(BaseModel):
    x: int
    y: int


class ActionRequest(BaseModel):
    action_type: ActionType
    source: Optional[CoordinateRequest] = None
    target: Optional[CoordinateRequest] = None
    direction: Optional[str] = None


# Response Models
class CoordinateResponse(BaseModel):
    x: int
    y: int


class TileResponse(BaseModel):
    x: int
    y: int
    flipped: bool
    tile_type: TileType
    faction: PieceOwner


class PlayerResponse(BaseModel):
    name: str
    score: int


class MoveHistoryResponse(BaseModel):
    timestamp: datetime
    player: str
    action_type: str
    details: Dict[str, Any]


class GameStateResponse(BaseModel):
    game_id: str
    created_at: datetime
    last_activity: datetime
    is_active: bool
    winner: Optional[str]
    players: List[str]
    current_player: str
    current_turn: int
    phase: GamePhase
    scores: Dict[str, int]
    rounds_remaining: Optional[int]
    board_size: int
    board_state: List[List[TileResponse]]
    face_down_tiles: int
    move_history: List[MoveHistoryResponse]


class GameListItemResponse(BaseModel):
    game_id: str
    players: List[str]
    is_active: bool
    created_at: datetime
    current_player: str
    phase: GamePhase
    winner: Optional[str]


class ActionResultResponse(BaseModel):
    success: bool
    message: str
    points_gained: Optional[int] = None
    game_state: Optional[GameStateResponse] = None


class CreateGameResponse(BaseModel):
    game_id: str
    message: str
    game_state: GameStateResponse


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


class StatsResponse(BaseModel):
    total_games: int
    active_games: int
    finished_games: int
    oldest_game: Optional[datetime]