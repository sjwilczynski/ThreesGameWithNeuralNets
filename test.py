from threes import *


def printer(curr_game):
    board = curr_game.stateInfo()
    for ys in board:
        for el in ys:
            x = "."
            if el != 0:
                x = el
            print("{:>4}".format(x), end=" ")
        print("")


def put_piece(t, x, y, el):
    t.board[y][x] = el


if __name__ == '__main__':
    game = Threes()
    filename = getFilename()
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
        w = input()
        if w in moves_dict:
            m = moves_dict[w]
            if game.canMove(m):
                if game.save_game:
                    saveState(game, m.value, filename)
                game.turn_counter += 1
                game.makeMove(m)
            else:
                print("THE MOVE IS NOT VALID!")
        else:
            print("INVALID COMMAND")
        print()
        printer(game)
