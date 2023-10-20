from enum import Enum
from input import Input, InputType
from board import Board, Piece

class GameOver(Enum):
    draw = 0
    p1win = 1
    p2win = 2
    
    
class InputRequest:
    """Immutable record of what input is requested by the GameEngine
    """
    def __init__(self,player: int, type: InputType) -> None:
        self._player = player
        self._type = type
        
    def get_player(self):
        return self._player
    
    def get_type(self):
        return self._type
    
    
    def get_first_inputRequest():
        return InputRequest(1,InputType.place)
    
class GameEngine:
    """An engine that runs the game and takes care of all the logic
    """
    def __init__(self) -> None:
        self._board = Board()
        self._turn = 1
        self._p1pieces = 12
        self._p2pieces = 12
        self._requested_type = InputType.place
        self._p1_broken_mill_square:str = None
        self._p2_broken_mill_square:str = None
        self._p1_broken_mill: list[tuple[str,str,str]] = None
        self._p2_broken_mill: list[tuple[str,str,str]] = None
        self._turn_no:int = 0
        
    
    
    def run(self,input:Input) -> InputRequest | GameOver:
        """Updates the gamestate according to an input, will return when game is over

        Args:
            input (Input): an input given by the player

        Returns:
            InputRequest: what input the gameEngine expects next
        """
        #this function is big and ugly, but noone but us should have to touch it so it's fine
        
        requested_type = None #this one will change as the function runs
        self._turn_no += 1
        if self._turn_no > 200:
            return GameOver.draw
        
        if input.getType() != self._requested_type:
            raise ValueError("Invalid input type")
        
        match input.getType():
            case InputType.place:
                target = self._board.get_piece(input.getFirstArgument())
                if target != Piece.unoccupied:
                    raise ValueError("Invalid place")
                
                self._board.set_piece(
                    input.getFirstArgument(),
                    Piece.fromPlayer(self._turn))
                
                if self._board.has_mill(input.getFirstArgument()):
                    requested_type = InputType.destroy
                
                if self._turn == 1:
                    self._p1pieces -= 1
                else:
                    self._p2pieces -= 1
                    
                if self._p1pieces == 0 and self._p2pieces == 0 and len([v for (k,v) in self._board.get_squares_list() if v != Piece.unoccupied])==0:
                    return GameOver.p2win
                    
                    
            case InputType.destroy:
                piece = self._board.get_piece(input.getFirstArgument())
                valid_target = Piece.p2 if self._turn == 1 else Piece.p1
                 
                if piece != valid_target:
                    raise ValueError("Invalid piece")
                p = Piece.unoccupied
                
                if(self._board.has_mill(input.getFirstArgument())):
                    #checks that all valid targets are mills if the target is in a mill
                    if not all(list(map(lambda x: self._board.has_mill(x),[k for (k,v) in self._board.get_squares_list() if v == valid_target]))):
                        raise ValueError("Attempting to remove mill when not appropriate")
                    
                self._board.set_piece(
                    input.getFirstArgument(),
                    p)
                    
                
            case InputType.move:
                piece_from = self._board.get_piece(input.getFirstArgument())
                piece_to   = self._board.get_piece(input.getSecondArgument())
                adjacency = self._board.get_adjacency_list()
                  
                if  piece_from != Piece.fromPlayer(self._turn)  or piece_to != Piece.unoccupied:
                    raise ValueError("Invalid move")
                
                if  input.getSecondArgument()  not in adjacency[input.getFirstArgument()] and self._board.count_pieces(Piece.fromPlayer(self._turn)) > 3:
                    raise ValueError("invalid move")
                
                shouldunban = False
                
                if self._turn == 1:
                    if input.getFirstArgument() == self._p1_broken_mill_square:
                        self._board.ban_mills(self._p1_broken_mill)
                        shouldunban = True
                else:
                    if input.getFirstArgument() == self._p2_broken_mill_square:
                        self._board.ban_mills(self._p2_broken_mill)
                        shouldunban = True
                
                broken_mill_delayed = None
                broken_mill_square_delayed = None
                                
                if self._board.has_mill(input.getFirstArgument()):
                    broken_mill_square_delayed = input.getSecondArgument()
                    broken_mill_delayed = self._board.get_mills(input.getFirstArgument())
                
                self._board.set_piece(
                    input.getFirstArgument(),
                    Piece.unoccupied)
                self._board.set_piece(
                    input.getSecondArgument(),
                    Piece.fromPlayer(self._turn))
                if self._board.has_mill(input.getSecondArgument()):
                    requested_type = InputType.destroy
                
                if self._turn == 1:
                    if shouldunban:
                        self._board.unban_mills(self._p1_broken_mill)
                    self._p1_broken_mill = broken_mill_delayed
                    self._p1_broken_mill_square = broken_mill_square_delayed
                    
                else:
                    if shouldunban:
                        self._board.unban_mills(self._p2_broken_mill)
                    self._p2_broken_mill = broken_mill_delayed
                    self._p2_broken_mill_square = broken_mill_square_delayed
                
        if requested_type == None:
            if self._turn == 1:
                if self._p2pieces > 0:
                    requested_type = InputType.place
                else:
                    requested_type = InputType.move
            else:
                if self._p1pieces > 0:
                    requested_type = InputType.place
                else:
                    requested_type = InputType.move
        
        
        
        if self._board.count_pieces(Piece.fromPlayer(1 if self._turn == 2  else 2)) + (self._p1pieces if self._turn == 2 else self._p2pieces) < 3:
            if self._turn == 1:
                return GameOver.p1win
            if self._turn == 2:
                return GameOver.p2win
        
        if requested_type != InputType.destroy:        
            self._turn = (2 if self._turn == 1 else 1)
            
        if requested_type == InputType.move:
            adjacency = self._board.get_adjacency_list()
            # produces a flat list of adjacent squares of every square the player has with only unique elements
            adjacent_player_pieces = [adjacency[k] for (k,v) in self._board.get_squares_list() if v == Piece.fromPlayer(self._turn)]
            adjacent_player_pieces = list(set([j for sub in adjacent_player_pieces for j in sub])) 
            can_not_move = all([self._board.get_piece(p) != Piece.unoccupied for p in adjacent_player_pieces])
            
            if can_not_move:
                if self._turn == 1:
                    return GameOver.p2win
                else:
                    return GameOver.p1win
            
        self._requested_type = requested_type
        
        
        return InputRequest(self._turn,requested_type) 
    
    def is_valid_move(self,input:Input) -> bool:
        match self._requested_type:
            case InputType.move:       
                piece_from = self._board.get_piece(input.getFirstArgument())
                piece_to   = self._board.get_piece(input.getSecondArgument())
                adjacency = self._board.get_adjacency_list()         
                if  piece_from != Piece.fromPlayer(self._turn)  or piece_to != Piece.unoccupied:
                    return False
                
                if  input.getSecondArgument()  not in adjacency[input.getFirstArgument()] and self._board.count_pieces(Piece.fromPlayer(self._turn)) > 3:
                    return False
            case InputType.place:
                target = self._board.get_piece(input.getFirstArgument())
                if target != Piece.unoccupied:
                    return False
            case InputType.destroy:
                piece = self._board.get_piece(input.getFirstArgument())
                valid_target = Piece.p2 if self._turn == 1 else Piece.p1
                
                if(self._board.has_mill(input.getFirstArgument())):
                    if not all(list(map(lambda x: self._board.has_mill(x),[k for (k,v) in self._board.get_squares_list() if v == valid_target]))):
                        return False
                 
                if piece != valid_target:
                    return False
                
        return True
    
    def should_warn_about_mill(self, input:Input)->bool:
        """Checks if a move may be trying to recreate a mill that cannot be recreated yet

        Args:
            input (Input): a move 

        Returns:
            bool: True if move recreates a mill too early
        """
        if input.getType() != InputType.move:
            raise ValueError("Input must have type be move")

        print(f"input: {input.getFirstArgument()}, {input.getSecondArgument()}")
        if self._turn == 1:
            print(f"broken mill square and mill: {self._p1_broken_mill_square}, {self._p1_broken_mill}")
            if input.getFirstArgument() == self._p1_broken_mill_square and any([input.getSecondArgument() in mill for mill in self._p1_broken_mill]):
                return True
        else:
            print(f"broken mill square and mill: {self._p2_broken_mill_square}, {self._p2_broken_mill}")
            if input.getFirstArgument() == self._p2_broken_mill_square and any([input.getSecondArgument() in mill for mill in self._p1_broken_mill]):
                return True
        
        return False
            
        
    def get_p1_on_board_pieces(self) -> int:
        return len([v for (k,v) in self._board.get_squares_list() if v ==Piece.p1])
    
    def get_p2_on_board_pieces(self) -> int:
        return len([v for (k,v) in self._board.get_squares_list() if v ==Piece.p2])
    
    def get_valid_moves(self) -> list[Input]:
        return []
    
    def get_board(self):
        return self._board
    
    def get_p1_pieces(self):
        return self._p1pieces
    def get_p2_pieces(self):
        return self._p2pieces
    
    def get_turn(self):
        return self._turn