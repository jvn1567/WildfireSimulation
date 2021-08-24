import sys
import os
from TerrainTile import TerrainTile
from TerrainMap import TerrainMap
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QRadioButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QApplication

TERRAIN_TYPES = ['City', 'River', 'Forest', 'Dry Forest', 'Brush',
                 'Dry Brush', 'Grass', 'Dry Grass']
TILE_SIZE = 25
MENU_WIDTH = 100
PANEL_XPOS = 500
PANEL_YPOS = 300
MIN_GRID = 10
MAX_GRID = 20
SIM_SPEED = 200
DEFAULT_MAP = 'test_map.txt'
USER_FILE = 'user_custom.txt'
IMAGE_PATH = os.getcwd() + '/images/'
WINDOW_TITLE = 'Wildfire Simulator'

class WildfireGUI(QWidget):
    """
    This class creates a GUI where the user can simulate a wildfire
    spreading through a location with varying terrain types and also
    edit the terrain.
    """

    def __init__(self):
        """
        Constructor for the GUI. Sets up the window and events.
        """
        super().__init__()
        self.map = TerrainMap(DEFAULT_MAP)
        self.set_dimensions()
        self.create_menu()
        self.show()
        #sim timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(SIM_SPEED)

    def set_dimensions(self):
        """
        Sets the dimensions of the GUI window according to size of the
        simulated TerrainMap and predefined parameters.
        """
        self.width = TILE_SIZE*len(self.map.grid) + MENU_WIDTH
        self.height = TILE_SIZE*len(self.map.grid)
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(PANEL_XPOS, PANEL_YPOS, self.width, self.height)

    def create_menu(self):
        """
        Creates the user menu on the right of the GUI window.
        """
        #layout management
        main_layout = QHBoxLayout()
        spacer_layout = QHBoxLayout()
        spacer_layout.addStretch(1)
        menu_layout = QVBoxLayout()
        #default actions
        self.click_action = 'Light Fire'
        self.tile_paint = 'city'
        #click action select
        menu_layout.addWidget(QLabel('Action on click:'))
        self.create_rb(menu_layout, 'Light Fire', True)
        self.create_rb(menu_layout, 'Paint Tile', False)
        #tile paint select
        menu_layout.addWidget(QLabel('Tile to paint:'))
        tile_select = QComboBox()
        tile_select.addItems(TERRAIN_TYPES)
        tile_select.currentIndexChanged.connect(self.set_tile_paint)
        menu_layout.addWidget(tile_select)
        #new map size select
        menu_layout.addWidget(QLabel('New map size:'))
        size_select = QComboBox()
        size_select.addItems([str(i) for i in range(MIN_GRID, MAX_GRID+1)])
        size_select.currentIndexChanged.connect(self.set_empty_map)
        menu_layout.addWidget(size_select)
        #save and load
        btn_save = QPushButton('Save', self)
        btn_save.clicked.connect(self.save)
        menu_layout.addWidget(btn_save)
        btn_load = QPushButton('Load', self)
        btn_load.clicked.connect(self.load)
        menu_layout.addWidget(btn_load)
        #finalize
        main_layout.addLayout(spacer_layout)
        main_layout.addLayout(menu_layout)
        self.setLayout(main_layout)

    def create_rb(self, layout, name, is_checked):
        """
        Creates a single radiobutton with the passed-in name and adds
        it to the passed-in layout. The radio button will be checked
        by default if is_checked is passed as true.

        Args:
            layout (QHBoxLayout): the layout to add the radiobutton to
            name (string): the radiobutton's option text
            is_checked (bool): true if the radiobutton is checked by default
        """
        radiobutton = QRadioButton(name)
        radiobutton.name = name
        radiobutton.setChecked(is_checked)
        radiobutton.toggled.connect(self.set_click_action)
        layout.addWidget(radiobutton)

    def set_click_action(self):
        """
        Sets a string tag deteriming whether user clicks will light fires
        or paint tiles when radiobutton options are changed.
        """
        self.click_action = self.sender().name

    def set_tile_paint(self, i):
        """
        Sets the TerrainTile type placed when painting tiles to the type
        selected in the QComboBox dropdown.

        Args:
            i (int): index of the dropdown menu item selected
        """
        self.tile_paint = TERRAIN_TYPES[i].lower().replace(' ', '_')

    def set_empty_map(self, i):
        """
        Replaces the current TerrainMap with a new TerrainMap of only grass
        with the chosen size parameter from the QComboBox.

        Args:
            i (int): index of the dropdown menu item selected
        """
        self.map = TerrainMap(None, int(10 + i))
        self.set_dimensions()
        self.update()

    def save(self):
        """
        Saves the TerrainMap's tile types to a file.
        """
        with open(self.map.MAP_PATH + USER_FILE, 'w') as f:
            f.write(str(self.map))

    def load(self):
        """
        Loads the last saved TerrainMap from a file.
        """
        self.map = TerrainMap(USER_FILE)
        self.set_dimensions()
        self.update()

    def tick(self):
        """
        Progress the animation. Each burning tile will have its burn
        state progressed and attempt to light a fire on the neighboring
        four tiles.
        """
        for row in range (0, len(self.map.grid)):
            for col in range (0, len(self.map.grid)):
                self.map.spread_fire(row, col)
                self.map.grid[row][col].burn()
        self.update()

    def paintEvent(self, event):
        """
        Redraws the simulation on the window.

        Args:
            event (event): default positional argument sent by PyQt5, unused
        """
        qp = QPainter(self)
        for row in range (0, len(self.map.grid)):
            for col in range (0, len(self.map.grid)):
                self.point = (TILE_SIZE*col, TILE_SIZE*row)
                tile = self.map.grid[row][col]
                if tile.is_burning:
                    self.image = IMAGE_PATH + str(tile) + 'R.png'
                elif tile.is_burnt and 'dry_' in str(tile):
                    self.image = IMAGE_PATH + str(tile)[4:] + 'B.png'
                elif tile.is_burnt:
                    self.image = IMAGE_PATH + str(tile) + 'B.png'
                else:
                    self.image = IMAGE_PATH + str(tile) + '.png'
                qp.drawImage(*self.point, QImage(self.image))
        qp.end()

    def mousePressEvent(self, QMouseEvent):
        """
        Attempts to light the tile on fire, or paint a new tile type,
        depending on the radiobutton option selected.

        Args:
            QMouseEvent (QMouseEvent): a mouse click event
        """
        col = int(QMouseEvent.pos().x()/TILE_SIZE)
        row = int(QMouseEvent.pos().y()/TILE_SIZE)
        if (self.map.in_bounds(row, col)):
            if self.click_action == 'Light Fire':
                tile = self.map.grid[row][col]
                if tile.resistance < 100:
                    self.map.grid[row][col].is_burning = True
            else:
                self.map.grid[row][col] = TerrainTile(self.tile_paint)
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WildfireGUI()
    sys.exit(app.exec_())