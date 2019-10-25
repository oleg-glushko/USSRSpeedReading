# The main idea of this program is to generate tables with the specific
# size of an edge, e.g., 5 cm per cell. You can also change the number
# of cells in rows/columns, the width of a line and the size of a font.
# Just modify constants placed in the top of this code.
# 
# You can control this app by keyboard hot-keys: press 'Space' to
# generate a new layout, 'Left/Right' to browse between modes, 'Up/Down'
# to adjust a number of visible cells in the sustained attention traning
# mode or switch sub-modes in the Schulte-Gorbov mode, and 'Esc'
# to exit the program.

import sys, importlib
from random import shuffle
from math import floor
if (importlib.util.find_spec("roman") is None):
    print("The 'roman' module isn't found, install it with pip:")
    print("python -m pip install roman")
    sys.exit(1)
from roman import toRoman
if (importlib.util.find_spec("PyQt5") is None):
    print("The 'PyQt5' module isn't found, install it with pip:")
    print("python -m pip install PyQt5")
    sys.exit(1)
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QFont, QPen, QPalette, QColor
from PyQt5.QtCore import Qt, QRect


INCH2CM_RATIO = 2.54
EDGE_SIZE = 3.06
EDGE_LINE_WIDTH = 3
MAX_CELLS_X = MAX_CELLS_Y = 5
FONT_RATIO = 1/4
DEFAULT_MODE = 0
MASK_SIZE = [1/5, 2/7, 3/8]
BG_COLOR = [255, 248, 236]
GR_COLOR = [180, 16, 16]
ALPHABET = list("абвгдежзиклмнопрстуфхцчшыэюя")


