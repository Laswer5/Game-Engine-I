class Tutorial:
    @staticmethod
    def runTutorial():
        """
        static method that runs a tutorial menu
        """
        titles = ["The Objective of the Game","How to Play","Winning conditions","Making a move","Additional information"]
        contents = [
            "The primary objective of the game is to form \"mills\" (a line of three pieces, horizontally or vertically). Every time a player forms a mill, they can remove one of their opponent's pieces from the board. The way to win is to reduce the opponent's pieces to a point where they have only two left. Each player starts with 12 pieces, which they will place and then move around the board.",
"""The game consists of three phases. Starting with Player 1, and then alternating, players place their pieces on any empty intersection point on the board in Phase 1. If a player forms a mill during this phase, they can remove one of the opponent's pieces that is not part of a mill. If all of an opponent's pieces are in mills, then any of the pieces can be removed. This phase continues until all 24 pieces (12 for each player) are on the board. 

When a player has no pieces left to place, the player transitions to Phase 2 and can now move one piece to an adjacent intersection point (along a line). Again, if a player forms a mill, they may remove one of their opponent's pieces following the same rules as above. If a player cannot move one of their pieces to an adjacent intersection point, the player loses the game. The game moves to Phase 3 when a player is down to only three pieces.

A player with only three pieces left can "fly" a piece from any point on the board to any other empty point, instead of just moving to an adjacent intersection. The other player continues to move pieces to adjacent intersections as before unless they too are reduced to three pieces, in which case they can also fly.
""",
"""\
The game ends when one of the following conditions is met:
- A player is reduced to two pieces, meaning they cannot form mills anymore. The other player is the winner. 
- A player cannot make a legal move (all their pieces are blocked by their opponent's pieces). The other player is the winner.
- If the game has gone on for more than 200 turns the game ends in a draw regardless
""",
"A player can make a move by writing the coordinates for the corresponding intersection point (i.e 'a1' or 'e4') and thenpressing ENTER.",
"Inputting -h you can get help during the game\nInputting -q during a game will exit the application immediately "]
        i = 0
        while True:
            print(f"{i+1}.{titles[i]}")
            print(contents[i])
            print("n: next, p: previous, q: quit")
            next = input()
            match next:
                case 'n':
                    i = (i+ 1)%len(titles)
                case 'p':
                    i = (i- 1)%len(titles)
                case 'q':
                    return
                case _:
                    print("invalid command")