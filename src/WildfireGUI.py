import sys
import os
from PyQt5 import QtGui, Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
from TerrainMap import TerrainMap

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

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(200)

        self.show()

    def tick(self):
        for row in range (0, len(self.map.grid)):
            for col in range (0, len(self.map.grid)):
                self.map.spread_fire(row, col)
                self.map.grid[row][col].burn()
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        for row in range (0, len(self.map.grid)):
            for col in range (0, len(self.map.grid)):
                self.point = (self.TILE_SIZE*col, self.TILE_SIZE*row)
                tile = self.map.grid[row][col]
                if tile.is_burning:
                    self.image = self.IMAGE_PATH + str(tile) + 'R.png'
                elif tile.is_burnt and 'dry_' in str(tile):
                    self.image = self.IMAGE_PATH + str(tile)[4:] + 'B.png'
                elif tile.is_burnt:
                    self.image = self.IMAGE_PATH + str(tile) + 'B.png'
                else:
                    self.image = self.IMAGE_PATH + str(tile) + '.png'
                qp.drawImage(*self.point, QImage(self.image))
        qp.end()

    def mousePressEvent(self, QMouseEvent):
        col = int(QMouseEvent.pos().x()/self.TILE_SIZE)
        row = int(QMouseEvent.pos().y()/self.TILE_SIZE)
        tile = self.map.grid[row][col]
        if tile.resistance < 100:
            while not tile.is_burning:
                tile.light()
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WildfireGUI()
    sys.exit(app.exec_())