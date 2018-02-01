from __future__ import absolute_import
from __future__ import division

import math
import random

from gameModel import *

REROLL_THREES = True


class Threes(Model):
    def __init__(self, save_game=True, data=None):
        Model.__init__(self, save_game)
        self.width = WIDTH
        self.height = HEIGHT
        self.newGame()
        if data:
            i, j = 0, 0
            size = self.width * self.height
            for elem in data[:size]:
                self.board[j][i] = elem
                i += 1
                if i >= self.width:
                    j += 1
                    i = 0
            self._parseNext(data[-3:])
            quantity_1 = data[:size].count(1)
            quantity_2 = data[:size].count(2)
            loaded = [min(4, 4 - (quantity_2 - quantity_1)), min(4, 4 - (quantity_1 - quantity_2)), 4]
            self.poss_index = sum(loaded)
            self.poss_nexts = np.array([])
            for i in xrange(3):
                self.poss_nexts = np.append(self.poss_nexts, [i + 1 for j in xrange(loaded[i])])
            random.shuffle(self.poss_nexts)
            for i in xrange(3):
                self.poss_nexts = np.append(self.poss_nexts, [i + 1 for j in xrange(4 - loaded[i])])

    def newGame(self):
        self.board = np.array([[0 for _ in xrange(self.width)] for _ in xrange(self.height)], dtype=np.int32)
        self.highest = 3
        self.highest_power = 0
        self.poss_nexts = np.array([(i % 3) + 1 for i in xrange(12)], dtype=np.int32)
        random.shuffle(self.poss_nexts)
        self.poss_index = 0
        self._initBoard()
        self._calculateNext()
        self._calculateVisibleNexts()

    def _parseNext(self, nexts):
        self.visible_nexts = list(ifilter(lambda x: x != 0, nexts))
        self.next = random.choice(self.visible_nexts)

    def _initBoard(self):
        fields = [(x, y) for x in xrange(self.width) for y in xrange(self.height)]
        random.shuffle(fields)
        for x, y in fields[:9]:
            self.board[y][x] = self.poss_nexts[self.poss_index]
            self.poss_index += 1
            if self.poss_index >= len(self.poss_nexts):
                random.shuffle(self.poss_nexts)
                self.poss_index = 0

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
        x_moved = set()
        y_moved = set()
        for y in ys:
            for x in xs:
                if self.board[y][x] != 0:
                    # if self.board[y + y_mod][x + x_mod] == 0:
                    #    self.board[y+y_mod][x+x_mod] = self.board[y][x]
                    #    self.board[y][x] = 0
                    #                   print(x + x_mod, y + y_mod)
                    if self.board[y + y_mod][x + x_mod] == 0 \
                            or self._canJoin(self.board[y + y_mod][x + x_mod], self.board[y][x]):
                        self.board[y + y_mod][x + x_mod] = self._join(self.board[y + y_mod][x + x_mod],
                                                                      self.board[y][x])
                        self.board[y][x] = 0
                        x_moved.add(x)
                        y_moved.add(y)
        return list(x_moved), list(y_moved)

    def makeMove(self, move):
        xs = [i for i in xrange(self.width)]
        ys = [i for i in xrange(self.height)]
        if move == MoveEnum.Left:
            _, y_moved = self._makeMove(xs[1:], ys, -1, 0)
            self.board[random.choice(y_moved)][self.width - 1] = self.next
        if move == MoveEnum.Up:
            x_moved, _ = self._makeMove(xs, ys[1:], 0, -1)
            self.board[self.height - 1][random.choice(x_moved)] = self.next
        if move == MoveEnum.Right:
            _, y_moved = self._makeMove(xs[::-1][1:], ys, 1, 0)
            self.board[random.choice(y_moved)][0] = self.next
        if move == MoveEnum.Down:
            x_moved, _ = self._makeMove(xs, ys[::-1][1:], 0, 1)
            self.board[0][random.choice(x_moved)] = self.next

        self.highest = max(max(x) for x in self.board)
        if self.highest > 3 * 2 ** self.highest_power:
            self.highest_power += 1
        self._calculateNext()
        self._calculateVisibleNexts()

    def _join(self, el1, el2):
        return el1 + el2

    def _canJoin(self, el1, el2):
        if el1 == el2 and el1 != 2 and el1 != 1:
            return True
        if min(el1, el2) == 1 and max(el1, el2) == 2:
            return True
        return False

    def _calculateNext(self):
        random_list = xrange(21)
        r = random.choice(random_list)
        if r == 0 and self.highest_power > SPECIAL_DEMOTION:
            p = random.choice(xrange(1, 1 + self.highest_power - SPECIAL_DEMOTION))
            self.next = 3 * 2 ** p
            return self.next
        self.next = self.poss_nexts[self.poss_index]
        self.poss_index += 1
        if self.poss_index >= len(self.poss_nexts):
            random.shuffle(self.poss_nexts)
            self.poss_index = 0
        elif REROLL_THREES:
            to_reroll = self.poss_nexts[self.poss_index:]
            random.shuffle(to_reroll)
            self.poss_nexts[self.poss_index:] = to_reroll
        return self.next

    def _calculateVisibleNexts(self):
        if self.next <= 3:
            self.visible_nexts = [self.next]
            return
        if self.highest_power - SPECIAL_DEMOTION < 3:
            self.visible_nexts = []
            for p in xrange(1, self.highest_power - SPECIAL_DEMOTION + 1):
                self.visible_nexts += [3 * (2 ** p)]
            return
        factor = Threes._scoringFactor(self.next) - 1
        poss = []
        if factor > 2:
            poss += [-1]  # 6 12 24
        if factor <= self.highest_power - SPECIAL_DEMOTION - 2:
            poss += [1]  # 24 48 96
        if self.highest_power - SPECIAL_DEMOTION - 1 >= factor > 1:
            poss += [0]  # 12 24 48
        modifier = random.choice(poss)
        self.visible_nexts = []
        for p in xrange(-1, 2):
            self.visible_nexts += [3 * 2 ** (p + modifier + factor)]

    @staticmethod
    def _scoringFactor(element):
        if element < 3:
            return 0
        return int(math.log(element / 3, 2) + 1)

    def score(self):
        result = 0
        for row in self.board:
            for el in row:
                factor = Threes._scoringFactor(el)
                if factor > 0:
                    result += 3 ** factor
        return result

    def data(self, normalize=False):
        
        result = np.log2(np.array(self.board.flatten()), where=[self.board.flatten() > 0])
        nexts = np.log2(self.visible_nexts) + 0.5
        for i in xrange(3 - len(nexts)):
            nexts = np.append(nexts, [0])
        result = np.append(result, nexts)
        if normalize:
            result = result / (3 * 12)
        return result
        
        '''
        result = np.array(self.board.flatten())
        nexts = self.visible_nexts
        for i in xrange(3 - len(nexts)):
            nexts += [0]
        result = np.append(result, nexts)
        if normalize:
            result = result / (3 * 2 ** 12)
        return result
        '''


    def stateInfo(self):
        return State(self.board, self.visible_nexts, self.score())
