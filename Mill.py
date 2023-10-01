# Import the necessary module for colored text
from termcolor import colored
#import HelperFunctions

import AI as ai
import HelperFunctions as helper

# Define the dimensions of the board
board_size = helper.get_board_size()

max_turns = 300
max_pieces = 4

player_piece = 'p'
ai_piece = 'a'
open_piece = helper.get_open_piece()

# Initialize an empty board
board = [[open_piece for _ in range(board_size)] for _ in range(board_size)]

# Define a list to keep track of marked pieces
marked_pieces = []
mills = []



# Print the game board
def print_board(board):
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == player_piece:
                if (r, c) in marked_pieces:
                    print(colored(player_piece.upper(), 'yellow'), end=' ')
                else:
                    print(colored(player_piece, 'green'), end=' ')
            elif cell == ai_piece:
                if (r, c) in marked_pieces:
                    print(colored(ai_piece.upper(), 'yellow'), end=' ')
                else:
                    print(colored(ai_piece, 'red'), end=' ')
            else:
                print(cell, end=' ')
        print()

# Place a piece on the board
def place_piece(row, col, piece, board):
    board[row][col] = piece

# Break a mill
def break_mill(row, col):
    for i in range(0, len(mills)):
        if ((row, col) in mills[i]):
            marks = mills[i]
            mills.pop(i)
            for n in marks:
                marked_pieces.remove(n)
            return

# Move a piece on the board
def move_piece(old_row, old_col, new_row, new_col, board):
    board[new_row][new_col] = board[old_row][old_col]
    board[old_row][old_col] = open_piece
    if ((old_row, old_col) in marked_pieces):
        break_mill(old_row, old_col)


# Count the number of a specific piece on the board
def count_pieces(board, piece):
    i = 0
    for n in range(0, board_size):
        for m in range(0, board_size):
            if (board[n][m] == piece and not (n, m) in marked_pieces):
                i = i + 1
    return i

# Check for a mill for one specific piece
def check_for_mill(board, row, col, piece):
    vertical_line = helper.find_vertical_line(board, row, col, piece, marked_pieces)
    horizontal_line = helper.find_horizontal_line(board, row, col, piece, marked_pieces)
    if (len(vertical_line) > 2):
        marked_pieces.extend(vertical_line)
        mills.append(vertical_line)
        remove_opponents_piece(board, piece)
    elif (len(horizontal_line) > 2):
        marked_pieces.extend(horizontal_line)
        mills.append(horizontal_line)
        remove_opponents_piece(board, piece)

# Remove an opponents piece
def remove_opponents_piece(board, piece):
    if (piece == player_piece):
        if (count_pieces(board, ai_piece) == 0):
            print("Player created a mill, but there are no pieces to remove.")
            return
        print("Player created a mill, remove AI's piece.")
        print_board(board)
        while True:
            try:
                row = int(input("Enter row (0-6): "))
                col = int(input("Enter column (0-6): "))
                if 0 <= row < board_size and 0 <= col < board_size and board[row][col] == ai_piece:
                    place_piece(row, col, open_piece, board)
                    break
                else:
                    print("Invalid remove. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        return
    elif (piece == ai_piece):
        if (count_pieces(board, player_piece) == 0):
            print("AI created a mill, but there are no pieces to remove.")
            return
        print("AI created a mill.")
        toRemove = ai.AiRemove(board, player_piece, marked_pieces)
        if (toRemove != 0):
            place_piece(toRemove[0], toRemove[1], open_piece, board)
            print("AI removed piece at: (", toRemove[0], ",", toRemove[1], ")")
    return

# Player move in Placement phase
def player_placement(board, piece):
    print_board(board)
    while True:
        try:
            row = int(input("Enter row (0-6): "))
            col = int(input("Enter column (0-6): "))
            if 0 <= row < board_size and 0 <= col < board_size and helper.is_valid_placement(row, col, board, marked_pieces):
                place_piece(row, col, piece, board)
                check_for_mill(board, row, col, piece)
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    return

# AI move in Placement phase
def ai_placement(board, piece):
    #player_placement(board, piece)
    place = ai.Place(board, piece, marked_pieces)
    place_piece(place[0], place[1], piece, board)
    check_for_mill(board, place[0], place[1], piece)


# Player move in Moving phase
def player_movement(board, piece, func):
    print_board(board)
    old_row = -1
    old_col = -1
    print("Select one of your pieces")
    while True:
        try:
            old_row = int(input("Enter row (0-6): "))
            old_col = int(input("Enter column (0-6): "))
            if 0 <= old_row < board_size and 0 <= old_col < board_size and board[old_row][old_col] == piece:
                break
            else:
                print("Invalid piece. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    print("Select an open space to move your piece")
    while True:
        try:
            new_row = int(input("Enter row (0-6): "))
            new_col = int(input("Enter column (0-6): "))
            if 0 <= new_row < board_size and 0 <= new_col < board_size and func(new_row, new_col, board, marked_pieces, old_row, old_col):
                move_piece(old_row, old_col, new_row, new_col, board)
                check_for_mill(board, new_row, new_col, piece)
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    return

# AI move in Moving phase
def ai_movement(board, piece):
    move = ai.Move(board, piece, marked_pieces)
    old = move[0]
    new = move[1]
    move_piece(old[0], old[1], new[0], new[1], board)
    check_for_mill(board, new[0], new[1], piece)
    return

# Helper function to send into player_movement
def _is_valid_placement(new_row, new_col, board, marked_pieces, old_row, old_col):
    return helper.is_valid_placement(new_row, new_col, board, marked_pieces)

# Player move in Flying phase
def player_fly(board, piece):
    player_movement(board, piece, _is_valid_placement)
    return

# AI move in Flying phase
def ai_fly(board, piece):
    fly = ai.Fly(board, piece, marked_pieces)
    old = fly[0]
    new = fly[1]
    move_piece(old[0], old[1], new[0], new[1], board)
    check_for_mill(board, new[0], new[1], piece)
    return

def main():

    # Placing phase
    for _ in range(max_pieces):
        print("Player's turn (", player_piece, ")")
        player_placement(board, player_piece)
        print("AI's turn (", ai_piece, ")")
        ai_placement(board, ai_piece)

    
    # Moving and flying phase
    for i in range(max_turns):
        print("Turn: " , i , "/" , max_turns)
        print("Player's turn (", player_piece, ")")
        if (count_pieces(board, player_piece) == 2):
            print("AI wins!")
            return
        elif (count_pieces(board, player_piece) == 3):
            player_fly(board, player_piece)
        else:
            player_movement(board, player_piece, helper.is_valid_move)

        print("AI's turn (", ai_piece, ")")
        if (count_pieces(board, ai_piece) == 2):
            print("Player wins!")
            return
        elif (count_pieces(board, ai_piece) == 3):
            ai_fly(board, ai_piece)
        else:
            ai_movement(board, ai_piece)
    print("Draw!")
    return


main()

