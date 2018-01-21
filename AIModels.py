from gameModel import *
from qLearningNet import *
from test import printer
import random

MOVES_DICT = {u"w": MoveEnum.Up,
              u"a": MoveEnum.Left,
              u"s": MoveEnum.Down,
              u"d": MoveEnum.Right}


class AIModel(object):
    def __init__(self, game, filename=None):
        self.game = game

    def choose_move(self):
        raise NotImplemented

    @staticmethod
    def test_ai(ai_model, number_of_games, verbose=False):
        global_scores = []
        moves_count = {MoveEnum.Up.name: 0,
                       MoveEnum.Left.name: 0,
                       MoveEnum.Down.name: 0,
                       MoveEnum.Right.name: 0}
        for _ in range(number_of_games):
            seed = int(time.time())
            random.seed(seed)
            ai_model.game.newGame()
            if verbose:
                printer(ai_model.game)
            while True:
                any_move = False
                for move in MOVES_DICT.values():
                    any_move = any_move or ai_model.game.canMove(move)
                if not any_move:
                    global_scores += [ai_model.game.score()]
                    break
                move = ai_model.choose_move()
                if verbose:
                    print "Best move is {}".format(move)
                moves_count[move.name] += 1
                if ai_model.game.canMove(move):
                    ai_model.game.makeMove(move)
                else:
                    raise Exception("AI performed invalid move")
                if verbose:
                    print
                    printer(ai_model.game)
            if verbose:
                print "Game score was {}".format(ai_model.game.score())
                print "Number of times each move were chosen {}".format(moves_count)


class QLearningNetAI(AIModel):
    def __init__(self, game, filename=None):
        super(QLearningNetAI, self).__init__(game)
        self.ai = QLearningNet()
        if filename is not None:
            self.ai.load_parameters(FILENAME)

    def choose_move(self):
        q_values = self.ai.Q(self.game.data())
        return sorted(self.game.getPossibleMoves(), key=lambda x: q_values[x.value])[0]


class RandomAI(AIModel):
    def __init__(self, game, filename=None):
        super(RandomAI, self).__init__(game)

    def choose_move(self):
        possible_moves = self.game.getPossibleMoves()
        return possible_moves[np.random.randint(0, len(possible_moves))]
