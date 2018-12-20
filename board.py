from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, pyqtSlot
from PyQt5.QtGui import QPainter, QColor


from piece import Piece

class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)
    playersTurn = pyqtSignal(int)
    blackCaptured = pyqtSignal(int)
    whiteCaptured = pyqtSignal(int)

    # todo set the board with and height in square
    boardWidth = 8
    boardHeight = 8
    Speed =300

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        # self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.resetGame()

        self.boardArray =[
                            [0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2],
                            [2, 0, 2, 0, 2, 0, 2, 0]
                          ]# 2d int/Piece array to story the state of the game
        self.printBoardArray()

        self.trackPieces = {}

        self.mousePressed = False
        self.firstClick = False
        self.secondClick = False
        self.curPos = ""
        self.nextPos = ""
        self.piece = 0
        self.reset = False
        self.turn = 1
        self.countBlackCaptures = 0
        self.countWhiteCaptures = 0


        list = {"1, 2": "#2039480", "2, 0": "#0980809", "3, 1": "#0980809", "1, 5": "#0980809", "5, 7": "#0980809", "6, 4": "#0980809", "9, 0": "#0980809"}
        print(list.get("3,1"))

        print(type(str(3) + ", " + str(1)))


    ''' Prints the board in the console. '''
    def printBoardArray(self):
        '''prints the boardArray in an arractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    ''' Converts the mousePressEvent to the (rows,col) in the board. Tells us which box was clicked. '''
    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        xPos = event.x()
        yPos = event.y()

        #print("X: ", xPos, "Y: ", yPos)
        #print("Col width: ", self.squareWidth(), "Row height: ", self.squareHeight())
        return str(int(yPos/self.squareHeight())) + ", " + str(int(xPos/self.squareWidth()))

    ''' Returns the width of the square '''
    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / Board.boardWidth

    ''' Returns the height of the square '''
    def squareHeight(self):
        '''returns the height of one squarein the board'''
        return self.contentsRect().height() / Board.boardHeight

    def start(self):
        '''starts game'''
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.resetGame()

        self.msg2Statusbar.emit(str("status message"))

        self.timer.start(Board.Speed, self)

    def pause(self):
        '''pauses game'''

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str("status message"))
        self.update()

    ''' All the main event happens here. Drawing the board and pieces. '''
    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

        ''' Checks if the mouse was pressed and the previous point and the next point is not empty.
            Reference variable is used to check the conditions. 
        '''

        if self.mousePressed and self.curPos != "" and self.nextPos != "":
            # Converts points (str) to list for easy access.
            curpos = [x.strip() for x in self.curPos.split(",")]
            nextpos = [x.strip() for x in self.nextPos.split(",")]

            temp = self.boardArray[int(curpos[0])][int(curpos[1])]
            self.boardArray[int(curpos[0])][int(curpos[1])] = 0
            self.boardArray[int(nextpos[0])][int(nextpos[1])] = temp
            self.printBoardArray()


            self.curPos = ""
            self.nextPos = ""

            painter.translate(int(nextpos[1]) * self.squareWidth(), int(nextpos[0]) * self.squareHeight())
            #painter.fillRect(0, 0, self.squareWidth(), self.squareHeight(), Qt.green)

            # painter.translate(3 * self.squareWidth(), 0 * self.squareHeight())

            if temp == 1:
                painter.setBrush(Qt.lightGray)
            elif temp == 2:
                painter.setBrush(Qt.black)
            radius = (self.squareWidth() - 2) / 2
            height = (self.squareHeight() - 2) / 2
            center = QPoint(radius, height)
            painter.drawEllipse(center, radius, height)
            self.update()
            self.mousePressed = False
            self.firstClick = False
            self.secondClick = False

    ''' All the mouse events happens here. Pieces and moved here and the capture is happening. '''
    def mousePressEvent(self, event):
        print("click location [", event.x(), ",", event.y(), "]")
        # todo you could call some game locig here
        print(type(event.x()), ": ", type(event.y()))
        pos = self.mousePosToColRow(event)
        #print(self.trackPieces)
        print("Pos: ", pos)

        ''' Variable used to check which piece was clicked. '''
        turn = [x.strip() for x in pos.split(",")]
        if self.boardArray[int(turn[0])][int(turn[1])] == self.turn:
            self.firstClick = True

        ''' Check if the previous point is not empty. '''
        if self.curPos != "":
            self.secondClick = True

        '''
        if self.firstClick:
            for points in self.trackPieces:
                if pos == points:
                    self.curPos = pos
                    break

        
        if self.curPos != "" and self.secondClick:
            for points in self.trackPieces: # Update the trackpieces after every move.
                if pos != points:
                    self.nextPos = pos
                else:
                    self.nextPos = ""
                    break
        '''

        #curpos = [x.strip() for x in self.curPos.split(",")]
        #print("Cur: ", curpos)

        #nextpos = [x.strip() for x in self.nextPos.split(",")]
        #print("Next: ", nextpos)

        ''' Condition is true only if the precious point is not null '''
        if self.firstClick and self.curPos == "":
            curpos = [x.strip() for x in pos.split(",")]
            if self.boardArray[int(curpos[0])][int(curpos[1])] != 0:
                #print("Cur: ", curpos)
                self.curPos = pos
                self.piece = self.boardArray[int(curpos[0])][int(curpos[1])]

        ''' If the second click is valid then we move forward with the piece movement and the capturing. '''
        if self.curPos != "" and self.secondClick:
            curpos = [x.strip() for x in self.curPos.split(",")]
            nextpos = [x.strip() for x in pos.split(",")]

            if self.boardArray[int(nextpos[0])][int(nextpos[1])] == 0: # Check for the boardarray number if moved.
                ''' Checks which piece was moved. '''
                if self.piece == 1: # Piece is white.
                    ''' if/elif statement to check if it is normal movement or capturing movement.
                        Deletes the captured piece if elif section. 
                    '''
                    if int(nextpos[0]) == (int(curpos[0]) + 1) and (int(nextpos[1]) >= 0 and int(nextpos[1]) <= 7 and (int(nextpos[1]) == (int(curpos[1]) - 1) or int(nextpos[1]) == (int(curpos[1]) + 1))):
                        self.nextPos = pos
                    elif int(nextpos[0]) == (int(curpos[0]) + 2) and (int(nextpos[1]) >= 0 and int(nextpos[1]) <= 7 and (int(nextpos[1]) == (int(curpos[1]) - 2) or int(nextpos[1]) == (int(curpos[1]) + 2))):
                        self.nextPos = pos
                        row = int(curpos[0]) + 1
                        if nextpos[1] > curpos[1]:
                            col = int(curpos[1]) + 1
                        else:
                            col = int(curpos[1]) - 1
                        print("Row: ", row)
                        print("Col: ", col)
                        self.boardArray[row][col] = 0
                        self.countBlackCaptures += 1
                        self.blackCaptured.emit(self.countBlackCaptures)
                    self.turn = 2 # Change player's turn for the scoreboard
                elif self.piece == 2: # Piece is black
                    if int(nextpos[0]) == (int(curpos[0]) - 1) and (int(nextpos[1]) >= 0 and int(nextpos[1]) <= 7 and (int(nextpos[1]) == (int(curpos[1]) - 1) or int(nextpos[1]) == (int(curpos[1]) + 1))):
                        self.nextPos = pos
                    elif int(nextpos[0]) == (int(curpos[0]) - 2) and (int(nextpos[1]) >= 0 and int(nextpos[1]) <= 7 and (int(nextpos[1]) == (int(curpos[1]) - 2) or int(nextpos[1]) == (int(curpos[1]) + 2))):
                        self.nextPos = pos
                        row = int(curpos[0]) - 1
                        if nextpos[1] > curpos[1]:
                            col = int(curpos[1]) + 1
                        else:
                            col = int(curpos[1]) - 1
                        print("Row: ", row)
                        print("Col: ", col)
                        self.boardArray[row][col] = 0
                        self.countWhiteCaptures += 1
                        self.whiteCaptured.emit(self.countWhiteCaptures)
                    self.turn = 1

            else:
                self.curPos = pos
            self.playersTurn.emit(self.turn)


            print("Cur: ", curpos)
            print("Next: ", nextpos)
            print("Piece: ", self.piece)


        '''
        if self.nextPos != "":
            self.trackPieces[self.nextPos] = self.trackPieces.pop(self.curPos)
        '''

        #print(self.trackPieces)
        if event.button() == Qt.LeftButton and self.curPos != "" and self.nextPos != "":
            #print(self.trackPieces)
            self.mousePressed = True
            self.update()

    def keyPressEvent(self, event):
        '''processes key press events if you would like to do any'''
        if not self.isStarted or self.curPiece.shape() == Piece.NoPiece:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        '''handles timer event'''
        #todo adapter this code to handle your timers

        if event.timerId() == self.timer.timerId():
            pass
        else:
            super(Board, self).timerEvent(event)

    ''' Resets the Game. '''
    def resetGame(self):
        '''clears pieces from the board'''
        # todo write code to reset game
        self.boardArray = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0]
        ]

        self.update()

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    ''' Draws the board. '''
    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # todo set the dafault colour of the brush
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                painter.save()
                if (row + col) % 2 == 0:
                    painter.setBrush(Qt.white)
                else:
                    painter.setBrush(Qt.green)
                colTransformation = col * self.squareWidth() # Todo set this value equal the transformation you would like in the column direction
                rowTransformation = row * self.squareHeight()  # Todo set this value equal the transformation you would like in the column direction
                painter.translate(colTransformation,rowTransformation)
                painter.fillRect(0, 0, self.squareWidth(), self.squareHeight(), painter.brush()) # Todo provide the required arguements
                painter.restore()
                # todo change the colour of the brush so that a checkered board is drawn

                #print("Col: ", col * self.squareWidth(), ",", "Row: ", self.squareHeight() * row)
                #print(row, " ", col)
                #print(rowTransformation, " ", colTransformation)


    ''' Draws the pieces on the board. '''
    def drawPieces(self, painter):
        '''draw the prices on the board'''
        colour = Qt.transparent

        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(col * self.squareWidth(), row * self.squareHeight())
                #Todo choose your colour and set the painter brush to the correct colour

                '''
                Incase if I need it
                
                if (row + col) % 2 == 0:
                    #painter.setBrush(Qt.black)
                else:
                    #painter.setBrush(Qt.lightGray)
                    
                '''
                piece = self.boardArray[row][col]
                if piece == 1:
                    painter.setBrush(Qt.lightGray)
                elif piece == 2:
                    painter.setBrush(Qt.black)

                if piece != 0:
                    radius = (self.squareWidth() - 2) / 2
                    height = (self.squareHeight() - 2) / 2
                    center = QPoint(radius, height)
                    painter.drawEllipse(center, radius, height)
                    # print(row, ",", col)
                    # self.returnColor(painter)
                    self.trackPieces[str(row) + ", " + str(col)] = painter.brush().color().name()


                '''
                if row <= 2 and row % 2 == 0 and col % 2 != 0:
                    painter.setBrush(Qt.lightGray)
                    radius = (self.squareWidth() - 2) / 2
                    center = QPoint(radius, radius - 2)
                    painter.drawEllipse(center, radius, radius - 4)
                    #print(row, ",", col)
                    #self.returnColor(painter)
                    self.trackPieces[str(row) + ", " + str(col)] = painter.brush().color().name()

                elif row <= 2 and row % 2 != 0 and  col % 2 == 0:
                    painter.setBrush(Qt.lightGray)
                    radius = (self.squareWidth() - 2) / 2
                    center = QPoint(radius, radius - 2)
                    painter.drawEllipse(center, radius, radius - 4)
                    #print(row, ",", col)
                    #self.returnColor(painter)
                    self.trackPieces[str(row) + ", " + str(col)] = painter.brush().color().name()

                if row >= 5 and row % 2 == 0 and col % 2 != 0:
                    painter.setBrush(Qt.black)
                    radius = (self.squareWidth() - 2) / 2
                    center = QPoint(radius, radius - 2)
                    painter.drawEllipse(center, radius, radius - 4)
                    #print(row, ",", col)
                    #self.returnColor(painter)
                    self.trackPieces[str(row) + ", " + str(col)] = painter.brush().color().name()

                elif row >= 5 and row % 2 != 0 and  col % 2 == 0:
                    painter.setBrush(Qt.black)
                    radius = (self.squareWidth() - 2) / 2
                    center = QPoint(radius, radius - 2)
                    painter.drawEllipse(center, radius, radius - 4)
                    #print(row, ",", col)
                    #self.returnColor(painter)
                    self.trackPieces[str(row) + ", " + str(col)] = painter.brush().color().name()
                '''

                # Todo draw some the pieces as elipses
                #radius = (self.squareWidth() - 2) / 2
                #center = QPoint(radius, radius)
                #painter.drawEllipse(center, radius, radius)
                painter.restore()


                #print(painter.brush().color().name())

                #print(x)

    def returnColor(self, painter):
        print(painter.brush().color().name())

    def returnPiece(self):
        return str(self.piece)

