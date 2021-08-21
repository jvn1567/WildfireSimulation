# temporary 
class TerrainMap():

    def __init__(self, size):
        self.grid = [[None for i in range(0,size)] for i in range(0, size)]

    def spread_fire(self, row, col):
        if self.grid[row][col].is_burning():
            self.grid[row][col].burn()
            adjacent = [(row-1, col), (row, col+1), (row+1, col), (row, col-1)]
            for r, c in adjacent:
                if self.in_bounds(r, c) and not self.grid[r][c].is_burning():
                    self.grid[r][c].singe()


    def in_bounds(self, row, col):
        size = len(self.grid)
        return row < size and col < size and row >= 0 and col >= 0

    def __str__(self):
        return str(self.grid)

# debug testing
if __name__ == '__main__':
    test = TerrainMap(10)
    test.grid[5][5] = 55
    print(test.in_bounds(5, 5))