from random import *

from threes import *


class loader:
    def __init__(self, game=Threes, epsilon=0.01):
        self.game = game
        self.game_state = self.game()
        self.epsilon = epsilon

    def get(self, model, batch_size=20):
        self.replay_memory = []
        for i in range(batch_size):
            self.replay_memory += [self._getOneBatch(model)]
        return np.array(self.replay_memory)

    def _getOneBatch(self, model):
        if not self.game_state.getPossibleMoves():
            self.game_state = self.game()
        move = None
        if random.random() < self.epsilon:
            move = random.choice(self.game_state.getPossibleMoves())
        else:
            best_result = 0
            for pos_move in self.game_state.getPossibleMoves():
                res = model(np.array([np.append(self.game_state.data(), [pos_move.value])]))
                if res > best_result:
                    best_result = res
                    move = pos_move
        return self.game_state.getTransitionData(move, True)


if __name__ == '__main__':
    def f(a):
        return a[0][-1]


    loa = loader()
    print(loa.get(f, 20))
