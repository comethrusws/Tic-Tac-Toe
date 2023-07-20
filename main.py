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
        self.setStyleSheet("background-color: black;")

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
                self.buttons[i][j].setFixedSize(100, 100)
                self.buttons[i][j].setStyleSheet("QPushButton { background-color: black; color: yellow; }")
                grid_layout.addWidget(self.buttons[i][j], i, j)
                self.buttons[i][j].clicked.connect(lambda _, x=i, y=j: self.on_click(x, y))

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(255, 255, 255, 150), 8, Qt.SolidLine)
        painter.setPen(pen)

        # Draw hash overlay
        for i in range(1, 3):
            painter.drawLine(0, i * 100, 300, i * 100)
            painter.drawLine(i * 100, 0, i * 100, 300)

        # Draw winning line
        if self.winning_line:
            x1, y1 = self.winning_line[0]
            x2, y2 = self.winning_line[2]
            painter.setPen(QPen(Qt.white, 5))
            painter.drawLine((y1 + 0.5) * 100, (x1 + 0.5) * 100, (y2 + 0.5) * 100, (x2 + 0.5) * 100)

    def on_click(self, x, y):
        if self.board[x][y] == '':
            self.board[x][y] = self.current_player
            self.buttons[x][y].setText(self.current_player)
            self.buttons[x][y].setDisabled(True)  # Disable button after click

            if self.check_winner(x, y):
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
            x, y = random.choice(empty_cells)
            self.on_click(x, y)

    def check_winner(self, x, y):
        # Check rows, columns, and diagonals for a win
        winning_combinations = [
            [(i, j) for j in range(3)],  # Rows
            [(i, j) for i in range(3)],  # Columns
            [(i, i) for i in range(3)],  # Diagonal
            [(i, 2 - i) for i in range(3)]  # Anti-diagonal
        ]

        for combo in winning_combinations:
            if (x, y) in combo:
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
