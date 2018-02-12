from __future__ import absolute_import

import math

from gameModel import *

EASY_WIDTH = 4
EASY_HEIGHT = 1
EASY_SCORE_MOD = 5
EASY_MAX_MOVES = 50


class EasyGame(Model):
    def __init__(self, save_game=False, data=None):
        super(EasyGame, self).__init__(save_game)
        self.width = EASY_WIDTH
        self.height = EASY_HEIGHT
        self.furthest_pos = (0, 0)
        self.elem_pos = [0, 0]
        self.moves_made = 0
        self.newGame()
        if data:
            i, j = 0, 0
            for elem in data:
                self.board[j][i] = elem
                i += 1
                if i >= self.width:
                    j += 1
                    i = 0

    def newGame(self):
        self.board = np.array([[0 for _ in xrange(self.width)] for _ in xrange(self.height)], dtype=np.int32)
        x = 0  # np.random.randint(0, self.width)
        y = 0  # np.random.randint(0, self.height)
        self.board[y][x] = 1
        self.elem_pos = [y, x]
        self.curr_score = x + y
        self.furthest_pos = (y, x)

    def _inBound(self, pos, shift):
        return self.height > pos[0] + shift[0] >= 0 and self.width > pos[1] + shift[1] >= 0

    def canMove(self, move):
        if self.elem_pos == [EASY_HEIGHT - 1, EASY_WIDTH - 1] or self.moves_made == EASY_MAX_MOVES:
            return False
        if move == MoveEnum.Left:
            return self._inBound(self.elem_pos, (0, -1))
        if move == MoveEnum.Up:
            return self._inBound(self.elem_pos, (-1, 0))
        if move == MoveEnum.Right:
            return self._inBound(self.elem_pos, (0, 1))
        if move == MoveEnum.Down:
            return self._inBound(self.elem_pos, (1, 0))

    def makeMove(self, move):
        self.board[self.elem_pos[0]][self.elem_pos[1]] = 0
        if move == MoveEnum.Left:
            self.elem_pos[1] += -1
        if move == MoveEnum.Up:
            self.elem_pos[0] += -1
        if move == MoveEnum.Right:
            self.elem_pos[1] += 1
        if move == MoveEnum.Down:
            self.elem_pos[0] += 1
        self.board[self.elem_pos[0]][self.elem_pos[1]] = 1

        if self.elem_pos[0] > self.furthest_pos[0] and self.elem_pos[1] > self.furthest_pos[1]:
            self.furthest_pos = (self.elem_pos[0], self.furthest_pos[1])
        elif self.elem_pos[1] > self.furthest_pos[1]:
            self.furthest_pos = (self.furthest_pos[0], self.elem_pos[1])
        self.moves_made += 1
        self.curr_score = self.elem_pos[0] + self.elem_pos[1]

    def stateInfo(self):
        return State(self.board, score=self.score())

    def score(self, normalize=False):
        res = (self.curr_score + 2) * EASY_SCORE_MOD - self.moves_made
        if normalize:
            min_score = EASY_MAX_MOVES - (2 * EASY_SCORE_MOD)
            max_score = (self.height + self.width) * EASY_SCORE_MOD
            res -= (max_score - min_score) / 2.0
            if res != 0:
                res = math.copysign(math.log(abs(res)), res) / math.log((max_score + min_score) / 2.0)
        return res

    def data(self, normalize=False):
        result = np.array(self.board.flatten())
        result = np.append(result, [])
        return result
