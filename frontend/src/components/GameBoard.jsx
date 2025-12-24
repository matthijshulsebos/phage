import './GameBoard.css';
import Tile from './Tile';

function GameBoard({ boardState, onTileClick, onExitClick, selectedTile, validMoves, disabled, showExits }) {
  const boardSize = 7;
  const boardClassName = disabled ? 'game-board disabled' : 'game-board';

  // Exit positions (outside the board)
  const exits = {
    north: { x: 3, y: -1 },
    east: { x: 7, y: 3 },
    south: { x: 3, y: 7 },
    west: { x: -1, y: 3 },
  };

  const canClickExit = showExits && selectedTile && !disabled;

  return (
    <div className={boardClassName}>
      {/* North exit */}
      <div className="exit-row top">
        <div className="exit-spacer"></div>
        {Array.from({ length: boardSize }, (_, i) => (
          <div
            key={i}
            className={`exit-cell ${i === 3 && showExits ? 'exit-active' : ''} ${i === 3 && canClickExit ? 'exit-clickable' : ''}`}
            onClick={() => i === 3 && canClickExit && onExitClick(exits.north.x, exits.north.y)}
          >
            {i === 3 && showExits && <span className="exit-marker">EXIT</span>}
          </div>
        ))}
        <div className="exit-spacer"></div>
      </div>

      <div className="board-middle">
        {/* West exit */}
        <div className="exit-column">
          {Array.from({ length: boardSize }, (_, i) => (
            <div
              key={i}
              className={`exit-cell ${i === 3 && showExits ? 'exit-active' : ''} ${i === 3 && canClickExit ? 'exit-clickable' : ''}`}
              onClick={() => i === 3 && canClickExit && onExitClick(exits.west.x, exits.west.y)}
            >
              {i === 3 && showExits && <span className="exit-marker">EXIT</span>}
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
                    key={x + '-' + y}
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

        {/* East exit */}
        <div className="exit-column">
          {Array.from({ length: boardSize }, (_, i) => (
            <div
              key={i}
              className={`exit-cell ${i === 3 && showExits ? 'exit-active' : ''} ${i === 3 && canClickExit ? 'exit-clickable' : ''}`}
              onClick={() => i === 3 && canClickExit && onExitClick(exits.east.x, exits.east.y)}
            >
              {i === 3 && showExits && <span className="exit-marker">EXIT</span>}
            </div>
          ))}
        </div>
      </div>

      {/* South exit */}
      <div className="exit-row bottom">
        <div className="exit-spacer"></div>
        {Array.from({ length: boardSize }, (_, i) => (
          <div
            key={i}
            className={`exit-cell ${i === 3 && showExits ? 'exit-active' : ''} ${i === 3 && canClickExit ? 'exit-clickable' : ''}`}
            onClick={() => i === 3 && canClickExit && onExitClick(exits.south.x, exits.south.y)}
          >
            {i === 3 && showExits && <span className="exit-marker">EXIT</span>}
          </div>
        ))}
        <div className="exit-spacer"></div>
      </div>
    </div>
  );
}

export default GameBoard;
