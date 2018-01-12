import enum
import time

import numpy as np

WIDTH = 4
HEIGHT = 4
SPECIAL_DEMOTION = 3


class MoveEnum(enum.Enum):
    Left = 0
    Up = 1
    Right = 2
    Down = 3


class State:
    def __init__(self, board, visible_nexts=None):
        self.board = board
        self.visible_nexts = visible_nexts

class Model:
    def __init__(self, save_game):
        self.save_game = save_game

    def canMove(self, move):
        raise NotImplemented

    def makeMove(self, move):
        raise NotImplemented

    def stateInfo(self):
        raise NotImplemented

    def data(self):
        """
        This method should return all data about current state of the model used by neural network.
        """
        raise NotImplemented


def getFilename():
    return "game_results/" + time.strftime("%Y%m%d-%H%M%S")


def saveState(model, move, filename):
    '''
    This function saves the game state for future learning.
    Current turn, state of the board, next value, current score and performed moved are saved.
    '''
    file = open(filename, 'a+')
    row = model.data()
    row = np.append([move], row)
    file.write(np.array2string(row, separator=',') + '\n')
    file.close()

def read_saved_result(filename):
    '''
    for future usage - read data from saved states
    '''
    file = open(filename, 'r')
    lines = file.read().splitlines()
    for line in lines:
        data = np.fromstring(line[1:-1], sep=',', dtype = np.int32)
        turn = data[0]
        board = data[1:17]
        next_value = data[17]
        score = data[18]
        print('{} {} {} {}'.format(turn, board, next_value, score))


def printer(curr_game):
    board = curr_game.stateInfo()
    for ys in board:
        for el in ys:
            x = "."
            if el != 0:
                x = el
            print("{:>4}".format(x), end=" ")
        print("")


def put_piece(t, x, y, el):
    t.board[y][x] = el
