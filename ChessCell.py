from ChessPieces import *


class Cell(object):

    width = IntDescriptor()
    index = IntDescriptor()
    color = ColorDescriptor()
    piece = SmthOrFalseDescriptor(Piece)
    position = PositionDescriptor()
    attacked = ChessDescriptor(int)

    def __init__(self, index: int, board_width=8):
        self.width = board_width
        self.index = index
        self.piece = False
        self.color = ['Black', 'White'][(self.index // self.width + self.index % self.width) % 2]
        self.position = 'abcdefgh'[self.index % self.width] + '12345678'[self.index // self.width]
        self.attacked = [0, 0]

    def __repr__(self):
        return self.position

    def __str__(self):
        if self.piece:
            return str(self.piece)
        else:
            return {'Black': '▯', 'White': '▮'}[self.color]

    def __getitem__(self, item: int):
        return self.attacked[item]

    def coord(self):
        return [Notation[self.position[0]], int(self.position[1])-1]


# _____________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________
