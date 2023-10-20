from gameEngine import GameEngine, GameOver, InputRequest
from iohandler import IOHandler
from menuRunner import MenuRunner, menuOption
from tutorialtext import Tutorial

class Game:
    def __init__(self) -> None:
        self._engine :GameEngine = GameEngine()
        self._input:IOHandler = IOHandler()
        self._menurunner:MenuRunner = MenuRunner()
    
    def run(self):
        """Runs the actual game
        """
        while True:
            op = self._menurunner.run()
            
            match op:
                case menuOption.play1v1:
                    self._run1v1()
            
                case menuOption.playComp:
                    print("Not implemented yet")

                case menuOption.showTutorial:
                    Tutorial.runTutorial()
                    
                case menuOption.quit:
                    return
                
    def _run1v1(self):
        """Runs a 1v1 game
        """
        lastInput = self._input.getInput(InputRequest.get_first_inputRequest(),self._engine)
        
        while True:
            request = self._engine.run(lastInput)
        
            if type(request) is GameOver:
                self._input.displayWinner(request)
                break
        
            else:
                lastInput = self._input.getInput(request,self._engine)
        
        self._engine = GameEngine()
        self._input = IOHandler()
        
