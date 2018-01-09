import enum
import random


WIDTH = 4
HEIGHT = 4
SPECIAL_DEMOTION = 3


class MoveEnum(enum.Enum):
    Left = 0,
    Up = 1,
    Right = 2,
    Down = 3


class Model:
    def canMove(self, move):
        raise NotImplemented

    def makeMove(self, move):
        raise NotImplemented

    def stateInfo(self):
        raise NotImplemented


class Threes(Model):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.highest = 3
        self.highest_power = 0
        self.poss_nexts = [(i % 3) + 1 for i in range(12)]
        random.shuffle(self.poss_nexts)
        self.poss_index = 0
        self.next = self._getNext()
        self._initBoard()
        self.current_score = 0

    def _initBoard(self):
        fields = [(x, y) for x in range(self.width) for y in range(self.height)]
        random.shuffle(fields)
        for x, y in fields[:9]:
            self.board[y][x] = random.choice(range(1, 4))

    def _canMove(self, xs, ys, x_mod, y_mod):
        for y in ys:
            for x in xs:
                if self.board[y][x] != 0:
                    if self._canJoin(self.board[y + y_mod][x + x_mod], self.board[y][x]) \
                            or self.board[y + y_mod][x + x_mod] == 0:
                        return True
        return False

    def canMove(self, move):
        xs = [i for i in range(self.width)]
        ys = [i for i in range(self.height)]
        if move == MoveEnum.Left:
            return self._canMove(xs[1:], ys, -1, 0)
        if move == MoveEnum.Up:
            return self._canMove(xs, ys[1:], 0, -1)
        if move == MoveEnum.Right:
            return self._canMove(xs[:-1], ys, 1, 0)
        if move == MoveEnum.Down:
            return self._canMove(xs, ys[:-1], 0, 1)

    def _makeMove(self, xs, ys, x_mod, y_mod):
        x_moved = set()
        y_moved = set()
        for y in ys:
            for x in xs:
                if self.board[y][x] != 0:
                    # if self.board[y + y_mod][x + x_mod] == 0:
                    #    self.board[y+y_mod][x+x_mod] = self.board[y][x]
                    #    self.board[y][x] = 0
                    #                   print(x + x_mod, y + y_mod)
                    if self.board[y + y_mod][x + x_mod] == 0 \
                            or self._canJoin(self.board[y + y_mod][x + x_mod], self.board[y][x]):
                        self.board[y + y_mod][x + x_mod] = self._join(self.board[y + y_mod][x + x_mod],
                                                                      self.board[y][x])
                        self.board[y][x] = 0
                        x_moved.add(x)
                        y_moved.add(y)
        return list(x_moved), list(y_moved)

    def makeMove(self, move):
        xs = [i for i in range(self.width)]
        ys = [i for i in range(self.height)]
        if move == MoveEnum.Left:
            _, y_moved = self._makeMove(xs[1:], ys, -1, 0)
            self.board[random.choice(y_moved)][self.width - 1] = self.next
        if move == MoveEnum.Up:
            x_moved, _ = self._makeMove(xs, ys[1:], 0, -1)
            self.board[self.height - 1][random.choice(x_moved)] = self.next
        if move == MoveEnum.Right:
            _, y_moved = self._makeMove(xs[::-1][1:], ys, 1, 0)
            self.board[random.choice(y_moved)][0] = self.next
        if move == MoveEnum.Down:
            x_moved, _ = self._makeMove(xs, ys[::-1][1:], 0, 1)
            self.board[0][random.choice(x_moved)] = self.next

        self.highest = max(max(x) for x in self.board)
        if self.highest > 3 * 2 ** self.highest_power:
            self.highest_power += 1
        self.next = self._getNext()
        self.current_score = self.score()

    def stateInfo(self):
        return self.board

    def _getNext(self):
        random_list = list(range(21))
        r = random.choice(random_list)
        if r == 0 and self.highest_power > SPECIAL_DEMOTION:
            p = random.choice(range(1, 1 + self.highest_power - SPECIAL_DEMOTION))
            return 3 * 2 ** p
        result = self.poss_nexts[self.poss_index]
        self.poss_index += 1
        if self.poss_index >= len(self.poss_nexts):
            random.shuffle(self.poss_nexts)
            self.poss_index = 0
        return result

    def _join(self, el1, el2):
        return el1 + el2

    def _canJoin(self, el1, el2):
        if el1 == el2 and el1 != 2 and el1 != 1:
            return True
        if min(el1, el2) == 1 and max(el1, el2) == 2:
            return True
        return False

    def score(self):
        '''
        Calculates the score of the current game state - TODO
        '''
        return 0

    def saveState(self):
        '''
        This function saves the game state for future learning.
        State of the board, next value, current score and performed moved are saved.
        '''
        pass


def printer(t):
    b = t.stateInfo()
    for ys in b:
        for el in ys:
            x = "."
            if el != 0:
                x = el
            print("{:>4}".format(x), end=" ")
        print("")


def put_piece(t, x, y, el):
    t.board[y][x] = el


game = Threes()
printer(game)

moves_dict = {"w": MoveEnum.Up,
              "a": MoveEnum.Left,
              "s": MoveEnum.Down,
              "d": MoveEnum.Right}
while True:
    anymove = False
    for m in moves_dict.values():
        anymove = anymove or game.canMove(m)
    if not anymove:
        break
    w = input()
    game.saveState()
    if w in moves_dict:
        m = moves_dict[w]
        if game.canMove(m):
            game.makeMove(m)
        else:
            print("THE MOVE IS NOT VALID!")
    print()
    printer(game)