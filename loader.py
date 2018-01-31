from __future__ import absolute_import

from random import *

from threes import *


class Loader(object):
    def __init__(self, game=None, epsilon=0.1):
        if game is not None:
            self.game = game
        else:
            self.game = Threes()
        self.epsilon = epsilon

    def get(self, model, batch_size=20):
        self.replay_memory = []
        for i in xrange(batch_size):
            self.replay_memory += [self._getOneBatch(model)]
        return np.array(self.replay_memory)

    def _getOneBatch(self, model):
        if not self.game.getPossibleMoves():
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
