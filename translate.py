from __future__ import absolute_import
import argparse
from threes import *
from io import open

import random

parser = argparse.ArgumentParser()
parser.add_argument(u"file", help=u"file to translate data")
args = parser.parse_args()

filename = args.file

f = open(filename)
seed = int(f.readline())
random.seed(seed)
game = Threes()

file = u''
if game.save_game:
    filename = getFilename()
    file = open(filename, u'a+')
    file.write(unicode(seed) + u'\n')

moves_dict = {MoveEnum.Up.value: MoveEnum.Up,
              MoveEnum.Left.value : MoveEnum.Left,
              MoveEnum.Down.value : MoveEnum.Down,
              MoveEnum.Right.value : MoveEnum.Right}
while True:
    any_move = False
    for m in moves_dict.values():
        any_move = any_move or game.canMove(m)
    if not any_move:
        break
    w = int(f.readline().split(',')[2])
    if w in moves_dict:
        m = moves_dict[w]
        if game.canMove(m):
            if game.save_game:
                saveState(game, m, file)
            game.turn_counter += 1
            game.makeMove(m)
        else:
            print u"THE MOVE IS NOT VALID!"
    else:
        print u"INVALID COMMAND"
        print w
    print
if game.save_game:
    file.close()




f.close()
