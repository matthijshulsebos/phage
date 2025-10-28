# De beer is los! - Game Instructions & Implementation Plan

## Game Overview

"De beer is los!" is a strategic two-player board game set in a forest. One player controls hunters and lumberjacks, while the other controls bears and foxes. The goal is to capture the opponent's pieces and score the most points.

## Game Setup

- 2 players required
- Player 1 (brown) plays with hunters and lumberjacks
- Player 2 (blue) plays with bears and foxes

## Game Pieces

### Hunter Team (Brown Player)

**Lumberjack** - 5 points
- Can capture all trees
- Moves only 1 space horizontally or vertically per turn

**Hunter** - 5 points
- Captures all animals (bears, foxes, pheasants, and ducks) but only in shooting direction
- Shooting direction cannot be changed (gun barrel determines capture direction)
- Can move in all directions, but can only capture in the direction the gun points

### Animal Team (Blue Player)

**Bear** - 10 points
- Captures hunters and lumberjacks (not other animals)
- Moves only 1 space horizontally or vertically per turn

**Fox** - 5 points
- Captures pheasants and ducks
- Can move any number of empty spaces in a straight line

### Neutral Pieces (Green - Both Players Can Move)

**Duck** - 2 points
- Can be captured by foxes and hunters
- Both players can move ducks

**Pheasant** - 3 points
- Can be captured by foxes and hunters
- Both players can move pheasants

**Tree** - 2 points
- Can be chopped down by lumberjacks
- Acts as obstacle for all other pieces (cannot pass through)
- Cannot be moved, only captured

## Gameplay

### Turn Actions

On your turn, you must do ONE of the following:
1. **Flip a tile face-up** - Reveal a face-down tile
2. **Move a revealed tile** - Move one of the face-up pieces

### Movement Rules

- Brown cards can only be moved by the brown player
- Blue cards can only be moved by the blue player
- Green cards (pheasants and ducks) can be moved by both players
- Trees cannot be moved, only captured by lumberjacks
- Pieces move in a straight line (up, down, left, or right) over any number of empty spaces (except bear and lumberjack: 1 space only)
- A piece cannot return to its previous position on the next turn
- A green card that was revealed or moved by the opponent cannot be moved immediately after

### Capturing

To capture a piece, move your piece according to movement rules onto the tile of the piece to be captured:
- Fox captures pheasants and ducks
- Hunter captures all animals (in shooting direction only)
- Bear captures hunters and lumberjacks
- Lumberjack captures trees

## End Game Phase

### Triggering End Game

When the last tile is flipped face-up, each player gets exactly 5 more turns.

### Forest Exits

During the final 5 turns, players can move their own pieces through the 4 forest exits (marked with arrows) to remove them from the board and score points.

## Game End & Scoring

### Game Ends When:
1. 5 rounds after the last tile is revealed, OR
2. All tiles are revealed AND one player has no pieces left on the board

### Scoring:
- Bear: 10 points
- Lumberjack: 5 points
- Hunter: 5 points
- Fox: 5 points
- Pheasant: 3 points
- Duck: 2 points
- Tree: 2 points

### Winner:
- Player with the most points wins
- Tiebreaker: Player who captured or removed the most tiles from the board wins

### Standard Play:
Normally, the game is played in two rounds so both players get to play with both the humans and the animals.

## Implementation Plan

### Phase 1: Core Game Logic
- [ ] Game board representation
- [ ] Tile system (face-up/face-down states)
- [ ] Piece types with movement rules
- [ ] Turn-based system
- [ ] Capture mechanics
- [ ] Point calculation

### Phase 2: Movement System
- [ ] Valid move calculation for each piece type
- [ ] Hunter shooting direction logic
- [ ] Movement restrictions (1-space for bear/lumberjack)
- [ ] Straight line movement (up, down, left, right)
- [ ] Obstacle detection (trees)
- [ ] Previous position tracking (no immediate return)
- [ ] Green card movement restrictions

### Phase 3: User Interface
- [ ] Game board visualization
- [ ] Tile flip functionality
- [ ] Piece movement interface
- [ ] Valid move highlighting
- [ ] Player turn indicator
- [ ] Score display
- [ ] Remaining turns counter (end game)

### Phase 4: End Game Features
- [ ] Last tile detection
- [ ] Final 5 turns countdown
- [ ] Forest exit system (4 exits with arrows)
- [ ] Piece removal functionality
- [ ] End game scoring
- [ ] Winner determination
- [ ] Two-round match system

### Phase 5: Game Rules Enforcement
- [ ] Turn validation
- [ ] Capture validation based on piece types
- [ ] Movement range validation
- [ ] Shooting direction validation for hunters
- [ ] Green card movement blocking
- [ ] Early game end condition check

---

## Quick Reference Card

**Captures:**
- Lumberjack → Trees
- Hunter → All animals (in shooting direction)
- Bear → Hunters & Lumberjacks
- Fox → Ducks & Pheasants

**Movement:**
- Bear & Lumberjack: 1 space only (horizontal or vertical)
- All others: Any number of empty spaces in a straight line
- Trees block movement

**Points:**
- Bear: 10 pts
- Hunter, Lumberjack, Fox: 5 pts each
- Pheasant: 3 pts
- Duck, Tree: 2 pts each
