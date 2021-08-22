import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from TerrainMap import *

class WildfireGUI(QWidget):

    TILE_SIZE = 25
    MENU_WIDTH = 100
    PANEL_XPOS = 500
    PANEL_YPOS = 300
    SIM_SPEED = 200
    DEFAULT_MAP = 'test_map.txt'
    IMAGE_PATH = os.getcwd() + '/images/'
    WINDOW_TITLE = 'Wildfire Simulator'
    TERRAIN_TYPES = ['City', 'River', 'Forest', 'Dry Forest', 'Brush',
                    'Dry Brush', 'Grass', 'Dry Grass']

    def __init__(self):
        super().__init__()
        self.map = TerrainMap(self.DEFAULT_MAP)
        self.set_dimensions()
        self.create_menus()
        self.show()
        #sim timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(self.SIM_SPEED)

    def set_dimensions(self):
        self.width = self.TILE_SIZE*len(self.map.grid) + self.MENU_WIDTH
        self.height = self.TILE_SIZE*len(self.map.grid)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setGeometry(self.PANEL_XPOS, self.PANEL_YPOS, self.width, self.height)

    def create_menus(self):
        #layout management
        main_layout = QHBoxLayout()
        spacer_layout = QHBoxLayout()
        spacer_layout.addStretch(1)
        menu_layout = QVBoxLayout()
        click_actions = QButtonGroup(self)
        #default actions
        self.click_action = 'Light Fire'
        self.tile_paint = 'city'
        #create menu items
        menu_layout.addWidget(QLabel('Action on click:'))
        self.create_rb(menu_layout, click_actions, 'Light Fire', True)
        self.create_rb(menu_layout, click_actions, 'Paint Tile', False)
        menu_layout.addWidget(QLabel('Tile to paint:'))
        tile_select = QComboBox()
        tile_select.addItems(self.TERRAIN_TYPES)
        tile_select.currentIndexChanged.connect(self.set_tile_paint)
        menu_layout.addWidget(tile_select)
        menu_layout.addWidget(QLabel('New map size:'))
        size_select = QComboBox()
        size_select.addItems([str(i) for i in range(10, 21)])
        size_select.currentIndexChanged.connect(self.set_empty_map)
        menu_layout.addWidget(size_select)

        #finalize
        main_layout.addLayout(spacer_layout)
        main_layout.addLayout(menu_layout)
        self.setLayout(main_layout)

    def create_rb(self, layout, group, name, is_checked):
        radiobutton = QRadioButton(name)
        radiobutton.name = name
        radiobutton.setChecked(is_checked)
        radiobutton.toggled.connect(self.set_click_action)
        layout.addWidget(radiobutton)
        group.addButton(radiobutton)

    def set_click_action(self):
        self.click_action = self.sender().name

    def set_tile_paint(self, i):
        self.tile_paint = self.TERRAIN_TYPES[i].lower().replace(' ', '_')

    def set_empty_map(self, i):
        self.map = TerrainMap(None, int(10 + i))
        self.set_dimensions()
        self.update()

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
        if (self.map.in_bounds(row, col)):
            if self.click_action == 'Light Fire':
                tile = self.map.grid[row][col]
                if tile.resistance < 100:
                    while not tile.is_burning:
                        tile.light()
            else:
                self.map.grid[row][col] = TerrainTile(self.tile_paint)
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WildfireGUI()
    sys.exit(app.exec_())