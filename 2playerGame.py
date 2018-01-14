import threes
import g2048
from gameModel import *
import random
import time


def printer(curr_games):
    board1 = curr_games[0].board
    board2 = curr_games[1].board
    size = board1.shape[0]
    for j in range(size):
        r1 = board1[j]
        r2 = board2[j]
        print_row(r1)
        print("", end=" | ")
        print_row(r2)
        print("")


def print_row(row):
    for el in row:
        x = "."
        if el != 0:
            x = el
        print("{:>4}".format(x), end=" ")


def is_any_move_valid(g1, g2):
    any_move = False
    for m in moves_dict.values():
        any_move = any_move or g1.canMove(m) or g2.canMove(m)
    return any_move


if __name__ == '__main__':
    games = []
    correct = False
    while not correct:
        game_type = input('Choose game type\n')
        if game_type == 'threes':
            games = [threes.Threes(save_game=False), threes.Threes(save_game=False)]
            correct = True
        elif game_type == '2048':
            games = [g2048.G2048(save_game=False), g2048.G2048(save_game=False)]
            correct = True
        else:
            print('You passed invalid game type - try again')

    seed = int(time.time())
    random.seed(seed)
    moves_dict = {"w": MoveEnum.Up,
                  "a": MoveEnum.Left,
                  "s": MoveEnum.Down,
                  "d": MoveEnum.Right}
    valid_inputs = ['w', 'a', 's', 'd', 'i', 'j', 'k', 'l']
    # to make move in player1's board use WSAD and in player2's board use IKJL
    players = ['Player1', 'Player2']
    curr_player = 0
    printer(games)
    print("It's {}'s turn".format(players[curr_player]))
    while is_any_move_valid(games[0], games[1]):
        user_input = input("Choose move\n")
        if user_input in valid_inputs:
            ind = valid_inputs.index(user_input)
            print(ind)
            i = int(ind > 3)
            move = moves_dict[valid_inputs[ind - 4] if i else valid_inputs[ind]]
            if games[i].canMove(move):
                games[i].turn_counter += 1
                games[i].makeMove(move)
                curr_player = (curr_player + 1) % 2
            else:
                print("THE MOVE IS NOT VALID!")
        else:
            print("INVALID COMMAND")
        print()
        printer(games)
        print("It's {}'s turn".format(players[curr_player]))
    print('Game has ended. The scores are:')
    print('Player1 - {}, Player2 - {}'.format(games[0].stateInfo().score, games[1].stateInfo().score))
