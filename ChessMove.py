from ChessCell import *


class Move(object):
    """Класс-контейнер хода, не проверяет легетимность и т.п.
    Всего лишь удобный способ хранения и передачи хода.
    move(index) (index = 0, 1) возвращает ссылку на клетку,
    move[index] (index = 0, 1) возвращает позицию клетки,
    move[index] (index = 2, 3, 4) возвращает ссылки на фигуры потеряеные или приобретённые в этом ходу:
        index = 2: fig_taken
        index = 3: fig_pawn (в ходе превращения пешки)
        index = 4: fig_appeared (в ходе превращения пешки)"""
    from_ = ChessDescriptor(Cell)
    to_ = ChessDescriptor(Cell)
    optional = SmthOrFalseDescriptor(str)
    fig_taken = SmthOrFalseDescriptor(Piece)
    fig_pawn = SmthOrFalseDescriptor(Pawn)
    fig_appeared = SmthOrFalseDescriptor(Piece)

    def __init__(self, cell_from, cell_to, optional=False):
        """optional содержит 'passant', '0-0', '0-0-0', 'x' или 'permute'"""
        self.from_ = cell_from
        self.to_ = cell_to
        if optional not in ('passant', '0-0', '0-0-0', 'x', 'permute', False):
            raise AttributeError("optional should be in ('passant', '0-0', '0-0-0', 'x', 'permute', False)")
        self.optional = optional

        self.fig_taken = False
        self.fig_pawn = False
        self.fig_appeared = False

    def __getitem__(self, item: int):
        if item not in (0, 1, 2, 3, 4):
            raise ValueError('Index out of range')
        return {0: self.from_.position, 1: self.to_.position,
                2: self.fig_taken, 3: self.fig_pawn,
                4: self.fig_appeared}[item]

    def __call__(self, item):
        if item not in (0, 1):
            raise ValueError('Index out of range')
        return {0: self.from_, 1: self.to_}[item]

    def __eq__(self, other):
        # большой вопрос - резонно ли вообще так сравнивать ходы?? Желательно брать ход сразу из доступных
        if other.from_.position == self.from_.position and other.to_.position == self.to_.position and \
                other.optional == self.optional:
            return True
        return False

    def __bool__(self):
        return True

    def __repr__(self):
        if not self.optional:
            return str(self.from_.position) + ' ' + str(self.to_.position)
        elif self.castle_long():
            return '0-0-0'
        elif self.castle_short():
            return '0-0'
        else:
            return str(self.from_.position) + ' ' + str(self.to_.position) + ' ' + self.optional

    def cmp_tuple(self, tuple_):
        try:
            if self[0] == tuple_[0] and self[1] == tuple_[1]:
                return True
            return False
        except ValueError:
            raise ValueError(f'Impossible to compare move {self} with tuple_ {tuple_}')

    @staticmethod
    def search_move(moves, tuple_):
        for mv in moves:
            if mv.cmp_tuple(tuple_):
                return mv
        return False

    @staticmethod
    def filter_moves_first(moves, first):
        """Среди всех ходов moves возвращает tuple тех ходов, в которых ПЕРВАЯ позиция совпадает с искомой"""
        list_ = []
        for mv in moves:
            if mv[0] == first:
                list_.append(mv)
        return tuple(list_)

    def capture(self):
        if self.optional == 'x':
            return True
        return False

    def passant(self):
        if self.optional == 'passant':
            return True
        return False

    def castle_long(self):
        if self.optional == '0-0-0':
            return True
        return False

    def castle_short(self):
        if self.optional == '0-0':
            return True
        return False

    def permute(self):
        if self.optional == 'permute':
            return True
        return False

    def common_step(self):
        if not bool(self.optional):
            return True
        return False


'''
def move(self, move):                             # не проверяет легитимность хода, просто аппарат его совершения
    color1 = {0: 'White', 1: 'Black'}[self.turn % 2]
    player1 = self.players[color1]
    if move not in player1.possible_moves:
        print('An impossible or incorrect move')
        return False
    else:
        if move[0] == '0-0-0':                                                  # ход "длинная рокировка"
            if color1 == 'White':
                self.__step(['e1', 'c1'])
                self.__step(['a1', 'd1'])
                self.get_cell('c1').occupied.turn += 1
            elif color1 == 'Black':
                self.__step(['e8', 'c8'])
                self.__step(['a8', 'd8'])
                self.get_cell('c8').occupied.turn += 1
            else:
                return False
            self.turn += 1
            self.half_turn += 1
            self.move_list.append(move)
            return True
        elif move[0] == '0-0':                                                  # ход "короткая рокировка"
            if color1 == 'White':
                self.__step(['e1', 'g1'])
                self.__step(['h1', 'f1'])
                self.get_cell('g1').occupied.turn += 1
            elif color1 == 'Black':
                self.__step(['e8', 'g8'])
                self.__step(['h8', 'f8'])
                self.get_cell('g8').occupied.turn += 1
            else:
                return False
            self.turn += 1
            self.half_turn += 1
            self.move_list.append(move)
            return True
        cell1 = self.get_cell(move[0])
        piece1 = cell1.occupied
        if len(move) == 2:                                                      # обычный ход
            self.__step(move)
            self.half_turn += 1
            if isinstance(piece1, Pawn):
                self.half_turn = 0
        elif move[-1] == 'x':                                                   # ход "взятие вражеской фигуры"
            cell2 = self.get_cell(move[1])
            move.append(cell2.occupied)
            self.players[cell2.occupied.color].remove_piece(cell2.occupied)
            self.__capture(move)
            self.half_turn = 0
        elif move[-1] == 'passant':                                             # ход "взятие на проходе"
            cell3 = self.get_cell(move[1][0] + move[0][1])
            move.append(cell3.occupied)
            self.players[cell3.occupied.color].remove_piece(cell3.occupied)
            self.__capture(move)
            self.half_turn = 0
        else:
            return False
        piece1.turn += 1
        self.turn += 1
        if isinstance(piece1, Pawn):  # Поднимаем флажок превращения пешки, потом по флажку обращаемся к интерфейсу
            if piece1.cell.position()[1] == 1 or piece1.cell.position()[1] == 8:
                self.permutation = True
                return True
        self.move_list.append(move)
'''
