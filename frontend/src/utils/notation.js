// Chess-like notation for Phage game moves
// Board uses columns a-g and rows 1-7

const PIECE_SYMBOLS = {
  't_cell': 'T',
  'dendritic_cell': 'D',
  'virus': 'V',
  'bacteria': 'B',
  'red_blood_cell': 'R',
  'debris': '▓'
};

const DIRECTION_SYMBOLS = {
  'NORTH': '↑',
  'SOUTH': '↓',
  'EAST': '→',
  'WEST': '←'
};

/**
 * Convert board coordinates (0-6, 0-6) to chess notation (a1-g7)
 * @param {number} x - Column index (0-6)
 * @param {number} y - Row index (0-6)
 * @returns {string} Position in chess notation (e.g., "c3")
 */
export function coordToNotation(x, y) {
  const column = String.fromCharCode(97 + x); // 97 = 'a'
  const row = (y + 1).toString();
  return column + row;
}

/**
 * Convert chess notation to board coordinates
 * @param {string} notation - Position in chess notation (e.g., "c3")
 * @returns {{x: number, y: number}} Board coordinates
 */
export function notationToCoord(notation) {
  const column = notation.charCodeAt(0) - 97; // 'a' = 0
  const row = parseInt(notation[1]) - 1;
  return { x: column, y: row };
}

/**
 * Generate move notation
 * @param {string} pieceType - Type of piece
 * @param {object} from - Starting position {x, y}
 * @param {object} to - Ending position {x, y}
 * @param {boolean} isCapture - Whether this is a capture move
 * @param {boolean} isDebrisRemoval - Whether this is debris removal
 * @param {boolean} isEscape - Whether this is an escape
 * @param {string} shootDirection - Direction for shooting (if applicable)
 * @returns {string} Move in chess notation
 */
export function formatMove(pieceType, from, to, options = {}) {
  const { 
    isCapture = false, 
    isDebrisRemoval = false, 
    isEscape = false,
    shootDirection = null
  } = options;
  
  const pieceSymbol = PIECE_SYMBOLS[pieceType] || '?';
  const fromNotation = coordToNotation(from.x, from.y);
  
  if (isDebrisRemoval) {
    return `${pieceSymbol}${fromNotation}*`;
  }
  
  if (isEscape) {
    return `${pieceSymbol}${fromNotation}!`;
  }
  
  if (shootDirection) {
    const dirSymbol = DIRECTION_SYMBOLS[shootDirection] || shootDirection;
    const toNotation = to ? coordToNotation(to.x, to.y) : '';
    return `${pieceSymbol}${fromNotation}${dirSymbol}${isCapture ? 'x' : ''}${toNotation}`;
  }
  
  const toNotation = coordToNotation(to.x, to.y);
  const captureSymbol = isCapture ? 'x' : '-';
  
  return `${pieceSymbol}${fromNotation}${captureSymbol}${toNotation}`;
}

/**
 * Parse move notation back to action
 * @param {string} notation - Move in chess notation
 * @returns {object} Parsed move details
 */
export function parseMove(notation) {
  // TODO: Implement parsing if needed for game replay
  return null;
}

/**
 * Get piece symbol for display
 * @param {string} pieceType - Type of piece
 * @returns {string} Single character symbol
 */
export function getPieceSymbol(pieceType) {
  return PIECE_SYMBOLS[pieceType] || '?';
}
