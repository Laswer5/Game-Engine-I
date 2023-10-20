from enum import Enum
import re
class InputType(Enum):
    place = 0
    move = 1
    destroy = 2
    
class Input:
    _valid_inputs: list[str] = ['a1','d1','g1','b2','d2','f2','c3','d3','e3','a4','b4','c4','e4','f4','g4','d5','c5','e5','f6','d6','b6','g7','d7','a7']
    def __init__(self, s: str,type:InputType) -> None:
        """parses and builds an input, throws an exception if s is malformed

        Args:
            s (str): a string representing an input
            type (InputType): what type of input is requested 
        """
        self._type = type
        self._place1, self._place2 = None, None
        match type:
            case InputType.place:
                self._place1 = Input.parsePlace(s)
            case InputType.move:
                self._place1,self._place2 = Input.parseMove(s)
            case InputType.destroy:
                self._place1 = Input.parsePlace(s)
    
    def getType(self):
        return self._type
    
    def getFirstArgument(self):
        return self._place1
    def getSecondArgument(self):
        return self._place2
    
    def parsePlace(s:str):
        #finds all instances of a valid letter and digit
        res = re.findall(r"[a-g]\d",s)
        if len(res) > 1:
            raise ValueError("Cannot have more than 1 argument when placing")
        if len(res) < 1:
            raise ValueError("Missing argument")
        if res[0] not in Input._valid_inputs:
            raise ValueError("Argument is invalid")
        
        return res[0]
        
    def parseMove(s:str):
        res = re.findall(r"[a-g]\d",s)
        if len(res) > 2:
            raise ValueError("Cannot have more than 2 arguments when placing")
        if len(res) < 2:
            raise ValueError("Missing argument")
        if res[0] not in Input._valid_inputs or res[1] not in Input._valid_inputs:
            raise ValueError("Argument is invalid")
        
        
        return res[0], res[1]
        
        