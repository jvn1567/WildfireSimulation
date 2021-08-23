import math
import os
from TerrainTile import TerrainTile

class TerrainMap():
    """
    A class containing a square grid of TerrainTile objects, representing
    a larger terrain area.
    """

    MAP_PATH = os.getcwd() + '/maps/'

    def __init__(self, mapfile=None, size=0):
        """
        Constructor for a TerrainTile. Loads data for the type of tile in
        each grid location from the passed in file, or creates an empty
        grid of only grass TerrainTiles if none is provided. The grass tile
        grid will have the number of rows and columns specied by the passed
        in size parameter.

        Args:
            mapfile (string, optional): the filename of the map data to load.
            Defaults to None.
            size (int, optional): the size of the grass-only map to create. 
            Defaults to 0.
        """
        if mapfile != None:
            with open(self.MAP_PATH + mapfile) as mapfile:
                tiles = mapfile.read().split()
            size = int(math.sqrt(len(tiles)))
            self.grid = []
            for i in range(0, size):
                self.grid.append([TerrainTile(tiles[i*size + j]) for j in range(0, size)])
        else:
            self.grid = []
            for i in range(0, size):
                self.grid.append([TerrainTile('grass') for j in range(0, size)])

    def spread_fire(self, row, col):
        """
        Attempts to light the four neighboring tiles if the tile at the passed in
        location is_burning.

        Args:
            row (int): the row of the tile to spread fire from
            col (int): the column of the tile to spread fire from
        """
        if self.grid[row][col].is_burning:
            self.grid[row][col].burn()
            adjacent = [(row-1, col), (row, col+1), (row+1, col), (row, col-1)]
            for r, c in adjacent:
                if self.in_bounds(r, c) and not self.grid[r][c].is_burning:
                    self.grid[r][c].light()


    def in_bounds(self, row, col):
        """
        Returns true if the passed in row and column are within the
        TerrainMap's boundaries.

        Args:
            row (int): the row to check
            col (int): the column to check

        Returns:
            (bool): true if the location passed is in the bounds of the
            TerrainMap
        """
        size = len(self.grid)
        return row < size and col < size and row >= 0 and col >= 0

    def __str__(self):
        """
        Returns a string representing the TerrainMap's tile types, with each
        entry separated by a space and each row separated by a return.

        Returns:
            (string): the TerrainMap grid's tile types
        """
        string = ''
        for row in range(0, len(self.grid)):
            for col in range(0, len(self.grid)):
                string = string + str(self.grid[row][col]) + ' '
            string += '\n'
        return string