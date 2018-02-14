from __future__ import absolute_import

from AIModels import *
from threes import *

TEST_NUM = 1

def printer(curr_game):
    board = curr_game.stateInfo().board
    for ys in board:
        for el in ys:
            x = u"."
            if el != 0:
                x = el
            print u"{:>4}".format(x),
        print u""


def put_piece(t, x, y, el):
    t.board[y][x] = el


if TEST_NUM == 0 and __name__ == u'__main__':
    seed = int(time.time())
    random.seed(seed)
    game = Threes()
    file = u''
    if game.save_game:
        filename = getFilename()
        file = open(filename, u'a+')
        file.write(unicode(seed) + u'\n')
        file.flush()
    printer(game)
    moves_dict = {u"w": MoveEnum.Up,
                  u"a": MoveEnum.Left,
                  u"s": MoveEnum.Down,
                  u"d": MoveEnum.Right}
    while True:
        any_move = False
        for m in moves_dict.values():
            any_move = any_move or game.canMove(m)
        if not any_move:
            break
        w = raw_input(u"Choose move\n")
        if w in moves_dict:
            m = moves_dict[w]
            if game.canMove(m):
                if game.save_game:
                    saveState(game, m, file)
                game.makeMove(m)
            else:
                print u"THE MOVE IS NOT VALID!"
        else:
            print u"INVALID COMMAND"
        print
        printer(game)
    if game.save_game:
        file.close()

if TEST_NUM == 1 and __name__ == u'__main__':
    game = Threes(save_game=False)
    ai = RandomAI(game)
    scores, move_count, highs = AIModel.test_ai(ai, 1, verbose=True)
    print move_count
    print np.mean(scores), np.mean(highs)
