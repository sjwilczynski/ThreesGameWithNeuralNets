from __future__ import absolute_import

from random import *

from threes import *


class Loader(object):
    def __init__(self, game=Threes, epsilon=0.01):
        self.game = game
        self.game_state = self.game()
        self.epsilon = epsilon

    def get(self, model, batch_size=20):
        self.replay_memory = []
        for i in xrange(batch_size):
            self.replay_memory += [self._getOneBatch(model)]
        return np.array(self.replay_memory)

    def _getOneBatch(self, model):
        if not self.game_state.getPossibleMoves():
            self.game_state = self.game()
        move = None
        if random.random() < self.epsilon:
            move = random.choice(self.game_state.getPossibleMoves())
        else:
            res = model.Q(self.game_state.data(True))
            move = sorted(self.game_state.getPossibleMoves(), key=lambda x: res[x.value])[0]
        return self.game_state.getTransitionData(move, True, True)


if __name__ == u'__main__':
    class f:
        def Q(self, a):
            return [a[0][-1]]


    loa = Loader()
    print
    random.choice(loa.game_state.getPossibleMoves())
    print
    loa.get(f())
