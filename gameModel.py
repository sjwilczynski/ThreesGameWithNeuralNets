import enum

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
    def canMove(self, move):
        raise NotImplemented

    def makeMove(self, move):
        raise NotImplemented

    def stateInfo(self):
        raise NotImplemented

    def data(self):
        raise NotImplemented

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