class Schulte(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = DEFAULT_MODE
        self.maskIndex = 0
        self.gorbovIndex = 0
        self.initArrays()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(0, 0, width, height)
        self.showFullScreen()
        self.setWindowTitle('Precise Schulte')
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(*BG_COLOR))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.show()
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.setPen(qp, Qt.black)
        font = QFont()
        font.setFamily("Arial")
        font.setWeight(QFont.Light)
        font.setPixelSize(floor(dpi / INCH2CM_RATIO * EDGE_SIZE * FONT_RATIO))
        qp.setFont(font)
        self.drawSchulteTable(event, qp)
        qp.end()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            app.quit()
        if event.key() == Qt.Key_Space:
            self.initArrays()
            self.update()
        if event.key() == Qt.Key_Left:
            self.mode = self.mode - 1
            if (self.mode < 0): self.mode = 3
            self.initArrays()
            self.update()
        if event.key() == Qt.Key_Right:
            self.mode = self.mode + 1
            if (self.mode > 3): self.mode = 0
            self.initArrays()
            self.update()
        if event.key() == Qt.Key_Up:
            if (self.mode == 1):
                self.maskIndex = self.maskIndex + 1
                if (self.maskIndex >= len(MASK_SIZE)): self.maskIndex = 0
            if (self.mode == 3):
                self.gorbovIndex = self.gorbovIndex + 1
                if (self.gorbovIndex > 2): self.gorbovIndex = 0
            if (0 != self.mode != 2):
                self.initArrays()
                self.update()
        if event.key() == Qt.Key_Down:
            if (self.mode == 1):
                self.maskIndex = self.maskIndex - 1
                if (self.maskIndex < 0): self.maskIndex = len(MASK_SIZE) - 1
            if (self.mode == 3):
                self.gorbovIndex = self.gorbovIndex - 1
                if (self.gorbovIndex < 0): self.gorbovIndex = 2
            if (0 != self.mode != 2):
                self.initArrays()
                self.update()
	
    def drawSchulteTable(self, event, qp):
        if (self.mode == 3 and self.gorbovIndex == 1):
            alphabet1 = ALPHABET[:]
            alphabet2 = ALPHABET[:]
            shuffle(alphabet1)
            shuffle(alphabet2)

        for i in range(cellsX):
            for j in range(cellsY):
                curIndex = cellsX * j + i

                # draw a cell
                if (self.mode == 3 and self.gorbovIndex == 2):
                    self.setPen(qp, Qt.white)
                else:
                    self.setPen(qp, Qt.black)
                qp.drawRect(startX + i * edge, startY + j * edge, edge, edge)

                if (self.mode == 3 and self.gorbovIndex == 2):
                    fillColor = QColor(*self.colors[curIndex])
                else:
                    fillColor = QColor(*BG_COLOR)
                qp.fillRect(startX + i * edge + EDGE_LINE_WIDTH - 1,
                            startY + j * edge + EDGE_LINE_WIDTH - 1,
                            edge - EDGE_LINE_WIDTH, edge - EDGE_LINE_WIDTH,
							fillColor)

                # draw a value
                rect = QRect(startX + i * edge, startY + j * edge, edge, edge)
                if (self.mode == 3 and self.gorbovIndex < 2):
                    self.setPen(qp, QColor(*self.colors[curIndex]))
                elif (self.mode == 3 and self.gorbovIndex == 2):
                    self.setPen(qp, QColor(255, 255, 255))
                else:
                    self.setPen(qp, Qt.black)

                if (self.mode == 3 and self.gorbovIndex == 1):
                    if (curIndex // (len(ALPHABET) - 1) > 0):
                        alphabetPos = curIndex - curIndex // len(ALPHABET) * len(ALPHABET)
                    else:
                        alphabetPos = curIndex
                    if (self.differs[curIndex]):
                        text = f"{self.numbers[curIndex]}-{alphabet1[alphabetPos]}"
                    else:
                        text = f"{self.numbers[curIndex]}-{alphabet1[alphabetPos]}"
                elif (self.mode == 2 and self.differs[curIndex]):
                    text = f"{toRoman(self.numbers[curIndex])}"
                else:
                    text = f"{self.numbers[curIndex]}"

                if (self.mode != 1 or self.mode == 1 and (curIndex + 1) in self.mask):
                    qp.drawText(rect, Qt.AlignCenter, text)
    
    def initArrays(self):
        # generate numbers for a table
        if (self.mode == 2 or self.mode == 3):
            self.numbers = list(range(1, cells + 1))
            for i in range(0, middle):
                self.numbers[i] = i + 1
            for j, i in enumerate(range(middle, cells)):
                self.numbers[i] = j + 1
        else:
            self.numbers = list(range(1, cells + 1))
        
        # generate conditions for cells & shuffle
        if (self.mode == 3):
            self.colors = list([BG_COLOR] * cells)
            for i in range(0, middle):
                self.colors[i] = [0, 0, 0]
            for i in range(middle, cells):
                self.colors[i] = GR_COLOR
            if (self.gorbovIndex == 1):
                self.differs = list([False] * cells)
                for i in range(middle, cells):
                    self.differs[i] = True
                tempArray = list(zip(self.numbers, self.colors, self.differs))
                shuffle(tempArray)
                self.numbers, self.colors, self.differs = zip(*tempArray)
            else:
                tempArray = list(zip(self.numbers, self.colors))
                shuffle(tempArray)
                self.numbers, self.colors = zip(*tempArray)
        elif (self.mode == 2):
            self.differs = list([False] * cells)
            for i in range(middle , cells):
                self.differs[i] = True
            tempArray = list(zip(self.numbers, self.differs))
            shuffle(tempArray)
            self.colors = list([BG_COLOR] * cells)
            self.numbers, self.differs = zip(*tempArray)
        else:
            self.colors = list([BG_COLOR] * cells)
            shuffle(self.numbers)
        if (self.mode == 1):
            self.mask = list(range(1, cells + 1))
            shuffle(self.mask)
            self.mask[:] = self.mask[:(floor(cells * MASK_SIZE[self.maskIndex]))]

    def setPen(self, qp, penColor):
        pen = QPen(penColor, EDGE_LINE_WIDTH, Qt.SolidLine)
        qp.setPen(pen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen() # app.screens()[0]
    app.setOverrideCursor(Qt.BlankCursor)
    # Calculate sizes for a Schulte table
    dpi = screen.physicalDotsPerInch()
    width = screen.size().width()
    height = screen.size().height()
    edge = floor(dpi / INCH2CM_RATIO * EDGE_SIZE)
    cellsX = width // (edge + EDGE_LINE_WIDTH)
    if cellsX > MAX_CELLS_X: cellsX = MAX_CELLS_X
    cellsY = height // (edge + EDGE_LINE_WIDTH)
    if cellsY > MAX_CELLS_Y: cellsY = MAX_CELLS_Y
    if (cellsX < 2 or cellsY < 2):
        print("Not enough cells, should be at least 2x2.")
        sys.exit(1)
    cells = cellsX * cellsY
    middle = cells // 2 if cells // 2 == cells / 2 else cells // 2 + 1
    startX = int((width - (cellsX * EDGE_SIZE / INCH2CM_RATIO * dpi)) // 2)
    startY = int((height - (cellsY * EDGE_SIZE / INCH2CM_RATIO * dpi)) // 2)
    schlt = Schulte()
    sys.exit(app.exec_())
