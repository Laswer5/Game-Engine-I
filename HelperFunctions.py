#from Mill import board_size, open_piece

board_size = 7

open_piece = 'o'

def get_board_size():
    return board_size
def get_open_piece():
    return open_piece

# Check if a placement is valid
# Returns true if the row and column is open and it is not a part of a mill
def is_valid_placement(row, col, board, marked_pieces):
    return board[row][col] == open_piece and not (row, col) in marked_pieces

# Determine if a move is valid
# Returns true if the length of the move is one, meaning that the new spot is either just to the left, right, under or above the old spot, and the new spot is opened and not part of a mill
def is_valid_move(row, col, board, marked_pieces, old_row, old_col):
    length = abs(row - old_row) + abs(col - old_col)
    if (length != 1):
        return False
    return is_valid_placement(row, col, board, marked_pieces)

def find_placed_pieces(board, piece, marked_pieces):
    pieces = []
    for i in range(0,(get_board_size()-1)):
        for j in range(0,(get_board_size()-1)):
            if (board[i][j] == piece and not (i, j) in marked_pieces):
                pieces.append((i, j))
    return pieces

# Find a vertical line of pieces
# Returns an array of all pieces vertically connected that are part of a mill(not in marked pieces) and are the same piece as the input piece
def find_vertical_line(board, row, col, piece, marked_pieces):
    vertical_line = set([(row, col)])
    i = row+1
    while (i < board_size):
        if (board[i][col] == piece and not (i, col) in marked_pieces):
            vertical_line.add((i, col))
            i = i + 1
        else:
            break
    i = row-1
    while (i >= 0):
        if (board[i][col] == piece and not (i, col) in marked_pieces):
            vertical_line.add((i, col))
            i = i - 1
        else:
            break
    return vertical_line

# Find a horizontal line of pieces
# Returns an array of all pieces horizontally connected that are part of a mill(not in marked pieces) and are the same piece as the input piece
def find_horizontal_line(board, row, col, piece, marked_pieces):
    horizontal_line = set([(row, col)])
    i = col+1
    while (i < board_size):
        if (board[row][i] == piece and not (row, i) in marked_pieces):
            horizontal_line.add((row, i))
            i = i + 1
        else:
            break
    i = col-1
    while (i >= 0):
        if (board[row][i] == piece and not (row, i) in marked_pieces):
            horizontal_line.add((row, i))
            i = i - 1
        else:
            break
    return horizontal_line

def find_legal_placements(board, piece, marked_pieces):
    legals = []
    for n in range(0, board_size):
        for m in range(0, board_size):
            if (is_valid_placement(n, m, board, marked_pieces)):
                legals.append((n, m))
    return legals

def find_legal_movements(board, piece, marked_pieces):
    legals = []
    for n in range(0, board_size):
        for m in range(0, board_size):
            if (board[n][m] == piece):
                for row in range(0, board_size):
                    for col in range(0, board_size):
                        if (is_valid_move(row, col, board, marked_pieces, n, m)):
                            legals.append(((n, m),(row, col)))
    return legals
