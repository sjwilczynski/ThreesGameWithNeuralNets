from __future__ import absolute_import

import copy
import numpy as np
import time
from io import open
from itertools import ifilter

import enum

WIDTH = 4
HEIGHT = 4
SPECIAL_DEMOTION = 3


class MoveEnum(enum.Enum):
    Left = 0
    Up = 1
    Right = 2
    Down = 3


class GameEnum(enum.Enum):
    Threes = 0
    G2048 = 1


class State(object):
    def __init__(self, board, visible_nexts=None, score=None):
        self.board = board
        self.visible_nexts = visible_nexts
        self.score = score


class Model(object):
    flatten_state_info_size = 0

    def __init__(self, save_game, data=None, normalized=False):
        self.save_game = save_game

    def newGame(self):
        raise NotImplemented

    def canMove(self, move):
        raise NotImplemented

    def getPossibleMoves(self):
        return list(ifilter(self.canMove, list(MoveEnum)))

    def makeMove(self, move):
        raise NotImplemented

    def stateInfo(self):
        raise NotImplemented

    def score(self, normalize=False):
        raise NotImplemented
        
    def tiles_count(self):
        return np.count_nonzero(self.stateInfo().board)

    def getTransitionData(self, move, make_move=False, normalize=False):
        game = self
        score = self.score(normalize)
        tiles = self.tiles_count()
        result = self.data(normalize)
        if not make_move:
            game = copy.deepcopy(self)
        game.makeMove(move)
        move_val = move.value
        # if normalize:
        #    move_val /= 4.0
        merged_tiles = tiles + 1 - game.tiles_count()
        titles_mod = 10 * max(0,merged_tiles)
        if normalize:
            titles_mod /= 1000.0
        score = game.score(normalize) - score + titles_mod
        result = np.append(result, [move_val, score])
        result = np.append(result, game.data(normalize))
        return result

    def data(self, normalize=False):
        u"""
        This method should return all data about current state of the model used by neural network.
        """
        raise NotImplemented

    @classmethod
    def getTransitionDataSize(class_name):
        return 2 * class_name.flatten_state_info_size + 2



def getFilename():
    return u"game_results/" + time.strftime(u"%Y%m%d-%H%M%S")


def saveState(model, move, file):
    u'''
    Saves state of the game for future learning
    :param model: current Model object
    :param move: move made by the player for the current game state
    :param file: file to save the data in
    :return:
    '''
    file.write(','.join([str(x) for x in model.getTransitionData(move)]) + u'\n')
    file.flush()


def read_saved_result(filename):
    u'''
    :param filename: name of the file to read the data from
    :return:
    '''
    file = open(filename, u'r')
    text = file.read()
    index = 0
    new_index = text.index(u'\n', index)
    seed = int(text[index:new_index])
    print seed
    index = new_index + 1
    while index < len(text):
        new_index = text.index(u']', index) + 1
        line = text[index:new_index]
        data = np.fromstring(line[1:-1], sep=u',', dtype=np.int32)
        turn = data[0]
        score = data[1]
        visible_moves = data[2:5]
        board = data[5:21]
        move = data[21]
        print u'{} {} {} {}'.format(turn, score, visible_moves, board, move)
        index = new_index + 1
