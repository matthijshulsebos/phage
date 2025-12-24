import { useState, useEffect } from 'react';
import './GameBoard.css';
import Tile from './Tile';

function GameBoard({ boardState, onTileClick, selectedTile, validMoves }) {
  const boardSize = 7;

  return (
    <div className="game-board">
      <div className="board-coordinates top">
        {Array.from({ length: boardSize }, (_, i) => (
          <div key={i} className="coord-label">
            {String.fromCharCode(97 + i)}
          </div>
        ))}
      </div>
      
      <div className="board-container">
        <div className="board-coordinates left">
          {Array.from({ length: boardSize }, (_, i) => (
            <div key={i} className="coord-label">
              {boardSize - i}
            </div>
          ))}
        </div>

        <div className="board-grid">
          {boardState.map((row, y) => (
            <div key={y} className="board-row">
              {row.map((tile, x) => {
                const isSelected = selectedTile && 
                  selectedTile.x === x && selectedTile.y === y;
                const isValidMove = validMoves?.some(
                  move => move.x === x && move.y === y
                );
                
                return (
                  <Tile
                    key={`${x}-${y}`}
                    tile={tile}
                    x={x}
                    y={y}
                    isSelected={isSelected}
                    isValidMove={isValidMove}
                    onClick={() => onTileClick(x, y, tile)}
                  />
                );
              })}
            </div>
          ))}
        </div>

        <div className="board-coordinates right">
          {Array.from({ length: boardSize }, (_, i) => (
            <div key={i} className="coord-label">
              {boardSize - i}
            </div>
          ))}
        </div>
      </div>

      <div className="board-coordinates bottom">
        {Array.from({ length: boardSize }, (_, i) => (
          <div key={i} className="coord-label">
            {String.fromCharCode(97 + i)}
          </div>
        ))}
      </div>
    </div>
  );
}

export default GameBoard;
