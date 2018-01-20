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
            print "tu {}".format(move)
        else:
            best_result = float("-inf")
            for pos_move in self.game_state.getPossibleMoves():
                res = model.Q(np.array([np.append(self.game_state.data(), [pos_move.value])]))[0]
                print res
                if res >= best_result:
                    best_result = res
                    move = pos_move
            if move is None:
                print self.game_state.getPossibleMoves()
        return self.game_state.getTransitionData(move, True)


if __name__ == u'__main__':
    def f(a):
        return a[0][-1]


    loa = loader()
    print loa.get(f, 20)
