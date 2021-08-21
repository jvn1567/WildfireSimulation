import sys
import os
from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QImage
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
from TerrainMap import TerrainMap

# temp example gui
class WildfireGUI(QWidget):

    TILE_SIZE = 25
    PANEL_WIDTH = 100
    DEFAULT_MAP = 'test_map.txt'
    IMAGE_PATH = os.getcwd() + '/images/'

    def __init__(self):
        super().__init__()
        self.map = TerrainMap(self.DEFAULT_MAP)
        self.title = 'Wildfire Simulator'
        self.left = 500
        self.top = 300
        self.width = self.TILE_SIZE*len(self.map.grid) # + self.PANEL_WIDTH
        self.height = self.TILE_SIZE*len(self.map.grid)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle(self.title)
        #button = QPushButton('PyQt5 button', self)
        #button.setToolTip('This is an example button')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.paintEvent(0)
        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)
        for row in range (0, len(self.map.grid)):
            for col in range (0, len(self.map.grid)):
                #temp
                self.image = self.IMAGE_PATH + str(self.map.grid[row][col]) + '.png'
                self.point = (self.TILE_SIZE*row, self.TILE_SIZE*col)
                qp.drawImage(*self.point, QImage(self.image))

        qp.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WildfireGUI()
    sys.exit(app.exec_())