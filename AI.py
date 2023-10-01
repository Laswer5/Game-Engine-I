import HelperFunctions
import random

diff = 0

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

def EasyMill():
    return

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
    
    #placera bredvid en ensam pjäs
    
    #placement när alla pieces är millade random i mittre 3x3
    
    return
def HardMove(board, piece, marked_pieces):
    return
def HardFly(board, piece, marked_pieces):
    return
