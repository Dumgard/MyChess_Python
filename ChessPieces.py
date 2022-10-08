from ChessDescriptors import *

from PyQt5.QtGui import QImage

Notation = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10        # etc.
}


class Piece(object):
    """Класс шахматных фигур. Обладает цветом, соответствующей фигуре клеткой на доске, ссылкой на эту доску, etc."""

    color = ColorDescriptor()
    position = PositionDescriptor()
    turn = IntDescriptor()

    def __init__(self, color, position=None):
        self.color = color
        self.position = position
        self.turn = 0
        self.available_cells = set()

    def __bool__(self):
        return True

    def reset_available_cells(self):
        self.available_cells = set()
        return True

    def add_available_cells(self, cell_to_move_on):
        self.available_cells.add(cell_to_move_on)
        return

    def rmv_available_cells(self, cell_to_remove):
        self.available_cells.remove(cell_to_remove)
        return True

    def restrict_available_cells(self, set_to_intersect_with):
        if isinstance(set_to_intersect_with, list):
            set_to_intersect_with = set(set_to_intersect_with)
        self.available_cells.intersection_update(set_to_intersect_with)
        return self.available_cells

    def coord(self):
        return [Notation[self.position[0]], int(self.position[1]) - 1]


class Pawn(Piece):

    bounded = SmthOrFalseDescriptor(Piece)
    weight = IntDescriptor()
    images = {'White': QImage("Pictures/wikipedia/wP.png"), 'Black': QImage("Pictures/wikipedia/bP.png")}

    def __init__(self, color, position=None):
        super().__init__(color, position)
        self.bounded = False
        self.weight = 1
        self.image = self.__class__.images[self.color]

    def __str__(self):
        if self.color == 'White':
            return '♟'
        else:
            return '♙'

    def __repr__(self):
        return 'Pawn' + ' ' + self.position


class Bishop(Piece):

    bounded = SmthOrFalseDescriptor(Piece)
    weight = IntDescriptor()

    def __init__(self, color, position=None):
        super().__init__(color, position)
        self.bounded = False
        self.weight = 3
        if self.color == 'White':
            self.image = QImage("Pictures/wikipedia/wB.png")
        else:
            self.image = QImage("Pictures/wikipedia/bB.png")

    def __str__(self):
        if self.color == 'White':
            return '♝'
        else:
            return '♗'

    def __repr__(self):
        return 'Bishop' + ' ' + self.position


class Knight(Piece):

    bounded = SmthOrFalseDescriptor(Piece)
    weight = IntDescriptor()

    def __init__(self, color, position=None):
        super().__init__(color, position)
        self.bounded = False
        self.weight = 3
        if self.color == 'White':
            self.image = QImage("Pictures/wikipedia/wN.png")
        else:
            self.image = QImage("Pictures/wikipedia/bN.png")

    def __str__(self):
        if self.color == 'White':
            return '♞'
        else:
            return '♘'

    def __repr__(self):
        return 'Knight' + ' ' + self.position


class Rook(Piece):

    bounded = SmthOrFalseDescriptor(Piece)
    weight = IntDescriptor()

    def __init__(self, color, position=None):
        super().__init__(color, position)
        self.bounded = False
        self.weight = 5
        if self.color == 'White':
            self.image = QImage("Pictures/wikipedia/wR.png")
        else:
            self.image = QImage("Pictures/wikipedia/bR.png")

    def __str__(self):
        if self.color == 'White':
            return '♜'
        else:
            return '♖'

    def __repr__(self):
        return 'Rook' + ' ' + self.position


class Queen(Piece):

    bounded = SmthOrFalseDescriptor(Piece)
    weight = IntDescriptor()

    def __init__(self, color, position=None):
        super().__init__(color, position)
        self.bounded = False
        self.weight = 9
        if self.color == 'White':
            self.image = QImage("Pictures/wikipedia/wQ.png")
        else:
            self.image = QImage("Pictures/wikipedia/bQ.png")

    def __str__(self):
        if self.color == 'White':
            return '♛'
        else:
            return '♕'

    def __repr__(self):
        return 'Queen' + ' ' + self.position


class King(Piece):

    in_check = SmthOrFalseDescriptor(Piece)
    weight = IntDescriptor()

    def __init__(self, color, position=None):
        super().__init__(color, position)
        self.in_check = False
        self.weight = 0
        if self.color == 'White':
            self.image = QImage("Pictures/wikipedia/wK.png")
        else:
            self.image = QImage("Pictures/wikipedia/bK.png")

    def __str__(self):
        if self.color == 'White':
            return '♚'
        else:
            return '♔'

    def __repr__(self):
        return 'King' + ' ' + self.position


'''
class VoidPiece(Piece):
    def __init__(self, board, cell):
        super().__init__(board, cell)
        self.color = None
'''
