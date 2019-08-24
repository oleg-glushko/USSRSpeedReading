# The main idea of this program is to generate tables with the specific
# size of an edge, e.g., 5 cm per cell. You can also change the number
# of cells in rows/columns, a width of the line and size of the font.
# Just modify constants placed in the top of this code.
# 
# You can control this app by keyboard hotkeys: press 'Space' to
# generate another layout or 'Esc' to exit the program.

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QFont, QPen, QPalette, QColor
from PyQt5.QtCore import Qt, QRect
from random import shuffle


INCH2CM_RATIO = 2.54
EDGE_SIZE = 5
EDGE_LINE_WIDTH = 3
MAX_CELLS = 5
FONT_RATIO = 2


class Schulte(QWidget):

    def __init__(self):
        super().__init__()
        self.numbers = list(range(1, cellsX * cellsY + 1))
        shuffle(self.numbers)
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, width, height)
        self.showFullScreen()
        self.setWindowTitle('Precise Schulte')
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor(255,248,236))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.black, EDGE_LINE_WIDTH, Qt.SolidLine)
        qp.setPen(pen)
        font = QFont()
        font.setFamily("Arial")
        font.setWeight(QFont.Light)
        font.setPixelSize(dpi / INCH2CM_RATIO * EDGE_SIZE / FONT_RATIO)
        qp.setFont(font)
        self.drawSchulteTable(event, qp)
        qp.end()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            app.quit()
        if event.key() == Qt.Key_Space:
            self.numbers = list(range(1, cellsX * cellsY + 1))
            shuffle(self.numbers)
            self.update()
    
    def drawSchulteTable(self, event, qp):
        for i in range(cellsX):
            for j in range(cellsY):
                qp.drawRect(startX + i * edge, startY + j * edge, edge, edge)
                rect = QRect(startX + i * edge, startY + j * edge, edge, edge)
                text = f"{self.numbers[i + cellsX * j]}"
                qp.drawText(rect, Qt.AlignCenter, text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen() # app.screens()[0]
    
    # Calculate sizes for a Schulte table
    dpi = screen.physicalDotsPerInch()
    width = screen.size().width()
    height = screen.size().height()
    edge = int(dpi / INCH2CM_RATIO * EDGE_SIZE)
    cellsX = int(width / edge)
    if cellsX > MAX_CELLS: cellsX = MAX_CELLS
    cellsY = int(height / edge)
    if cellsY > MAX_CELLS: cellsY = MAX_CELLS
    startX = (width - (cellsX * EDGE_SIZE / INCH2CM_RATIO * dpi)) / 2
    startY = (height - (cellsY * EDGE_SIZE / INCH2CM_RATIO * dpi)) / 2
    
    schlt = Schulte()
    sys.exit(app.exec_())
