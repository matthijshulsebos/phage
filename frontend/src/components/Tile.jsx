import PieceArt from './PieceArt';
import './Tile.css';

function Tile({ tile, x, y, isSelected, isValidMove, onClick }) {
  const { flipped, tile_type, faction } = tile;

  // Center tile is always empty
  const isEmpty = tile_type === 'empty';

  const tileClasses = [
    'tile',
    flipped && faction, // Only add faction class if flipped
    flipped && 'flipped', // Add flipped class to enable faction colors
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
        <PieceArt type={tile_type} size={72} />
      )}

      {isValidMove && <div className="move-indicator">+</div>}
    </div>
  );
}

export default Tile;
