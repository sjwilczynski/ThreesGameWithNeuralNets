import random

from gameModel import *
from min_max import best_move as minimax_choose_move
from qLearningNet import *
from test import printer

MOVES_DICT = {u"w": MoveEnum.Up,
              u"a": MoveEnum.Left,
              u"s": MoveEnum.Down,
              u"d": MoveEnum.Right}


class AIModel(object):
    def __init__(self, game):
        self.game = game
        seed = int(time.time())
        random.seed(seed)

    def choose_move(self, verbose=False):
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
                move = ai_model.choose_move(verbose)
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
            self.ai = QLearningNet(input_size=game.flatten_state_info_size)
            if filename is not None:
                print "Loading net parameters"
                self.ai.load_parameters(filename)

    def choose_move(self, verbose=False):
        q_values = self.ai.Q(self.game.data(True))
        #print sorted(self.game.getPossibleMoves(), key=lambda x: q_values[x.value])
        if verbose:
            print self.game.data(True)
            print "Qvalues ",["%.15f"%item for item in q_values]
        return sorted(self.game.getPossibleMoves(), key=lambda x: q_values[x.value])[-1]


class RandomAI(AIModel):
    def __init__(self, game):
        super(RandomAI, self).__init__(game)

    def choose_move(self, verbose=False):
        possible_moves = self.game.getPossibleMoves()
        return possible_moves[np.random.randint(0, len(possible_moves))]


class SimpleAI(AIModel):
    def __init__(self, game):
        super(SimpleAI, self).__init__(game)

    def choose_move(self, verbose=False):
        moves = [MoveEnum.Right, MoveEnum.Down, MoveEnum.Up, MoveEnum.Left]
        for move in moves:
            if self.game.canMove(move):
                return move
        return None

class MiniMaxAI(AIModel):
    def __init__(self, game):
        super(MiniMaxAI, self).__init__(game)

    def choose_move(self, verbose=False):
        return minimax_choose_move(self.game, MOVES_DICT.values())
