import { useState, useEffect, useCallback } from 'react';
import './App.css';
import GameBoard from './components/GameBoard';
import api from './services/api';

function App() {
  const [gameState, setGameState] = useState(null);
  const [gameId, setGameId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);
  const [selectedTile, setSelectedTile] = useState(null);
  const [playerName, setPlayerName] = useState('Player');

  // Get the human player name (first player)
  const humanPlayer = gameState?.players?.[0] || playerName;
  const isMyTurn = gameState?.current_player === humanPlayer;

  const createGame = async () => {
    const name = playerName || 'Player';

    setLoading(true);
    setError(null);

    try {
      const response = await api.createGame(name, null); // Always vs AI
      setGameId(response.game_id);
      setGameState(response.game_state);
      setMessage('Game created! Flip a tile to start.');
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

  // Apply an action and handle the response
  const applyAction = useCallback(async (action) => {
    if (!gameId || !isMyTurn || actionLoading) return;

    setActionLoading(true);
    setError(null);
    setMessage(null);

    try {
      const result = await api.applyAction(gameId, humanPlayer, action);

      if (result.success) {
        setMessage(result.message);
        if (result.game_state) {
          setGameState(result.game_state);
        }
        setSelectedTile(null);
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setActionLoading(false);
    }
  }, [gameId, humanPlayer, isMyTurn, actionLoading]);

  // Handle AI turn - poll for updates when it's AI's turn
  useEffect(() => {
    if (!gameState || !gameId) return;
    if (gameState.phase === 'finished') return;

    // If it's not my turn, the AI is playing - poll for updates
    if (!isMyTurn) {
      const pollInterval = setInterval(async () => {
        try {
          const state = await api.getGameState(gameId);
          setGameState(state);

          // Stop polling if it's now my turn or game is finished
          if (state.current_player === humanPlayer || state.phase === 'finished') {
            clearInterval(pollInterval);
          }
        } catch (err) {
          console.error('Failed to poll game state:', err);
        }
      }, 1000);

      return () => clearInterval(pollInterval);
    }
  }, [gameState?.current_player, gameId, isMyTurn, humanPlayer, gameState?.phase]);

  const handleTileClick = (x, y, tile) => {
    // Don't allow actions if not my turn or loading
    if (!isMyTurn || actionLoading) {
      if (!isMyTurn) setMessage("Wait for your turn...");
      return;
    }

    // Clear previous messages on new action
    setError(null);
    setMessage(null);

    // If tile is not flipped, flip it
    if (!tile.flipped) {
      applyAction({
        action_type: 'flip',
        target: { x, y }
      });
      return;
    }

    // If clicking on an already selected tile, deselect it
    if (selectedTile && selectedTile.x === x && selectedTile.y === y) {
      setSelectedTile(null);
      return;
    }

    // If we have a selected tile and clicking on another tile, try to move
    if (selectedTile) {
      applyAction({
        action_type: 'move',
        source: { x: selectedTile.x, y: selectedTile.y },
        target: { x, y }
      });
      return;
    }

    // Select the flipped tile for movement
    // Only select if the tile has a piece that can be moved
    if (tile.tile_type !== 'empty' && tile.tile_type !== 'debris') {
      setSelectedTile({ x, y, tile });
      setMessage(`Selected ${tile.tile_type.replace('_', ' ')} at ${String.fromCharCode(97 + x)}${y + 1}`);
    }
  };

  if (!gameState) {
    return (
      <div className="app">
        <div className="menu">
          <h1>Phage</h1>
          <p>Immune System vs Pathogens</p>

          <div className="create-game-form">
            <button onClick={createGame} disabled={loading}>
              {loading ? 'Creating Game...' : 'Play vs AI'}
            </button>
          </div>

          {error && <div className="error">{error}</div>}
        </div>
      </div>
    );
  }

  const isGameOver = gameState.phase === 'finished';

  return (
    <div className="app">
      <header className="game-header">
        <h1>Phage</h1>
        <div className="game-info">
          <div className={`player-info ${gameState.current_player === gameState.players[0] ? 'active' : ''}`}>
            <span className="player-name">{gameState.players[0]}</span>
            <span className="player-faction">(Immune System)</span>
            <span className="player-score">Score: {gameState.scores[gameState.players[0]]}</span>
          </div>
          <div className="vs">VS</div>
          <div className={`player-info ${gameState.current_player === gameState.players[1] ? 'active' : ''}`}>
            <span className="player-name">{gameState.players[1]}</span>
            <span className="player-faction">(Pathogens)</span>
            <span className="player-score">Score: {gameState.scores[gameState.players[1]]}</span>
          </div>
        </div>
        <div className="game-status">
          Turn {gameState.current_turn} | Phase: {gameState.phase.toUpperCase()} |
          Face-down tiles: {gameState.face_down_tiles}
        </div>
        <div className={`current-turn ${isMyTurn ? 'your-turn' : 'opponent-turn'}`}>
          {isGameOver
            ? `Game Over! Winner: ${gameState.winner || 'Draw'}`
            : isMyTurn
              ? 'Your turn - flip a tile or move a piece'
              : `Waiting for ${gameState.current_player}...`}
        </div>
        {actionLoading && <div className="action-loading">Processing...</div>}
      </header>

      {/* Message and error display */}
      {message && <div className="message">{message}</div>}
      {error && <div className="error">{error}</div>}

      <main className="game-main">
        <GameBoard
          boardState={gameState.board_state}
          onTileClick={handleTileClick}
          selectedTile={selectedTile}
          validMoves={[]}
          disabled={!isMyTurn || actionLoading || isGameOver}
        />

        {selectedTile && (
          <div className="action-panel">
            <h3>Selected: {selectedTile.tile.tile_type.replace('_', ' ')}</h3>
            <p>Position: {String.fromCharCode(97 + selectedTile.x)}{selectedTile.y + 1}</p>
            <p>Click another tile to move, or click again to deselect</p>
            <button onClick={() => setSelectedTile(null)}>Cancel</button>
          </div>
        )}
      </main>

      <div className="game-controls">
        <button onClick={loadGameState} className="refresh-btn">
          Refresh
        </button>
        <button onClick={() => {
          setGameState(null);
          setGameId(null);
          setSelectedTile(null);
          setMessage(null);
          setError(null);
        }} className="new-game-btn">
          New Game
        </button>
      </div>
    </div>
  );
}

export default App;
