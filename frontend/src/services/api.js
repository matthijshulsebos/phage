const API_BASE_URL = 'http://localhost:8000';

class PhageAPI {
  async createGame(player1Name, player2Name = null) {
    const response = await fetch(`${API_BASE_URL}/api/game/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        player1_name: player1Name, 
        player2_name: player2Name 
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create game');
    }
    
    return response.json();
  }

  async getGameState(gameId) {
    const response = await fetch(`${API_BASE_URL}/api/game/${gameId}/state`);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get game state');
    }
    
    return response.json();
  }

  async applyAction(gameId, playerName, action) {
    const response = await fetch(
      `${API_BASE_URL}/api/game/${gameId}/action?player_name=${encodeURIComponent(playerName)}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(action)
      }
    );
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to apply action');
    }
    
    return response.json();
  }

  async listGames(includeInactive = false) {
    const response = await fetch(
      `${API_BASE_URL}/api/game/list?include_inactive=${includeInactive}`
    );
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to list games');
    }
    
    return response.json();
  }

  async deleteGame(gameId) {
    const response = await fetch(`${API_BASE_URL}/api/game/${gameId}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to delete game');
    }
    
    return response.json();
  }
}

export default new PhageAPI();
