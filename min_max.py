import copy

from g2048 import *
from test import *

game = Threes()
printer(game)
game2 = copy.deepcopy(game)
game2.makeMove(MoveEnum.Up)
print()
printer(game)
print()
printer(game2)


def count_non_empty(board):
    result = 0
    for row in board:
        for el in row:
            if el > 0:
                result += 1
    return result


def board_modifier(x, y):
    result = 1
    if x == 0 or x == 3:
        result *= 1.5
    if y == 0 or y == 3:
        result *= 1.5
    return result


def heuristic_value(board):
    result = 0
    x, y = 0, 0
    for row in board:
        x = 0
        for el in row:
            factor = Threes._scoringFactor(el)
            if factor > 0:
                result += (3 ** factor) * board_modifier(x, y)
            x += 1
        y += 1
    return result / count_non_empty(board)


def rec_best_move(model, moves, depth):
    if depth == 0:
        return model
    score = 0
    result = model
    for move in moves:
        if not model.canMove(move):
            continue
        model_c = copy.deepcopy(model)
        model_c.makeMove(move)
        model_c = rec_best_move(model_c, moves, depth - 1)
        new_score = heuristic_value(model_c.stateInfo().board)
        if new_score > score:
            result = model_c
            score = new_score
    return result


def best_move(model, moves):
    result = None
    score = 0
    for move in moves:
        if not model.canMove(move):
            continue
        model_c = copy.deepcopy(model)
        model_c.makeMove(move)
        model_c = rec_best_move(model_c, moves, 3)
        new_score = heuristic_value(model_c.stateInfo().board)
        if new_score > score:
            score = new_score
            result = move
    return result


if __name__ == '__main__':
    seed = int(time.time())
    random.seed(seed)
    game = G2048()
    printer(game)
    moves_dict = {"w": MoveEnum.Up,
                  "a": MoveEnum.Left,
                  "s": MoveEnum.Down,
                  "d": MoveEnum.Right}
    while True:
        any_move = False
        for m in moves_dict.values():
            any_move = any_move or game.canMove(m)
        if not any_move:
            break
        m = best_move(game, moves_dict.values())
        game.turn_counter += 1
        game.makeMove(m)
        print()
        printer(game)
        print(game.stateInfo().score)