import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QWidget, QGridLayout
from PyQt5.QtGui import QIcon, QFont, QPainter, QPen, QColor
from PyQt5.QtCore import Qt

class TicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(100, 100, 500, 500)
        self.setWindowIcon(QIcon("Resources\logo.png"))
        self.setToolTip("Tic Tac Toe")

        self.current_player = 'X'
        self.board = [[''] * 3 for _ in range(3)]
        self.winning_line = []
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        self.buttons = [[QPushButton('', self) for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setFont(QFont('Arial', 30))
                self.buttons[i][j].setFixedSize(150, 150)  
                self.buttons[i][j].setStyleSheet("QPushButton { background-color: black; color: red; }")
                grid_layout.addWidget(self.buttons[i][j], i, j)
                self.buttons[i][j].clicked.connect(lambda _, row=i, col=j: self.on_click(row, col))

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(255, 255, 255, 150), 8, Qt.SolidLine)
        painter.setPen(pen)

       
        for i in range(1, 3):
            painter.drawLine(0, i * 150, 450, i * 150)
            painter.drawLine(i * 150, 0, i * 150, 450)

        
        if self.winning_line:
            x1, y1 = self.winning_line[0]
            x2, y2 = self.winning_line[2]
            painter.setPen(QPen(Qt.white, 5))
            painter.drawLine(int((y1 + 0.5) * 150), int((x1 + 0.5) * 150), int((y2 + 0.5) * 150), int((x2 + 0.5) * 150))

    def on_click(self, row, col):
        if self.board[row][col] == '':
            self.board[row][col] = self.current_player
            self.buttons[row][col].setText(self.current_player)
            self.buttons[row][col].setDisabled(True)  

            if self.check_winner(row, col):
                self.show_winner_message()
                self.reset_game()
                return

            if self.check_draw():
                self.show_draw_message()
                self.reset_game()
                return

            self.current_player = 'X' if self.current_player == 'O' else 'O'
            if self.current_player == 'O':
                self.ai_move()

    def ai_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.on_click(row, col)

    def check_winner(self, row, col):
        # check rows ra cloumn for wins
        winning_combinations = [
            [(row, j) for j in range(3)],  #rows
            [(i, col) for i in range(3)],  #columns
            [(i, i) for i in range(3)],  # diagonal
            [(i, 2 - i) for i in range(3)]  #antidiagonal
        ]

        for combo in winning_combinations:
            if (row, col) in combo:
                if all(self.board[i][j] == self.current_player for i, j in combo):
                    self.winning_line = combo
                    return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))

    def show_winner_message(self):
        QMessageBox.information(self, "Game Over", f"Player {self.current_player} wins!")

    def show_draw_message(self):
        QMessageBox.information(self, "Game Over", "It's a draw!")

    def reset_game(self):
        self.current_player = 'X'
        self.board = [[''] * 3 for _ in range(3)]
        self.winning_line = []

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText('')
                self.buttons[i][j].setDisabled(False)

        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TicTacToe()
    window.show()
    sys.exit(app.exec_())