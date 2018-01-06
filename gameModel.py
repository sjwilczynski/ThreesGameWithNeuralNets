import enum
import random

WIDTH = 4
HEIGHT = 4


# Plansza =

# Nazwy klas (CapLet, CamelCase), nazwy metod (), pola klasy, argumenty metod
# NazwyKlas, nazwy_metod


class MoveEnum(enum.Enum):
    Left = 0,
    Up = 1,
    Right = 2,
    Down = 3


class Model:
    def canMove(self, move):
        raise NotImplemented

    def makeMove(self, move):
        # polityka poruszania (przesuń wszystko)
        # Wylosuj nowy pionek i połóż go na planszy
        raise NotImplemented

    def stateInfo(self):
        raise NotImplemented


class Threes(Model):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.highest = 3
        self.poss_nexts = [1, 2, 3]
        self.next = random.choice(self.poss_nexts)
        self._initBoard()

    def _initBoard(self):
        fields = [(x, y) for x in range(self.width) for y in range(self.height)]
        random.shuffle(fields)
        for x, y in fields[:9]:
            self.board[y][x] = random.choice(self.poss_nexts)

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
        if max(self.poss_nexts) * 8 < self.highest:
            self.poss_nexts += [self.poss_nexts[-1] * 3]
        self.next = random.choice(self.poss_nexts)

    def stateInfo(self):
        return self.board

    def _join(self, el1, el2):
        return el1 + el2

    def _canJoin(self, el1, el2):
        if el1 == el2 and el1 != 2 and el1 != 1:
            return True
        if min(el1, el2) == 1 and max(el1, el2) == 2:
            return True
        return False


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


t = Threes()
printer(t)

# for j in range(4):
#    for i in range(4):
#        put_piece(t, j, i, (1 + i) * (j+1))

# #put_piece(t, 0, 0, 0)
# printer(t)
# print(t.canMove(MoveEnum.Left))
# t.makeMove(MoveEnum.Left)
# #t.makeMove(MoveEnum.Left)
# #t.makeMove(MoveEnum.Right)
# printer(t)
moves_dict = {"w": MoveEnum.Up,
              "a": MoveEnum.Left,
              "s": MoveEnum.Down,
              "d": MoveEnum.Right}
while True:
    anymove = False
    for m in moves_dict.values():
        anymove = anymove or t.canMove(m)
    if not anymove:
        break
    w = input()
    if w in moves_dict:
        m = moves_dict[w]
        if t.canMove(m):
            t.makeMove(m)
        else:
            print("NOOOO!")
    print()
    printer(t)
