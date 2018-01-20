
import argparse
from threes3 import *
from io import open

import random

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to translate data")
args = parser.parse_args()

filename = args.file

f = open(filename)
seed = int(f.readline())
random.seed(seed)
game = Threes()

file = ''
if game.save_game:
    filename = getFilename()
    file = open(filename, 'a+')
    file.write(str(seed) + '\n')

moves_dict = {MoveEnum.Up.value: MoveEnum.Up,
              MoveEnum.Left.value : MoveEnum.Left,
              MoveEnum.Down.value : MoveEnum.Down,
              MoveEnum.Right.value : MoveEnum.Right}

def read_next_data():
    first_line = f.readline()
    if not first_line:
        file.close()
        exit(0)
    if first_line[-2] != ']':
        first_line += f.readline()
    return first_line

while True:
    any_move = False
    for m in list(moves_dict.values()):
        any_move = any_move or game.canMove(m)
    if not any_move:
        break
    w = int(read_next_data().split(',')[-1][:-2]) 
    if w in moves_dict:
        m = moves_dict[w]
        if game.canMove(m):
            if game.save_game:
                saveState(game, m, file)
            game.turn_counter += 1
            game.makeMove(m)
        else:
            print(w)
    else:
        print(w)
if game.save_game:
    file.close()




f.close()
