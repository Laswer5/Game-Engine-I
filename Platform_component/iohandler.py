import sys
from gameEngine import InputRequest, GameEngine, InputType, GameOver
from BoardRenderer import BoardRenderer
from input import Input
from tutorialtext import Tutorial

class IOHandler:
    def __init__(self) -> None:
        self._renderer = None
        self._last_move_type = None
        self._p1_phase = 1
        self._p2_phase = 1
        pass
    
    def displayWinner(self, gameover: GameOver):
        match gameover:
            case GameOver.p1win:
                print("player 1 has won")
            case GameOver.p2win:
                print("player 2 has won")
            case GameOver.draw:
                print("draw")
    
    def _phase_shift_alert(self, gameState:GameEngine):
        turn = gameState.get_turn()
        if turn == 1:
            if gameState.get_p1_pieces() == 0 and  self._p1_phase == 1:
                self._p1_phase = 2
                print("Now entering phase 2 for player 1")
            if gameState.get_p1_on_board_pieces() == 3 and self._p1_phase == 2:
                self._p1_phase = 3
                print("Now entering phase 3 for player 1")
                
        elif turn == 2:
            if gameState.get_p2_pieces() == 0 and  self._p2_phase == 1:
                self._p2_phase = 2
                print("Now entering phase 2 for player 2")
            if gameState.get_p1_on_board_pieces() == 3 and self._p2_phase == 2:
                self._p2_phase = 3
                print("Now entering phase 3 for player 2")
    
    def _print_pieces_left(self,gameState:GameEngine):
        match self._p1_phase:
            case 1:
                print(f"Pieces player 1 has left to place:{gameState.get_p1_pieces()}")
            case 2:
                print(f"Pieces player 1 has left on board:{gameState.get_p1_on_board_pieces()}")
            case 3:
                print(f"Player player 1 has left on board: 3")
        match self._p2_phase:
            case 1:
                print(f"Pieces player 2 has left to place:{gameState.get_p2_pieces()}")
            case 2:
                print(f"Pieces player 2 has left on board:{gameState.get_p2_on_board_pieces()}")
            case 3:
                print(f"Player player 2 has left on board: 3")
            
                
    def getInput(self,inputRequest: InputRequest, gameState: GameEngine) -> Input:
        """Gets input from the user

        Args:
            inputRequest (InputRequest): The input requested
            gameState (GameEngine): The gameEngine

        Returns:
            Input: The input given by the player
        """
        turn = gameState.get_turn()
        
        self._phase_shift_alert(gameState)
        
        if self._renderer == None:        
            self._renderer = BoardRenderer()
        isvalid = False
        while(not isvalid):
            try:
                
                if self._last_move_type == InputType.destroy and inputRequest.get_type() != InputType.destroy:
                    print(f"player {turn} lost a piece")
                
                self._renderer.render(gameState,inputRequest.get_type() == InputType.destroy)
                turn = gameState.get_turn()
                self._print_pieces_left(gameState)
                print(f"Player {turn}s turn:")
                match inputRequest.get_type():
                    case InputType.place:
                        print("Select a location to place the piece")
                        a = input()
                    case InputType.move:
                        print("Select a location to move a piece from and to(format: xn yk where x, y are rows and n and k are collumns)")
                        a = input()
                    case InputType.destroy:
                        print("Select a Piece to destroy")
                        a = input()
                if a == '-q':
                    sys.exit(0)
                if a == '-h':
                    Tutorial.runTutorial()
                    continue
                input_val = Input(a,inputRequest.get_type())
                if inputRequest.get_type() == InputType.move:
                    if gameState.should_warn_about_mill(input_val):
                        ans = ""
                        while ans not in ["y","n"]:
                            print("You may be trying to form a mill that cannot be re-formed yet")
                            print("To reform the mill you must wait an another turn")
                            print("Do you wish to make the move anyways?(y/n)")

                            ans = input()
                            
                        if ans == "n":
                            continue
                        
                if not gameState.is_valid_move(input_val):
                    print("Input was not a valid move, try again")
                    continue
                
                self._last_move_type = inputRequest.get_type()
                return input_val
                
            except ValueError as e:
                print("Something went wrong, try again")