from PyQt5.QtWidgets import QDockWidget, QLabel, QWidget, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from board import Board
#from draughts import Draughts
from board import Board
import sys

class ScoreBoard(QDockWidget):

    piece = ""

    def __init__(self):
        super().__init__()
        self.initUI()
       # self.d1 = Draughts(self)


    def initUI(self):
        '''initiates ScoreBoard UI'''
        board = Board(self)
        piece = board.returnPiece()


        self.resize(50, 50)
        self.center()
        self.setWindowTitle('ScoreBoard')
        self.lbw = QLabel(self)
        self.lbl = QLabel(self)
        self.lbd = QLabel(self)
        self.lbw.move(10, 20)
        self.lbw.setText("wins = " + self.piece)
        self.lbl.move(10, 40)
        self.lbl.setText("loses = 2")
        self.lbd.move(10, 60)
        self.lbd.setText("draws = 3")
        self.lbl = QLabel(self)
        self.lbd = QLabel(self)

        self.button1 = QPushButton('Exit', self)
        self.button1.setToolTip('this is an example')
        # self.button1.resize(button1.sizeHint())
        self.button1.move(10, 50)
        self.button1.setGeometry(0, 100, 40, 20)
        self.button1.clicked.connect(self.on_click)


        self.show()

    def on_click(self, a):
        board = Board(self)
        board.resetGame()

    def center(self):
        '''centers the window on the screen'''




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