from enum import Enum


class Pieces(Enum):
    EMPTY = "*"
    ROOK = "ROOK"
    QUEEN = "QUEEN"
    KING = "KING"
    KNIGHT = "KNIGHT"
    BISHOP = "BISHOP"
    PAWN = "PAWN"

    def print_me(self):
        print(self.value[0], end="")


class Color(Enum):
    BLACK = 2  # DOWN
    WHITE = 1  # UP
    DEF = 0


def get_positions_for_figure(figure, x, y, i):
    return {
        Pieces.ROOK: [(i + x, y), (x - i, y), (x, y + i), (x, y - i)],
        Pieces.BISHOP: [(i + x, i + y), (x - i, i + y), (x - i, y - i), (x + i, y - i)],
        Pieces.QUEEN: [(i + x, i + y), (x - i, i + y), (x - i, y - i), (x + i, y - i),
                       (i + x, y), (x - i, y), (x, y + i), (x, y - i)],
        Pieces.KNIGHT: [(x + k, y + l) for k in [-2, 2] for l in [-1, 1]] +
                       [(x + l, y + k) for k in [-2, 2] for l in [-1, 1]],
        Pieces.KING: [(x + l, y + k) for l in [-1, 0, 1] for k in [-1, 0, 1] if l != 0 or k != 0],
        Pieces.PAWN: [(x + l, y + k) for k in [-1, 1] for l in [-1, 1]] +
                     [(x - 1, y), (x - 2, y), (x + 1, y), (x + 2, y)]
    }[figure]


class Board:
    # bottom left == black
    def __init__(self):
        self.board = [[(Pieces.EMPTY, Color.DEF)] * 8 for i in range(8)]
        self.setup_board()

    def setup_board(self):
        with open("configuration.txt") as f:
            lines = f.readlines()
            for line in lines:
                x, y, piece = line.rstrip().split()
                self.board[0][int(x) - 1] = (Pieces(piece), Color.WHITE)
                self.board[1][int(x) - 1] = (Pieces.PAWN, Color.WHITE)

                self.board[7][int(x) - 1] = (Pieces(piece), Color.BLACK)
                self.board[6][int(x) - 1] = (Pieces.PAWN, Color.BLACK)

    def print_board(self):
        for i in self.board:
            for piece, color in i:
                piece.print_me()
                print(" ", end="")
            print()

    def move_figure(self, x, y, new_x, new_y):
        assert 1 <= x <= 8
        assert 1 <= y <= 8
        assert 1 <= new_y <= 8
        assert 1 <= new_x <= 8

        figure, color = self.board[x - 1][y - 1]
        figure_to, color_to = self.board[new_x - 1][new_y - 1]
        all_combs = self.get_possible_moves(x, y)

        assert color != color_to  # Move not allowed: some other figure of same color on destination

        if (new_x - 1, new_y - 1) in all_combs:

            self.board[x - 1][y - 1] = (Pieces.EMPTY, Color.DEF)
            self.board[new_x - 1][new_y - 1] = (figure, color)
        else:
            assert False  # Move not allowed

    def get_possible_moves(self, x, y):
        assert 1 <= x <= 8
        assert 1 <= y <= 8

        possible_set = set()
        piece, color = self.board[x - 1][y - 1]

        assert piece != Pieces.EMPTY

        if piece in [Pieces.BISHOP, Pieces.ROOK, Pieces.QUEEN]:
            path_not_blocked = [True] * 4
            for i in range(1, 8):
                t = get_positions_for_figure(piece, x, y, i)

                for j, (p, k) in enumerate(t):
                    if 8 >= p >= 1 and 8 >= k >= 1:
                        if self.board[p - 1][k - 1][1] == color:
                            path_not_blocked[j] = False
                        if path_not_blocked[j]:
                            possible_set.add((p, k))

        if piece in [Pieces.KNIGHT, Pieces.KING, Pieces.PAWN]:
            t = get_positions_for_figure(piece, x, y, 0)
            for j, k in t:
                if 8 >= j >= 1 and 8 >= k >= 1:
                    if self.board[j - 1][k - 1][1] != color:
                        possible_set.add((j, k))

        return [(j - 1, k - 1) for j, k in possible_set]

    def print_possible_moves(self, x, y):

        combs = self.get_possible_moves(x, y)
        print("_" * 15)
        for i in range(8):
            for j in range(8):
                poss_fig, poss_col = self.board[i][j]

                if (i, j) in combs:
                    print("X ", end="")
                else:
                    poss_fig.print_me()
                    print(" ", end="")
            print()

        print("_" * 15)


class Player:
    def __init__(self, color):
        pass


def main():
    b = Board()
    b.print_board()

    b.move_figure(7, 1, 5, 1)
    b.move_figure(7, 3, 5, 3)
    # b.move_figure(7, 2, 5, 2)
    # b.move_figure(7, 4, 5, 4)

    b.print_possible_moves(8, 4)


if __name__ == '__main__':
    main()
