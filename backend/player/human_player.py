from player.player import Player
from pieces.piece_owner import PieceOwner
from common.models.action import Action, ActionType
from common.models.coordinate import Coord
from common.models.direction import Direction


class HumanPlayer(Player):
    def __init__(self, name: str, faction: PieceOwner = None):
        super().__init__(name, faction)

    def choose_action(self, game_engine):
        """Prompt the human player for an action."""
        print(f"\n{self.name}'s turn (Phase: {game_engine.phase.name})")
        print(f"Score: {game_engine.scores[self.name]}")
        
        # Show available actions based on game phase
        if game_engine.phase.name == "FLIP":
            print("Actions: [F]lip tile, [M]ove piece")
        else:
            print("Actions: [M]ove piece, [S]hoot (hunters), [C]ut tree (lumberjacks)")
        
        while True:
            try:
                action_input = input("Choose action (F/M/S/C): ").upper().strip()
                
                if action_input == 'F':
                    return self._choose_flip_action(game_engine)
                elif action_input == 'M':
                    return self._choose_move_action(game_engine)
                elif action_input == 'S':
                    return self._choose_shoot_action(game_engine)
                elif action_input == 'C':
                    return self._choose_cut_action(game_engine)
                else:
                    print("Invalid action. Try again.")
                    
            except (ValueError, KeyboardInterrupt) as e:
                print("Invalid input. Try again.")
    
    def _choose_flip_action(self, game_engine):
        """Choose a tile to flip."""
        print("Choose coordinates to flip (e.g., '2 3'):")
        try:
            x, y = map(int, input().split())
            target = Coord(x, y)
            
            # Validate flip action
            tile = game_engine.board.get_tile(target)
            if not tile:
                print("No tile at that position!")
                return self.choose_action(game_engine)
            if tile.flipped:
                print("Tile already flipped!")
                return self.choose_action(game_engine)
                
            return Action(ActionType.FLIP, target=target)
            
        except (ValueError, IndexError):
            print("Invalid coordinates!")
            return self.choose_action(game_engine)
    
    def _choose_move_action(self, game_engine):
        """Choose a piece to move."""
        print("Choose piece to move (e.g., '2 3') and destination (e.g., '4 5'):")
        print("Format: 'from_x from_y to_x to_y'")
        try:
            from_x, from_y, to_x, to_y = map(int, input().split())
            source = Coord(from_x, from_y)
            target = Coord(to_x, to_y)
            
            # Basic validation
            from_tile = game_engine.board.get_tile(source)
            if not from_tile:
                print("No piece at source position!")
                return self.choose_action(game_engine)
                
            return Action(ActionType.MOVE, source=source, target=target)
            
        except (ValueError, IndexError):
            print("Invalid coordinates!")
            return self.choose_action(game_engine)
    
    def _choose_shoot_action(self, game_engine):
        """Choose shooting action for hunters."""
        print("Choose hunter position to shoot from (e.g., '2 3'):")
        try:
            x, y = map(int, input().split())
            source = Coord(x, y)
            
            return Action(ActionType.SHOOT, target=source)
            
        except (ValueError, IndexError):
            print("Invalid coordinates!")
            return self.choose_action(game_engine)
    
    def _choose_cut_action(self, game_engine):
        """Choose tree to cut for lumberjacks."""
        print("Choose lumberjack position to cut from (e.g., '2 3'):")
        try:
            x, y = map(int, input().split())
            source = Coord(x, y)
            
            return Action(ActionType.CUT, target=source)
            
        except (ValueError, IndexError):
            print("Invalid coordinates!")
            return self.choose_action(game_engine)