from gameModel import *
from qLearningNet import *
from min_max import best_move as minimax_choose_move
from test import printer
import random

MOVES_DICT = {u"w": MoveEnum.Up,
              u"a": MoveEnum.Left,
              u"s": MoveEnum.Down,
              u"d": MoveEnum.Right}


class AIModel(object):
    def __init__(self, game):
        self.game = game
        seed = int(time.time())
        random.seed(seed)

    def choose_move(self):
        raise NotImplemented

    @staticmethod
    def test_ai(ai_model, number_of_games, verbose=False):
        global_scores = []
        highests = []
        moves_count = {MoveEnum.Up.name: 0,
                       MoveEnum.Left.name: 0,
                       MoveEnum.Down.name: 0,
                       MoveEnum.Right.name: 0}
        for _ in range(number_of_games):
            ai_model.game.newGame()
            if verbose:
                printer(ai_model.game)
            while True:
                any_move = False
                for move in MOVES_DICT.values():
                    any_move = any_move or ai_model.game.canMove(move)
                if not any_move:
                    global_scores += [ai_model.game.score()]
                    highests += [ai_model.game.highest]
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
        if verbose:
            print "All scores {}".format(global_scores)
            print "Moves count {}".format(moves_count)
        return global_scores, moves_count, highests


class QLearningNetAI(AIModel):
    def __init__(self, game, filename=None, net=None):
        super(QLearningNetAI, self).__init__(game)
        if net is not None:
            self.ai = net
        else:
            self.ai = QLearningNet()
            if filename is not None:
                print "Loading net parameters"
                self.ai.load_parameters(filename)

    def choose_move(self):
        q_values = self.ai.Q(self.game.data())
        return sorted(self.game.getPossibleMoves(), key=lambda x: q_values[x.value])[0]


class RandomAI(AIModel):
    def __init__(self, game):
        super(RandomAI, self).__init__(game)

    def choose_move(self):
        possible_moves = self.game.getPossibleMoves()
        return possible_moves[np.random.randint(0, len(possible_moves))]


class MiniMaxAI(AIModel):
    def __init__(self, game):
        super(MiniMaxAI, self).__init__(game)

    def choose_move(self):
        return minimax_choose_move(self.game, MOVES_DICT.values())
