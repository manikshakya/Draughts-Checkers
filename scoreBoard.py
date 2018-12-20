from PyQt5.QtWidgets import QDockWidget, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from board import Board
#from draughts import Draughts
import sys

class ScoreBoard(QDockWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
       # self.d1 = Draughts(self)


    def initUI(self):
        '''initiates ScoreBoard UI'''

        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()


        self.player = QLabel(self)
        self.blackCaptured = QLabel(self)
        self.whiteCaptured = QLabel(self)

        self.player.move(10, 20)
        self.player.setText("Current Player: White")

        self.blackCaptured.move(10, 40)
        self.blackCaptured.setText("Black Captured: 0")

        self.whiteCaptured.move(10, 60)
        self.whiteCaptured.setText("White Captured = 0")


        #self.lbl = QLabel(self)
        #self.lbd = QLabel(self)

        self.button1 = QPushButton('Exit', self)
        self.button1.setToolTip('this is an example')
        # self.button1.resize(button1.sizeHint())
        self.button1.move(10, 50)
        self.button1.setGeometry(0, 100, 40, 20)
        self.button1.clicked.connect(self.on_click)


        self.mainLayout.addWidget(self.player)
        self.mainLayout.addWidget(self.blackCaptured)
        self.mainLayout.addWidget(self.whiteCaptured)
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)
        self.show()

    def on_click(self, a):
        board = Board(self)
        board.resetGame()

    def center(self):
        '''centers the window on the screen'''

    def make_connection(self, board):
        board.playersTurn.connect(self.viewTurns)

        board.blackCaptured.connect(self.viewBlackCaptured)
        board.whiteCaptured.connect(self.viewWhiteCaptured)

    @pyqtSlot(int)
    def viewTurns(self, turn):
        color = ""
        if turn == 1:
            color = "White"
        elif turn == 2:
            color = "Black"
        self.player.setText("Current Player: " + color)
        print("Turn: " + color)

    @pyqtSlot(int)
    def viewBlackCaptured(self, countBlack):
        self.blackCaptured.setText("Black Captured: " + str(countBlack))

    @pyqtSlot(int)
    def viewWhiteCaptured(self, countWhite):
        self.whiteCaptured.setText("White Captured: " + str(countWhite))



"""
from PyQt5.QtWidgets import QDockWidget
from board import Board
import sys

class ScoreBoard(QDockWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        self.show()

    def center(self):
        '''centers the window on the screen'''

"""