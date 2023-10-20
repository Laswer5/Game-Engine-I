from enum import Enum
#responsibility: handle IO for a menu and instruct calling class what option was chosen
#could be generalized to handle any menu and have its contents supplied from somewhere else
class menuOption(Enum):
    play1v1 = 1
    playComp = 2
    showTutorial = 3
    quit = 4
class MenuRunner:
    def __init__(self) -> None:
        pass
    
    def run(self) -> menuOption:
        """Runs the main menu

        Returns:
            menuOption: the option chosen
        """
        while(True):
            print("Choose an option")
            print("1: Play 1v1 locally")
            print("2: Play against the computer")
            print("3: Show tutorial")
            print("4: Quit")
            try:
                option:int = int(input())
                if 0 < option <= 4:
                    return menuOption(option)
                else:
                    print("Inputted value is not a valid option, try again")
            except:
                print("Inputted value is not a valid option, try again")