from fastapi import APIRouter, HTTPException
from typing import List
from ..models.api_models import (
    CreateGameRequest, CreateGameResponse, ActionRequest, ActionResultResponse,
    GameStateResponse, GameListItemResponse, ErrorResponse, StatsResponse
)
from ..models.game_manager import game_session_manager
from common.models.action import Action, ActionType
from common.models.coordinate import Coord
from common.models.direction import Direction


router = APIRouter(prefix="/api/game", tags=["game"])


@router.post("/create", response_model=CreateGameResponse)
async def create_game(request: CreateGameRequest):
    """Create a new game session."""
    try:
        game_id = game_session_manager.create_game(
            request.player1_name, 
            request.player2_name
        )
        
        game_state = game_session_manager.get_game_state(game_id)
        if not game_state:
            raise HTTPException(status_code=500, detail="Failed to create game")
        
        return CreateGameResponse(
            game_id=game_id,
            message=f"Game created successfully. {request.player1_name} vs {game_state['players'][1]}",
            game_state=GameStateResponse(**game_state)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create game: {str(e)}")


@router.get("/{game_id}/state", response_model=GameStateResponse)
async def get_game_state(game_id: str):
    """Get the current state of a game."""
    game_state = game_session_manager.get_game_state(game_id)
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return GameStateResponse(**game_state)


@router.post("/{game_id}/action", response_model=ActionResultResponse)
async def apply_action(game_id: str, action_request: ActionRequest, player_name: str):
    """Apply a player action to the game."""
    try:
        # Convert API action to internal action
        action_type = ActionType[action_request.action_type.value]
        
        source = None
        target = None
        direction = None
        
        if action_request.source:
            source = Coord(action_request.source.x, action_request.source.y)
        
        if action_request.target:
            target = Coord(action_request.target.x, action_request.target.y)
        
        if action_request.direction:
            direction = Direction[action_request.direction]
        
        action = Action(
            type=action_type,
            source=source,
            target=target,
            direction=direction
        )
        
        # Apply the action
        success, message, points_gained = game_session_manager.apply_action(game_id, player_name, action)

        if not success:
            return ActionResultResponse(
                success=False,
                message=message,
                points_gained=0
            )

        # Get updated game state
        game_state = game_session_manager.get_game_state(game_id)

        return ActionResultResponse(
            success=True,
            message=message,
            points_gained=points_gained,
            game_state=GameStateResponse(**game_state) if game_state else None
        )
        
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid action parameter: {str(e)}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to apply action: {str(e)}") from e


@router.get("/list", response_model=List[GameListItemResponse])
async def list_games(include_inactive: bool = False):
    """List all games."""
    try:
        games = game_session_manager.list_games(include_inactive)
        return [GameListItemResponse(**game) for game in games]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to list games: {str(e)}"
        ) from e


@router.delete("/{game_id}")
async def delete_game(game_id: str):
    """Delete a game session."""
    success = game_session_manager.delete_game(game_id)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return {"message": f"Game {game_id} deleted successfully"}


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get overall game statistics."""
    try:
        stats = game_session_manager.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get stats: {str(e)}"
        ) from e


@router.post("/cleanup")
async def cleanup_expired_games(timeout_hours: int = 24):
    """Clean up expired game sessions."""
    try:
        count = game_session_manager.cleanup_expired_games(timeout_hours)
        return {"message": f"Cleaned up {count} expired games"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to cleanup: {str(e)}"
        ) from e