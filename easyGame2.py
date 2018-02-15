from __future__ import absolute_import

import math

from gameModel import *

EASY_WIDTH = 4
EASY_HEIGHT = 4
EASY_SCORE_MOD = 5
EASY_MAX_MOVES = 50


class EasyGame2(Model):
    flatten_state_info_size = EASY_WIDTH * EASY_HEIGHT

    def __init__(self, save_game=False, data=None, normalized=False):
        super(EasyGame2, self).__init__(save_game)
        self.width = EASY_WIDTH
        self.height = EASY_HEIGHT
        self.furthest_pos = (0, 0)
        self.elem_pos = [[0, 0], [0, 0]]
        self.highest = 1
        self.newGame()
        if data:
            if normalized:
                data = np.array(data)
                data *= 2
                data = np.round(data)
                data = np.asarray(np.round(data), dtype=int).tolist()
            i, j = 0, 0
            self.elem_pos = []
            for elem in data:
                self.board[j][i] = elem
                for n in xrange(elem):
                    self.elem_pos += [[j, i]]
                i += 1
                if i >= self.width:
                    j += 1
                    i = 0

    def newGame(self):
        self.board = np.array([[0 for _ in xrange(self.width)] for _ in xrange(self.height)], dtype=np.int32)
        x = np.random.randint(0, self.width)
        y = np.random.randint(0, self.height)
        x2 = x
        y2 = y
        while x2 == x and y2 == y:
            x2 = np.random.randint(0, self.width)
            y2 = np.random.randint(0, self.height)
        self.board[y][x] = 1
        self.board[y2][x2] = 1
        self.elem_pos = [[y, x], [y2, x2]]
        self.curr_score = self._distScore()
        self.moves_made = 0

    def _distScore(self):
        result = self.width + self.height - 2 - np.abs(self.elem_pos[0][0] - self.elem_pos[1][0]) - \
                 np.abs(self.elem_pos[0][1] - self.elem_pos[1][1])
        return result

    def _inBound(self, pos, shift):
        return self.height > pos[0] + shift[0] >= 0 and self.width > pos[1] + shift[1] >= 0

    def _canMove(self, move, elem):
        if move == MoveEnum.Left:
            return self._inBound(elem, (0, -1))
        if move == MoveEnum.Up:
            return self._inBound(elem, (-1, 0))
        if move == MoveEnum.Right:
            return self._inBound(elem, (0, 1))
        if move == MoveEnum.Down:
            return self._inBound(elem, (1, 0))

    def canMove(self, move):
        if self.elem_pos[0] == self.elem_pos[1] or self.moves_made == EASY_MAX_MOVES:
            return False
        result = False
        for elem in self.elem_pos:
            result = result or self._canMove(move, elem)
        return result

    def makeMove(self, move):
        for ind in xrange(len(self.elem_pos)):
            if self._canMove(move, self.elem_pos[ind]):
                self.board[self.elem_pos[ind][0]][self.elem_pos[ind][1]] = 0
                if move == MoveEnum.Left:
                    self.elem_pos[ind][1] += -1
                if move == MoveEnum.Up:
                    self.elem_pos[ind][0] += -1
                if move == MoveEnum.Right:
                    self.elem_pos[ind][1] += 1
                if move == MoveEnum.Down:
                    self.elem_pos[ind][0] += 1
        for ind in xrange(len(self.elem_pos)):
            self.board[self.elem_pos[ind][0]][self.elem_pos[ind][1]] = 1
        if self.elem_pos[0] == self.elem_pos[1]:
            self.board[self.elem_pos[0][0]][self.elem_pos[0][1]] = 2
        self.moves_made += 1
        self.curr_score = self._distScore()

    def stateInfo(self):
        return State(self.board, score=self.score())

    def score(self, normalize=False):
        res = self.curr_score * EASY_SCORE_MOD - self.moves_made
        if normalize:
            min_score = EASY_MAX_MOVES
            max_score = (self.height + self.width - 2) * EASY_SCORE_MOD
            res -= (max_score - min_score) / 2.0
            if res != 0:
                res = math.copysign(math.log(abs(res)), res) / math.log((max_score + min_score) / 2.0)
        return res

    def data(self, normalize=False):
        result = np.array(self.board.flatten())
        if normalize:
            result = result / 2.0
        result = np.append(result, [])
        return result
