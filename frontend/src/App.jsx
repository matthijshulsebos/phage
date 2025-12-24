import { useState, useEffect } from 'react';
import './App.css';
import GameBoard from './components/GameBoard';
import api from './services/api';

function App() {
  const [gameState, setGameState] = useState(null);
  const [gameId, setGameId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedTile, setSelectedTile] = useState(null);
  const [playerName, setPlayerName] = useState('');
  const [opponentName, setOpponentName] = useState('');

  const createGame = async () => {
    if (!playerName) {
      setError('Please enter your name');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await api.createGame(
        playerName, 
        opponentName || null
      );
      setGameId(response.game_id);
      setGameState(response.game_state);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadGameState = async () => {
    if (!gameId) return;
    
    try {
      const state = await api.getGameState(gameId);
      setGameState(state);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleTileClick = (x, y, tile) => {
    console.log('Tile clicked:', { x, y, tile });
    
    if (!tile.flipped) {
      // TODO: Implement flip action
      console.log('Flip tile at', x, y);
    } else {
      // Select tile for movement
      setSelectedTile({ x, y, tile });
    }
  };

  if (!gameState) {
    return (
      <div className="app">
        <div className="menu">
          <h1>🦠 Phage</h1>
          <p>Immune System vs Pathogens</p>
          
          <div className="create-game-form">
            <input
              type="text"
              placeholder="Your name"
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
            />
            <input
              type="text"
              placeholder="Opponent name (leave empty for AI)"
              value={opponentName}
              onChange={(e) => setOpponentName(e.target.value)}
            />
            <button onClick={createGame} disabled={loading}>
              {loading ? 'Creating...' : 'Create Game'}
            </button>
          </div>
          
          {error && <div className="error">{error}</div>}
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="game-header">
        <h1>🦠 Phage</h1>
        <div className="game-info">
          <div className="player-info">
            <span className="player-name">{gameState.players[0]}</span>
            <span className="player-faction">(Immune System)</span>
            <span className="player-score">Score: {gameState.scores[gameState.players[0]]}</span>
          </div>
          <div className="vs">VS</div>
          <div className="player-info">
            <span className="player-name">{gameState.players[1]}</span>
            <span className="player-faction">(Pathogens)</span>
            <span className="player-score">Score: {gameState.scores[gameState.players[1]]}</span>
          </div>
        </div>
        <div className="game-status">
          Turn {gameState.current_turn} | Phase: {gameState.phase.toUpperCase()} | 
          Face-down tiles: {gameState.face_down_tiles}
        </div>
        <div className="current-turn">
          Current player: <strong>{gameState.current_player}</strong>
        </div>
      </header>

      <main className="game-main">
        <GameBoard
          boardState={gameState.board_state}
          onTileClick={handleTileClick}
          selectedTile={selectedTile}
          validMoves={[]} // TODO: Calculate valid moves
        />
        
        {selectedTile && (
          <div className="action-panel">
            <h3>Selected: {selectedTile.tile.tile_type}</h3>
            <p>Position: {String.fromCharCode(97 + selectedTile.x)}{selectedTile.y + 1}</p>
            <button onClick={() => setSelectedTile(null)}>Cancel</button>
          </div>
        )}
      </main>

      <button onClick={loadGameState} className="refresh-btn">
        Refresh Game State
      </button>
    </div>
  );
}

export default App;
