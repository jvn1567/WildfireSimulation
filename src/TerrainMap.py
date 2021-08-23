import math
import os
from TerrainTile import TerrainTile

class TerrainMap():

    MAP_PATH = os.getcwd() + '/maps/'

    def __init__(self, mapfile=None, size=0):
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
        if self.grid[row][col].is_burning:
            self.grid[row][col].burn()
            adjacent = [(row-1, col), (row, col+1), (row+1, col), (row, col-1)]
            for r, c in adjacent:
                if self.in_bounds(r, c) and not self.grid[r][c].is_burning:
                    self.grid[r][c].light()


    def in_bounds(self, row, col):
        size = len(self.grid)
        return row < size and col < size and row >= 0 and col >= 0

    def __str__(self):
        string = ''
        for row in range(0, len(self.grid)):
            for col in range(0, len(self.grid)):
                string = string + str(self.grid[row][col]) + ' '
            string += '\n'
        return string