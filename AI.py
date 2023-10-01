import HelperFunctions
import random

diff = 2

def Place(board, piece, marked_pieces):
    if (diff == 0):
        return EasyPlace(board, piece, marked_pieces)
    elif (diff == 1):
        return MediumPlace(board, piece, marked_pieces)
    elif (diff == 2):
        return HardPlace(board, piece, marked_pieces)
    
def Move(board, piece, marked_pieces):
    if (diff == 0):
        return EasyMove(board, piece, marked_pieces)
    elif (diff == 1):
        return MediumMove(board, piece, marked_pieces)
    elif (diff == 2):
        return HardMove(board, piece, marked_pieces)
    
def Fly(board, piece, marked_pieces):
    if (diff == 0):
        return EasyFly(board, piece, marked_pieces)
    elif (diff == 1):
        return MediumFly(board, piece, marked_pieces)
    elif (diff == 2):
        return HardFly(board, piece, marked_pieces)


# Easy places pieces i a random order
def EasyPlace(board, piece, marked_pieces):
    legal_places = HelperFunctions.find_legal_placements(board, piece, marked_pieces)
    place = legal_places[random.randint(0, len(legal_places)) - 1]
    return place
def EasyMove(board, piece, marked_pieces):
    legal_places = HelperFunctions.find_legal_movements(board, piece, marked_pieces)
    place = legal_places[random.randint(0, len(legal_places)) - 1]
    return place
def EasyFly(board, piece, marked_pieces):
    legal_flys = HelperFunctions.find_legal_flys(board, piece, marked_pieces)
    fly = legal_flys[random.randint(0, len(legal_flys)) - 1]
    return fly

# Medium makes moves from Easy half the time, and from Hard half the time
def MediumPlace(board, piece, marked_pieces):
    move = random.randint(1,2)
    if move == 1:
        return EasyPlace()
    else:
        return HardPlace()
def MediumMove(board, piece, marked_pieces):
    move = random.randint(1,2)
    if move == 1:
        return EasyMove()
    else:
        return HardMove()
def MediumFly(board, piece, marked_pieces):
    move = random.randint(1,2)
    if move == 1:
        return EasyFly()
    else:
        return HardFly()

# Hard always makes a mill if it can, otherwise tries to place pieces next to eachother in order to make mills in the future
def HardPlace(board, piece, marked_pieces):
    #placera bredvid ett "par" om det går att göra en mill
    legalPlaces = HelperFunctions.find_legal_placements(board, piece, marked_pieces)
    millPlace = MillPlaceCheck(board, piece, marked_pieces, legalPlaces, 3)
    if (millPlace != 0):
        return millPlace
    
    #placera bredvid en ensam pjäs
    pairPlace = MillPlaceCheck(board, piece, marked_pieces, legalPlaces, 2)
    if (pairPlace != 0):
        return pairPlace
    #placement när alla pieces är millade random i mittre 3x3
    return EasyPlace(board, piece, marked_pieces)
    
def HardMove(board, piece, marked_pieces):
    legalMoves = HelperFunctions.find_legal_movements(board, piece, marked_pieces)
    millMove = MillMoveCheck(board, piece, marked_pieces, legalMoves, 3)
    if (millMove != 0):
        return millMove
    
    pairMove = MillMoveCheck(board, piece, marked_pieces, legalMoves, 2)
    if (pairMove != 0):
        return pairMove
    
    # Maybe want to try to move pieces toward eachother rather than just randomly
    return EasyMove(board, piece, marked_pieces)

def HardFly(board, piece, marked_pieces):
    legalFlys = HelperFunctions.find_legal_flys(board, piece, marked_pieces)
    millFly = MillMoveCheck(board, piece, marked_pieces, legalFlys, 3)
    if (millFly != 0):
        return millFly
    
    pairFly = MillMoveCheck(board, piece, marked_pieces, legalFlys, 2)
    if (pairFly != 0):
        return pairFly
    
    return EasyFly(board, piece, marked_pieces)

# Check if any placement in a list of legal placements would result in a big enough line to meet the threshhold. Set threshhold to 3 => check for mill, 2 => check for pair
def MillPlaceCheck(board, piece, marked_pieces, legal_places, threshhold):
    for n in range(0, len(legal_places) - 1):
        place = legal_places[n]
        verticalMill = HelperFunctions.find_vertical_line(board, place[0], place[1], piece, marked_pieces)
        horizontalMill = HelperFunctions.find_horizontal_line(board, place[0], place[1], piece, marked_pieces)
        if (len(verticalMill) >= threshhold or len(horizontalMill) >= threshhold):
            return place
    return 0

# Does exactly what MillPlaceCheck does, except legal_places is in the form [((),()) , ((),())...] instead of [(),()...]
def MillMoveCheck(board, piece, marked_pieces, legal_places, threshhold):
    for n in range(0, len(legal_places) - 1):
        move = legal_places[n]
        verticalMill = HelperFunctions.find_vertical_line(board, move[1][0], move[1][1], piece, marked_pieces)
        horizontalMill = HelperFunctions.find_horizontal_line(board, move[1][0], move[1][1], piece, marked_pieces)
        if (len(verticalMill) >= threshhold or len(horizontalMill) >= threshhold):
            return move
    return 0

# Finds a piece from the opponent to remove.
# Piece arg should be the player's piece
def AiRemove(board, piece, marked_pieces):
    pieces = HelperFunctions.find_placed_pieces(board, piece, marked_pieces)
    piece_to_remove = 0
    if(len(pieces) > 0):
        piece_to_remove = pieces[random.randint(0, (len(pieces)-1))]
    return piece_to_remove
    
