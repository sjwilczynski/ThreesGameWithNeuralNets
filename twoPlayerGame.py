from __future__ import absolute_import
import threes
import g2048
from gameModel import *
import random
import time
import sys


def printer(curr_games):
    board1 = curr_games[0].board
    board2 = curr_games[1].board
    size = board1.shape[0]
    for j in xrange(size):
        r1 = board1[j]
        r2 = board2[j]
        print_row(r1)
        print u"", sys.stdout.write(u" | ")
        print_row(r2)
        print u""


def print_row(row):
    for el in row:
        x = u"."
        if el != 0:
            x = el
        print u"{:>4}".format(x),


def is_any_move_valid(g1, g2, dict=None):
    if not dict:
        dict = moves_dict
    any_move = False
    for m in dict.values():
        any_move = any_move or g1.canMove(m) or g2.canMove(m)
    return any_move


if __name__ == u'__main__':
    games = []
    correct = False
    while not correct:
        game_type = raw_input(u'Choose game type\n')
        if game_type == u'threes':
            games = [threes.Threes(save_game=False), threes.Threes(save_game=False)]
            correct = True
        elif game_type == u'2048':
            games = [g2048.G2048(save_game=False), g2048.G2048(save_game=False)]
            correct = True
        else:
            print u'You passed invalid game type - try again'

    seed = int(time.time())
    random.seed(seed)
    moves_dict = {u"w": MoveEnum.Up,
                  u"a": MoveEnum.Left,
                  u"s": MoveEnum.Down,
                  u"d": MoveEnum.Right}
    valid_inputs = [u'w', u'a', u's', u'd', u'i', u'j', u'k', u'l']
    # to make move in player1's board use WSAD and in player2's board use IKJL
    players = [u'Player1', u'Player2']
    curr_player = 0
    printer(games)
    print u"It's {}'s turn".format(players[curr_player])
    while is_any_move_valid(games[0], games[1]):
        user_input = raw_input(u"Choose move\n")
        if user_input in valid_inputs:
            ind = valid_inputs.index(user_input)
            i = int(ind > 3)
            move = moves_dict[valid_inputs[ind - 4] if i else valid_inputs[ind]]
            if games[i].canMove(move):
                games[i].makeMove(move)
                curr_player = (curr_player + 1) % 2
            else:
                print u"THE MOVE IS NOT VALID!"
        else:
            print u"INVALID COMMAND"
        print
        printer(games)
        print u"It's {}'s turn".format(players[curr_player])
    print u'Game has ended. The scores are:'
    print u'Player1 - {}, Player2 - {}'.format(games[0].stateInfo().score, games[1].stateInfo().score)
