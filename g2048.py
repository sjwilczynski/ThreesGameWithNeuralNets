from __future__ import absolute_import
import random

from gameModel import *


class G2048(Model):
    def __init__(self, save_game=True):
        super(G2048, self).__init__(save_game)
        self.width = WIDTH
        self.height = HEIGHT
        self.board = np.array([[0 for _ in xrange(self.width)] for _ in xrange(self.height)], dtype=np.int32)
        self._initBoard()
        self.turn_counter = 0
        self.score = 0

    def _initBoard(self):
        fields = [(x, y) for x in xrange(self.width) for y in xrange(self.height)]
        random.shuffle(fields)
        for x, y in fields[:2]:
            self.board[y][x] = self._getNext()

    def _canMove(self, xs, ys, x_mod, y_mod):
        for y in ys:
            for x in xs:
                if self.board[y][x] != 0:
                    if self._canJoin(self.board[y + y_mod][x + x_mod], self.board[y][x]) \
                            or self.board[y + y_mod][x + x_mod] == 0:
                        return True
        return False

    def canMove(self, move):
        xs = [i for i in xrange(self.width)]
        ys = [i for i in xrange(self.height)]
        if move == MoveEnum.Left:
            return self._canMove(xs[1:], ys, -1, 0)
        if move == MoveEnum.Up:
            return self._canMove(xs, ys[1:], 0, -1)
        if move == MoveEnum.Right:
            return self._canMove(xs[:-1], ys, 1, 0)
        if move == MoveEnum.Down:
            return self._canMove(xs, ys[:-1], 0, 1)

    def _makeMove(self, xs, ys, x_mod, y_mod):
        for y in ys:
            for x in xs:
                if self.board[y][x] != 0:
                    x2 = x
                    y2 = y
                    while self.height > y2 + y_mod >= 0 and self.width > x2 + x_mod >= 0 and \
                                    self.board[y2 + y_mod][x2 + x_mod] == 0:
                        self.board[y2 + y_mod][x2 + x_mod] = self.board[y2][x2]
                        self.board[y2][x2] = 0
                        y2 += y_mod
                        x2 += x_mod
                    if self.height > y2 + y_mod >= 0 and self.width > x2 + x_mod >= 0 and \
                            self._canJoin(self.board[y2 + y_mod][x2 + x_mod], self.board[y2][x2]):
                        self.board[y2 + y_mod][x2 + x_mod] = self._join(self.board[y2 + y_mod][x2 + x_mod],
                                                                        self.board[y2][x2])
                        self.board[y2][x2] = 0

    def _emptyFields(self):
        result = []
        for y in xrange(4):
            for x in xrange(4):
                if self.board[y][x] == 0:
                    result += [(y, x)]
        return result

    def makeMove(self, move):
        xs = [i for i in xrange(self.width)]
        ys = [i for i in xrange(self.height)]
        if move == MoveEnum.Left:
            self._makeMove(xs[1:], ys, -1, 0)
        if move == MoveEnum.Up:
            self._makeMove(xs, ys[1:], 0, -1)
        if move == MoveEnum.Right:
            self._makeMove(xs[::-1][1:], ys, 1, 0)
        if move == MoveEnum.Down:
            self._makeMove(xs, ys[::-1][1:], 0, 1)

        y, x = random.choice(self._emptyFields())
        self.board[y][x] = self._getNext()

    def _join(self, el1, el2):
        self.score += el1 + el2
        return el1 + el2

    def _canJoin(self, el1, el2):
        return el1 == el2

    def _getNext(self):
        return 2 if random.random() < 0.9 else 4

    def data(self):
        result = np.array(self.board.flatten())
        result = np.append([self.turn_counter, self.score], result)
        return result

    def score(self):
        return self.score

    def stateInfo(self):
        return State(self.board, score=self.score)
