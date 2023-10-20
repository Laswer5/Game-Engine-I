from enum import Enum

class Piece(Enum):
    unoccupied = 0
    p1 = 1
    p2 = 2
    def __str__(self) -> str:
        match self: 
            case Piece.unoccupied:
                return " "
            case Piece.p1:
                return "X"
            case Piece.p2:
                return "O"
    def fromPlayer(i:int):
        return Piece.p1 if i == 1 else Piece.p2
        

class Board:
    """A board
    
    Implementation detail ideas: its a graph
    """
    def __init__(self) -> None:
        self._dict = {
            'a1':Piece.unoccupied,
            'd1':Piece.unoccupied,
            'g1':Piece.unoccupied,
            'b2':Piece.unoccupied,
            'd2':Piece.unoccupied,
            'f2':Piece.unoccupied,
            'c3':Piece.unoccupied,
            'd3':Piece.unoccupied,
            'e3':Piece.unoccupied,
            'a4':Piece.unoccupied,
            'b4':Piece.unoccupied,
            'c4':Piece.unoccupied,
            'e4':Piece.unoccupied,
            'f4':Piece.unoccupied,
            'g4':Piece.unoccupied,
            'd5':Piece.unoccupied,
            'c5':Piece.unoccupied,
            'e5':Piece.unoccupied,
            'f6':Piece.unoccupied,
            'd6':Piece.unoccupied,
            'b6':Piece.unoccupied,
            'g7':Piece.unoccupied,
            'd7':Piece.unoccupied,
            'a7':Piece.unoccupied,
        }
        self._adjacency = {
            'a1':['b2','a4','d1'],
            'd1':['a1','d2','g1'],
            'g1':['d1','f2','g4'],
            'b2':['a1','c3','b4','d2'],
            'd2':['d1','b2','f2','d3'],
            'f2':['g1','f4','e3','d2'],
            'c3':['b2','d3','c4'],
            'd3':['d2','c3','e3'],
            'e3':['f2','d3','e4'],
            'a4':['a7','a1','b4'],
            'b4':['a4','b6','b2','c4'],
            'c4':['b4','c3','c5'],
            'e4':['f4','e3','e5'],
            'f4':['g4','f6','f2','e4'],
            'g4':['f4','g1','g7'],
            'd5':['c5','e5','d6'],
            'c5':['b6','d5','c4'],
            'e5':['f6','d5','e4'],
            'f6':['g7','f4','e5','d6'],
            'd6':['d7','b6','f6','d5'],
            'b6':['a7','c5','b4','d6'],
            'g7':['d7','f6','g4'],
            'd7':['a7','d6','g7'],
            'a7':['b6','a4','d7']   
        }
        self._mills : list[tuple[str,str,str]] = []
        self._banned_mills : list[tuple[str,str,str]] = []
        
        
    def get_squares_list(self):
        """Returns a list of the squares sorted by alphabetical order

        Returns:
            list[tuple[str,Piece]]: _description_
        """
        return list(sorted(self._dict.items(), key = lambda x: x[0]))
    
    def has_mill(self,place:str)->bool:
        """Checks if a location has a mill, does not modify internal state or take into account past states of the board
        
        Args:
            place: str the place where the set will happen
            piece: Piece the piece to be checked against
        Returns:
            bool: wether it would create a mill or not 
        """    
        #this function is really ugly, if this class were to be reimplemented it could have been made alot prettier
        
        return any([place in l for l in self._mills])
    
    def ban_mills(self,mills:list[tuple[str,str,str]]):
        self._banned_mills = list(set(self._banned_mills + mills))
        
    def unban_mills(self,mills:list[tuple[str,str,str]]):
        for mill in mills:
            self._banned_mills.remove(mill)
    
    def get_mills(self,place:str)->[tuple[str,str,str]]:
        return [l for l in self._mills if place in l]        
        
    def count_pieces(self,piece:Piece)->int:
        return  list(map(lambda x: x[1],self.get_squares_list())).count(piece)
    def get_adjacency_list(self):
        return self._adjacency
            
    
    def set_piece(self,location,type):
        possible_mills = [('a1','d1','g1'),('a1','a4','a7'),('a1','b2','c3'),('b2','d2','f2'),('d1','d2','d3'),('g1','g4','g7'),
                          ('g1','f2','e3'),('f2','f4','f6'),('b2','b4','b6'),('c3','c4','c5'),('e3','e4','e5'),('a4','b4','c4'),
                          ('e4','f4','g4'),('c5','d5','e5'),('b6','d6','f6'),('a7','d7','g7'),('a7','b6','c5'),('g7','f6','e5'),
                          ('d5','d6','d7'),('c3','d3','e3')]
        self._dict[location] = type
        if type == Piece.unoccupied:
            for mill in [m for m in self._mills if location in m]:
                self._mills.remove(mill)    
                
        else:
            for possible_mill in [m for m in possible_mills if location in m]:
                #checks that the other pieces in the possible mill are correct
                pieces = [self.get_piece(possible_mill[0]), self.get_piece(possible_mill[1]), self.get_piece(possible_mill[2])]

                if (pieces == [Piece.p1,Piece.p1,Piece.p1] or pieces == [Piece.p2,Piece.p2,Piece.p2]) and possible_mill not in self._banned_mills:
                    self._mills.append(possible_mill)
                    break
        
    def get_piece(self,location) -> type:
        return self._dict[location]
        
    
    def __str__(self) -> str:
        #produces an orderered list of string representations of pieces
        l = list(map(lambda x:str(x[1]),self.get_squares_list()))
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
            
        return s.format(*l)
        

if __name__ == "__main__":
    board = Board()
    print(str(board))
    board.set_piece("a1",Piece.p1)
    board.set_piece("a7",Piece.p2)
    board.set_piece("a4",Piece.p1)
    board.set_piece("b6",Piece.p2)
    board.set_piece("e3",Piece.p1)
    board.set_piece("c5",Piece.p2)
    board.set_piece("e3",Piece.unoccupied)
    print(str(board))