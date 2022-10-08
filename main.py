from ChessBoard import *

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

gm = game_mode_classic
thinking_time = 200


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.state = 0
        self.Board = None
        self.cell_active = False
        self.moves_from_active_cell = None
        self.cells_to_move = []
        self.cells_to_passant = []
        self.change = 0
        self.imgEnt = QImage("Pictures/EnterFigure.png")
        self.imgMove = QImage("Pictures/MoveAvailable.png")
        self.imgAttack = QImage("Pictures/Attack.png")
        self.imgFrame = QImage("Pictures/Frame.png")
        self.timer = QTimer()
        self.turn0 = None
        self.timer.timeout.connect(self.if_move_done)

    def if_move_done(self):
        if self.Board.players[Colors[self.Board.turn % 2]].bot:
            bot_move = self.Board.bot_move()
            self.change = 1
            self.update()
            if self.Board.permutation:
                piece = {'q': 'Queen', 'r': 'Rook', 'b': 'Bishop', 'n': 'Knight'}
                self.Board.pawn_permutation(piece[bot_move[-1]])
            self.Board.look_for_cells_are_attacked()
            self.Board.move_creator()
            if len(self.Board.players[Colors[(self.Board.turn) % 2]].possible_moves) == 0:
                congrats(self.Board.players[Colors[(self.Board.turn + 1) % 2]])
            self.timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.state == 1:
            if self.change != 0:
                painter.drawImage(QRect(0, 0, 600, 600), chess[0])
                for cell in self.Board.cells:
                    cell_rectangle = QRect(cell.coord()[0] * 72 + 20, (7 - cell.coord()[1]) * 70 + 10, 72, 72)
                    if cell.piece:
                        painter.drawImage(cell_rectangle, cell.piece.image)
                    if cell == self.cell_active:
                        painter.drawImage(cell_rectangle, self.imgEnt)
                    elif cell in self.cells_to_move:
                        if not cell.piece:
                            painter.drawImage(cell_rectangle, self.imgMove)
                        else:
                            painter.drawImage(cell_rectangle, self.imgAttack)
                    elif cell in self.cells_to_passant:
                        painter.drawImage(cell_rectangle, self.imgAttack)
                if self.Board.someone_in_check:
                    king = self.Board.someone_in_check
                    cell_rectangle = QRect(king.coord()[0] * 72 + 20, (7 - king.coord()[1]) * 70 + 10, 72, 72)
                    painter.drawImage(cell_rectangle, self.imgAttack)
                self.change = 0
                if self.Board.permutation:
                    painter.drawImage(QRect(60, 220, 480, 160), self.imgFrame)
                    if self.Board.turn % 2 == 0:
                        painter.drawImage(QRect(92, 260, 80, 80), QImage("Pictures/wikipedia/wN.png"))
                        painter.drawImage(QRect(204, 260, 80, 80), QImage("Pictures/wikipedia/wB.png"))
                        painter.drawImage(QRect(316, 260, 80, 80), QImage("Pictures/wikipedia/wR.png"))
                        painter.drawImage(QRect(428, 260, 80, 80), QImage("Pictures/wikipedia/wQ.png"))
                    if self.Board.turn % 2 == 1:
                        painter.drawImage(QRect(92, 260, 80, 80), QImage("Pictures/wikipedia/bN.png"))
                        painter.drawImage(QRect(204, 260, 80, 80), QImage("Pictures/wikipedia/bB.png"))
                        painter.drawImage(QRect(316, 260, 80, 80), QImage("Pictures/wikipedia/bR.png"))
                        painter.drawImage(QRect(428, 260, 80, 80), QImage("Pictures/wikipedia/bQ.png"))
                self.timer.start(thinking_time)

    def mousePressEvent(self, event):
        if self.Board.players[Colors[self.Board.turn % 2]].bot:
            return None
        if self.state == 0:
            return None
        px, py = event.pos().x(), event.pos().y()
        if self.Board.permutation:
            piece_to_permute = None
            if px in range(92, 172) and py in range(260, 340):
                piece_to_permute = 'Knight'
            elif px in range(204, 284) and py in range(260, 340):
                piece_to_permute = 'Bishop'
            elif px in range(316, 396) and py in range(260, 340):
                piece_to_permute = 'Rook'
            elif px in range(428, 508) and py in range(260, 340):
                piece_to_permute = 'Queen'
            self.Board.pawn_permutation(piece_to_permute)
            self.Board.look_for_cells_are_attacked()
            self.Board.move_creator()
            self.change = 1
        else:
            if px in range(20, 596) and py in range(10, 570):
                x = (px-20)//72
                y = (py-10)//70
                cell_entered = self.Board([x, 7-y])
                self.change = 1
                if not self.cell_active:
                    if cell_entered.piece and cell_entered.piece.color == Colors[self.Board.turn % 2]:
                        self.cell_active = cell_entered
                        self.moves_from_active_cell = Move.filter_moves_first(
                            self.Board.players[Colors[self.Board.turn % 2]].possible_moves,
                            self.cell_active.position
                        )
                        self.cells_to_move, self.cells_to_passant = [], []
                        for move_ in self.moves_from_active_cell:
                            if move_.passant():
                                self.cells_to_passant.append(move_(1))
                            else:
                                self.cells_to_move.append(move_(1))
                    else:
                        self.cell_active = False
                        self.moves_from_active_cell = None
                        self.cells_to_move = []
                        self.cells_to_passant = []
                else:
                    if cell_entered in self.cells_to_move or cell_entered in self.cells_to_passant:
                        mv = Move.search_move(self.moves_from_active_cell,
                                              (self.cell_active.position, cell_entered.position))
                        print(mv)
                        if mv:
                            self.turn0 = self.Board.turn
                            self.Board.move(mv)
                            self.Board.look_for_cells_are_attacked()
                            self.Board.move_creator()
                            print(self.Board.encryption_forsyth_edwards())
                        self.cell_active = False
                        self.moves_from_active_cell = None
                        self.cells_to_move = []
                        self.cells_to_passant = []
                        if len(self.Board.players[Colors[(self.Board.turn) % 2]].possible_moves) == 0:
                            congrats(self.Board.players[Colors[(self.Board.turn + 1) % 2]])
                    else:
                        if cell_entered.piece and cell_entered.piece.color == Colors[self.Board.turn % 2]:
                            self.cell_active = cell_entered
                            self.moves_from_active_cell = Move.filter_moves_first(
                                self.Board.players[Colors[self.Board.turn % 2]].possible_moves,
                                self.cell_active.position
                            )
                            self.cells_to_move, self.cells_to_passant = [], []
                            for move_ in self.moves_from_active_cell:
                                if move_.passant():
                                    self.cells_to_passant.append(move_(1))
                                else:
                                    self.cells_to_move.append(move_(1))
                        else:
                            self.cell_active = False
                            self.moves_from_active_cell = None
                            self.cells_to_move = []
                            self.cells_to_passant = []
        self.update()


app = QApplication(sys.argv)
mainW = MainWindow()


def new_game():
    mainW.state = 1
    mainW.change = 1
    mainW.Board = Board(gm, player2bot=True)
    mainW.Board.look_for_cells_are_attacked()
    mainW.Board.move_creator()
    btn1.hide()
    mainW.update()
    print('Game starts')


def main_menu():
    mainW.state = 0
    btn1.show()


def congrats(player):
    r = QMessageBox.question(mainW, "Congrats", str(player)+' won the Game, congratulations!', QMessageBox.Ok, QMessageBox.Ok)
    print('Game ends')
    if r == QMessageBox.Ok:
        main_menu()


mainW.resize(600, 600)
mainW.setWindowTitle("Chess")

chess = [QImage("Pictures/ChessBoard.png")]
print(chess)
btn1 = QPushButton(mainW)
btn1.move(200, 100)
btn1.setText("New Game")
btn1.clicked.connect(new_game)
btn1.show()
mainW.show()
sys.exit(app.exec_())
