from ChessMove import *


class Player(object):

    color = ColorDescriptor()
    pieces = ChessDescriptor(Piece)
    bot = BoolDescriptor()
    king = ChessDescriptor(King)
    possible_moves = ChessDescriptor(Move)

    def __init__(self, my_pieces, color, i_am_bot=False):
        self.color = color
        self.pieces = set(my_pieces)
        self.bot = i_am_bot
        self.king = None
        self.possible_moves = []

    def __repr__(self):
        return f'Player {self.color}'

    def add_piece(self, piece):
        if not piece:
            print('The piece is not existing')
            return False
        elif piece.color != self.color:
            print('Not the same color')
            return False
        self.pieces.add(piece)

    def remove_piece(self, piece):
        try:
            self.pieces.remove(piece)
        except ValueError:
            raise ValueError('Impossible to remove a non-existing piece')

    def reset_possible_moves(self):
        self.possible_moves = []
        return True

    def add_possible_moves(self, move_):
        self.possible_moves.append(move_)
        return True

    def print_possible_moves(self):
        if len(self.possible_moves) == 0:
            print('There are no possible moves, seems like checkmate :(')
            return False
        print('Possible moves are:')
        i = 0
        for move in self.possible_moves:
            i += 1
            print(move, end='   ')
            if i % 5 == 0:
                print()
        print()
        return True

    '''def search_for_possible_moves(self):
        pass

        for figure in self.pieces:
            for cell in figure.available_cells:
                if figure.cell == cell:
                    continue
                if cell.occupied != 0:
                    self.possible_moves.append([, ])
        '''

# _____________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________
