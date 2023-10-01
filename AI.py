import HelperFunctions
import random

diff = 2

# Takes a board, the piece for the ai, and a list of pieces that are part of mills.
# Returns a tuple of coordinates to place a piece
def Place(board, piece, marked_pieces):
    if (diff == 0):
        return EasyPlace(board, piece, marked_pieces)
    elif (diff == 1):
        return MediumPlace(board, piece, marked_pieces)
    elif (diff == 2):
        return HardPlace(board, piece, marked_pieces)
    
# Takes a board, the piece for the ai, and a list of pieces that are part of mills.
# Returns a ((oldx, oldy),(newx, newy)) containing coordinates to move from and coordinates to move to. Old are where to move from and new is where to move to.
def Move(board, piece, marked_pieces):
    if (diff == 0):
        return EasyMove(board, piece, marked_pieces)
    elif (diff == 1):
        return MediumMove(board, piece, marked_pieces)
    elif (diff == 2):
        return HardMove(board, piece, marked_pieces)

# Takes a board, the piece for the ai, and a list of pieces that are part of mills.
# Returns a ((oldx, oldy),(newx, newy)) containing coordinates to fly from and coordinates to fly to. Old are where to fly from and new is where to fly to.
def Fly(board, piece, marked_pieces):
    if (diff == 0):
        return EasyFly(board, piece, marked_pieces)
    elif (diff == 1):
        return MediumFly(board, piece, marked_pieces)
    elif (diff == 2):
        return HardFly(board, piece, marked_pieces)

# Easy places pieces randomly
def EasyPlace(board, piece, marked_pieces):
    legal_places = HelperFunctions.find_legal_placements(board, piece, marked_pieces)
    place = legal_places[random.randint(0, len(legal_places)) - 1]
    return place
# Easy moves pieces randomly
def EasyMove(board, piece, marked_pieces):
    legal_places = HelperFunctions.find_legal_movements(board, piece, marked_pieces)
    place = legal_places[random.randint(0, len(legal_places)) - 1]
    return place
# Easy flies pieces randomly
def EasyFly(board, piece, marked_pieces):
    legal_flys = HelperFunctions.find_legal_flys(board, piece, marked_pieces)
    fly = legal_flys[random.randint(0, len(legal_flys)) - 1]
    return fly

# Medium makes places from Easy half the time, and from Hard half the time
def MediumPlace(board, piece, marked_pieces):
    move = random.randint(1,2)
    if move == 1:
        return EasyPlace(board, piece, marked_pieces)
    else:
        return HardPlace(board, piece, marked_pieces)
# Medium makes moves from Easy half the time, and from Hard half the time
def MediumMove(board, piece, marked_pieces):
    move = random.randint(1,2)
    if move == 1:
        return EasyMove(board, piece, marked_pieces)
    else:
        return HardMove(board, piece, marked_pieces)
# Medium makes flys from Easy half the time, and from Hard half the time
def MediumFly(board, piece, marked_pieces):
    move = random.randint(1,2)
    if move == 1:
        return EasyFly(board, piece, marked_pieces)
    else:
        return HardFly(board, piece, marked_pieces)

# Hard always makes a mill if it can, otherwise tries to place pieces next to eachother in order to make mills in the future
def HardPlace(board, piece, marked_pieces):
    legalPlaces = HelperFunctions.find_legal_placements(board, piece, marked_pieces)
    # Place so that a mill is formed
    millPlace = MillPlaceCheck(board, piece, marked_pieces, legalPlaces, 3)
    if (millPlace != 0):
        return millPlace
    
    # Place next to lone piece
    pairPlace = MillPlaceCheck(board, piece, marked_pieces, legalPlaces, 2)
    if (pairPlace != 0):
        return pairPlace
    # Place randomly
    return EasyPlace(board, piece, marked_pieces)
    
# Hard always makes a mill if it can, otherwise tries to place pieces next to eachother in order to make mills in the future
def HardMove(board, piece, marked_pieces):
    legalMoves = HelperFunctions.find_legal_movements(board, piece, marked_pieces)
    # Move so that a mill is formed
    millMove = MillMoveCheck(board, piece, marked_pieces, legalMoves, 3)
    if (millMove != 0):
        return millMove
    
    # Move next to lone piece
    pairMove = MillMoveCheck(board, piece, marked_pieces, legalMoves, 2)
    if (pairMove != 0):
        return pairMove
    
    # Move randomly. Maybe want to try to move pieces toward eachother rather than just randomly
    return EasyMove(board, piece, marked_pieces)

# Hard always makes a mill if it can, otherwise tries to place pieces next to eachother in order to make mills in the future
def HardFly(board, piece, marked_pieces):
    legalFlys = HelperFunctions.find_legal_flys(board, piece, marked_pieces)
    # Fly so that a mill is formed
    millFly = MillMoveCheck(board, piece, marked_pieces, legalFlys, 3)
    if (millFly != 0):
        return millFly
    
    # Move next to lone piece
    pairFly = MillMoveCheck(board, piece, marked_pieces, legalFlys, 2)
    if (pairFly != 0):
        return pairFly
    
    # Fly randomly. Maybe should fly to block player.
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
    
