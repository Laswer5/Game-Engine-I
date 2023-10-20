from board import Board, Piece
from gameEngine import GameEngine
class BoardRenderer:
    def __init__(self) -> None:
        j = 2
        l = ['X','O','*','P','M']
        while j>0:
            print("Choose a symbol")
            for (i,k) in enumerate(l):
                print(f"{i}:{k}")
            try:
                a = int(input())
                if j == 2:
                    self._p1sym = l[a]
                elif j == 1:
                    self._p2sym = l[a]
                
                j-=1
                l.pop(a)
                
            except Exception:
                print("something went wrong")
        print("To make a move, write the coordinates for the corresponding intersection point (i.e 'a1' or 'e4') and press ENTER.")
                
    def render(self,gameState:GameEngine,destruction:bool):
        #internal function used to make rendering symbols easier
        board = gameState.get_board()
        valid_target = Piece.p2 if gameState.get_turn() == 1 else Piece.p1
        only_mills = all(list(map(lambda x: board.has_mill(x),[k for (k,v) in board.get_squares_list() if v == valid_target])))
        def convert_to_symbol(location):
            place, p = location
            
            start = ""
            end = "\033[0m"
            #fixes escape codes to make the mills blue when you are asked to delete something
            if board.has_mill(place):
                start += "\u001b[34m"
            if destruction:
                if only_mills and board.has_mill(place) and p == valid_target:
                    start += "\033[1m"
                elif not board.has_mill(place) and p == valid_target:
                    start += "\033[1m"
                    
                    
                    
                    
            match p:
                case Piece.p1:
                    return start + self._p1sym + end
                case Piece.p2:
                    return start + self._p2sym + end
                case _:
                    return ' '
                    
        s = """\
7  ({2})━━━━━━━━━━━━━({14})━━━━━━━━━━━━({23}) 
    ┃╲              ┃             ╱┃
    ┃ ╲             ┃            ╱ ┃
    ┃  ╲            ┃           ╱  ┃
6   ┃  ({5})━━━━━━━━━({13})━━━━━━━━({20})  ┃          
    ┃   ┃╲          ┃         ╱┃   ┃          
    ┃   ┃ ╲         ┃        ╱ ┃   ┃         
    ┃   ┃  ╲        ┃       ╱  ┃   ┃        
5   ┃   ┃  ({8})━━━━━({12})━━━━({17})  ┃   ┃     
    ┃   ┃   ┃              ┃   ┃   ┃
    ┃   ┃   ┃              ┃   ┃   ┃
4  ({1})━({4})━({7})            ({16})━({19})━({22})
    ┃   ┃   ┃              ┃   ┃   ┃          
    ┃   ┃   ┃              ┃   ┃   ┃       
3   ┃   ┃  ({6})━━━━━({11})━━━━({15})  ┃   ┃   
    ┃   ┃  ╱        ┃       ╲  ┃   ┃     
    ┃   ┃ ╱         ┃        ╲ ┃   ┃    
    ┃   ┃╱          ┃         ╲┃   ┃
2   ┃  ({3})━━━━━━━━━({10})━━━━━━━━({18})  ┃
    ┃  ╱            ┃           ╲  ┃
    ┃ ╱             ┃            ╲ ┃
    ┃╱              ┃             ╲┃
1  ({0})━━━━━━━━━━━━━({9})━━━━━━━━━━━━({21})
    a   b  c        d       e   f  g"""
        values = [convert_to_symbol(x) for x in board.get_squares_list()]
        print(s.format(*values))