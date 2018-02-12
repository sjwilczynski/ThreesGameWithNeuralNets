from __future__ import absolute_import

from random import *

import min_max
from easyGame import *
from threes import *


class BaseLoader(object):
    def __init__(self, game=Threes()):
        self.game = game

        def get(self, model, batch_size=20):
            pass


class Loader(BaseLoader):
    def __init__(self, game=Threes(), epsilon=0.1):
        super(Loader, self).__init__(game)
        self.epsilon = epsilon

    def get(self, model, batch_size=20):
        self.replay_memory = []
        for i in xrange(batch_size):
            self.replay_memory += [self._getOneBatch(model)]
        return np.array(self.replay_memory)

    def _getOneBatch(self, model):
        while not self.game.getPossibleMoves():
            self.game.newGame()
        move = None
        if random.random() < self.epsilon:
            move = random.choice(self.game.getPossibleMoves())
        else:
            res = model.Q(self.game.data(True))
            move = sorted(self.game.getPossibleMoves(), key=lambda x: res[x.value])[-1]
        return self.game.getTransitionData(move, True, True)
    
    @staticmethod
    def get_random_states(game, num_states, input_size=19):
        data = np.zeros((1, input_size))
        game.newGame()
        for i in range(50*num_states):
            if not game.getPossibleMoves():
                game.newGame()
            move = random.choice(game.getPossibleMoves())
            data = np.append(data,np.array(game.getTransitionData(move, True, True)[:input_size], ndmin=2),axis=0)
        indices = np.random.randint(1, len(data), num_states)
        return data[indices, :]


class MinMaxLoader(BaseLoader):
    def __init__(self, game=Threes(), epsilon=0.1):
        super(MinMaxLoader, self).__init__(game)
        self.epsilon = epsilon

    def get(self, model, batch_size=20):
        self.replay_memory = []
        for i in xrange(batch_size):
            self.replay_memory += [self._getOneBatch(model)]
        return np.array(self.replay_memory)

    def _getOneBatch(self, model):
        while not self.game.getPossibleMoves():
            self.game.newGame()
        move = None
        if random.random() < self.epsilon:
            move = random.choice(self.game.getPossibleMoves())
        else:
            move = min_max.best_move(self.game)
        return self.game.getTransitionData(move, True, True)


if __name__ == u'__main__':
    class f:
        def Q(self, a):
            return [1, 2, 3, 4]


    loa = Loader(game=EasyGame())
    print random.choice(loa.game.getPossibleMoves())
    print loa.get(f())
