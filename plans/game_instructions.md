
# Phage - Game Instructions & Implementation Plan

## Game Overview

"Phage" is a strategic two-player board game set in the human bloodstream. One player controls the immune system (T cells and dendritic cells), while the other controls pathogens (viruses and bacteria). The goal is to eliminate the opponent's cells and score the most points.

## Game Setup

- 2 players required
- Player 1 (Immune System) plays with T cells and dendritic cells
- Player 2 (Pathogens) plays with viruses and bacteria
- 7×7 game board with 48 tiles placed face-down
- Center position (3,3) remains empty

## Game Pieces

### Immune System Team (Player 1)

**T Cell** - 8 pieces, 5 points each
- Specialized cytotoxic cells that target pathogens
- Releases cytotoxins in a fixed direction to neutralize threats
- Can move any number of spaces in straight lines (horizontal or vertical)
- Can only capture in their fixed shooting direction
- Shooting direction cannot be changed once set

**Dendritic Cell** - 2 pieces, 5 points each
- Cleanup cells that remove cellular debris
- Moves only 1 space horizontally or vertically per turn
- Can remove debris obstacles from adjacent spaces
- Cannot attack pathogens directly (only clears debris)

### Pathogen Team (Player 2)

**Virus** - 2 pieces, 10 points each
- Large, aggressive pathogens that attack immune cells
- Moves only 1 space horizontally or vertically per turn
- Can capture T cells and dendritic cells
- Cannot attack other pathogens or red blood cells

**Bacteria** - 6 pieces, 5 points each
- Fast-moving pathogens that infect blood cells
- Can move any number of empty spaces in a straight line
- Captures and infects red blood cells
- Uses hemolysis to damage the bloodstream

### Neutral Pieces (Both Players Can Move)

**Red Blood Cell** - 15 pieces total
- 7 cells worth 2 points each
- 8 cells worth 3 points each
- Can be infected by bacteria or eliminated by T cells
- Both players can move red blood cells strategically
- Represent the battlefield's resources

**Debris** - 15 pieces, 2 points each
- Dead cells and cellular fragments
- Acts as obstacles blocking movement for all pieces
- Cannot be moved by any player
- Can only be removed by dendritic cells
- Clears pathways when removed

## Gameplay

### Turn Actions

On your turn, you must do ONE of the following:
1. **Flip a tile face-up** - Reveal a face-down tile
2. **Move a revealed tile** - Move one of the face-up pieces


### Movement Rules

- Immune system pieces (T cells, dendritic cells) can only be moved by Player 1
- Pathogen pieces (viruses, bacteria) can only be moved by Player 2
- Red blood cells can be moved by both players
- Debris cannot be moved, only removed by dendritic cells
- Most pieces move in straight lines (horizontal or vertical) any number of empty spaces
- Viruses and dendritic cells move only 1 space per turn
- A piece cannot return to its previous position on the next turn
- A red blood cell that was revealed or moved by the opponent cannot be moved on the immediately following turn

### Capturing

To capture a piece, move your piece onto the target's tile following movement rules:

**Immune System captures:**
- T cells eliminate viruses, bacteria, and infected red blood cells (only in shooting direction)
- Dendritic cells remove debris from adjacent spaces

**Pathogen captures:**
- Viruses attack and destroy T cells and dendritic cells
- Bacteria infect and capture red blood cells

### Special Rules

**T Cell Shooting Mechanism:**
- Each T cell has a fixed shooting direction (north, south, east, or west)
- Can move freely in any direction
- Can only capture targets in their shooting direction
- Direction cannot be changed during the game

**Red Blood Cell Restrictions:**
- If opponent reveals a red blood cell, you cannot move it on your next turn
- If opponent moves a red blood cell, you cannot move that same cell on your next turn
- This prevents rapid back-and-forth control

**Debris Removal:**
- Dendritic cells can remove debris from any adjacent space (not diagonal)
- Removing debris scores points and clears pathways
- Multiple debris pieces can be removed if adjacent

## End Game Phase

### Triggering End Game

When the last tile is flipped face-up, the game enters the Escape Phase. Each player gets exactly 5 more turns.

### Bloodstream Exits

During the final 5 turns, players can move their own pieces to one of the 4 bloodstream exit points to remove them from the board and secure their points:
- North exit: position (3, 0)
- East exit: position (6, 3)
- South exit: position (3, 6)
- West exit: position (0, 3)

Pieces that exit cannot be captured and their points are secured.

## Game End & Scoring

### Game Ends When:
1. Both players have completed 5 turns after the last tile was revealed, OR
2. All tiles are revealed AND one player has no pieces remaining on the board

### Scoring:
- **Virus:** 10 points each
- **T Cell:** 5 points each
- **Dendritic Cell:** 5 points each
- **Bacteria:** 5 points each
- **Red Blood Cell (3pt):** 3 points each
- **Red Blood Cell (2pt):** 2 points each
- **Debris:** 2 points each

### Winner:
- Player with the most points wins
- Tiebreaker: Player who captured or removed the most tiles from the board wins

### Tournament Play:
For balanced competition, play two games where players switch sides. The player with the highest combined score across both games wins the match.

## Implementation Plan

### Phase 1: Core Game Logic ✓
- ✓ Game board representation (7×7 grid)
- ✓ Tile system (face-up/face-down states)
- ✓ All piece types with movement rules implemented
- ✓ Turn-based system
- ✓ Capture mechanics
- ✓ Point calculation

### Phase 2: Movement System ✓
- ✓ Valid move calculation for each piece type
- ✓ T cell shooting direction logic
- ✓ Movement restrictions (1-space for virus/dendritic cell)
- ✓ Straight line movement validation
- ✓ Obstacle detection (debris)
- ✓ Previous position tracking (no immediate return)
- ✓ Red blood cell movement restrictions

### Phase 3: User Interface
- [ ] Game board visualization
- [ ] Tile flip functionality (UI)
- [ ] Piece movement interface
- [ ] Valid move highlighting
- [ ] Player turn indicator
- [ ] Score display
- [ ] Remaining turns counter (end game)

### Phase 4: End Game Features ✓
- ✓ Last tile detection
- ✓ Final 5 turns countdown
- ✓ Bloodstream exit system (4 exits)
- ✓ Piece removal functionality
- ✓ End game scoring
- ✓ Winner determination
- [ ] Two-round match system (UI)

### Phase 5: Game Rules Enforcement ✓
- ✓ Turn validation
- ✓ Capture validation based on piece types
- ✓ Movement range validation
- ✓ Shooting direction validation for T cells
- ✓ Red blood cell movement blocking
- ✓ Early game end condition check

---

## Quick Reference Card

**Immune System Captures:**
- T Cell → Viruses, Bacteria, Red Blood Cells (in shooting direction only)
- Dendritic Cell → Debris (adjacent spaces)

**Pathogen Captures:**
- Virus → T Cells & Dendritic Cells
- Bacteria → Red Blood Cells

**Movement:**
- Virus & Dendritic Cell: 1 space only (horizontal or vertical)
- T Cell, Bacteria, Red Blood Cell: Any number of spaces in straight line
- Debris: Cannot move (blocks all pieces)

**Points:**
- Virus: 10 pts
- T Cell, Dendritic Cell, Bacteria: 5 pts each
- Red Blood Cell (large): 3 pts
- Red Blood Cell (small), Debris: 2 pts each
