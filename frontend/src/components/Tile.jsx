import { getPieceSymbol } from '../utils/notation';
import './Tile.css';

function Tile({ tile, x, y, isSelected, isValidMove, onClick }) {
  const { flipped, tile_type, faction } = tile;
  
  // Center tile is always empty
  const isEmpty = tile_type === 'empty';
  
  const tileClasses = [
    'tile',
    faction,
    isSelected && 'selected',
    isValidMove && 'valid-move',
    isEmpty && 'empty-tile'
  ].filter(Boolean).join(' ');

  return (
    <div className={tileClasses} onClick={onClick}>
      {isEmpty ? (
        <div className="empty-marker"></div>
      ) : !flipped ? (
        <div className="tile-back">?</div>
      ) : (
        <div className="tile-piece">
          {/* TODO: Replace with actual images once added */}
          <div className="piece-symbol">{getPieceSymbol(tile_type)}</div>
          <div className="piece-type">{tile_type.replace('_', ' ')}</div>
        </div>
      )}
      
      {isValidMove && <div className="move-indicator">✓</div>}
    </div>
  );
}

export default Tile;
