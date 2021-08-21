import random

class TerrainTile():

    TERRAIN_TYPE = {
        'city': (0, 1000, 35),
        'river': (0, 0, 100),
        'forest': (1000, 2500, 20),
        'dry forest': (200, 2500, 5),
        'brush': (500, 1000, 20),
        'grass': (500, 500, 20),
        'dry grass': (0, 500, 0)
    }

    def __init__(self, type):
        self.set_params(TerrainTile.TERRAIN_TYPE.get(type))
    
    def set_params(self, moisture, material, resistance):
        self.burning = False
        self.moisture = moisture
        self.material = material
        self.resistance = resistance

    def burn(self):
        if self.moisture >= 100:
            self.moisture -= 100
        elif 0 < self.moisture < 100:
            self.moisture = 0
            self.burning = True
        elif self.material >= 100:
            self.material -= 100
        else:
            self.material = 0
            self.burning = False
            self.resistance = 100

    def singe(self):
        if not self.burning:
            roll = random.randint(0, 100)
            if roll > self.resistance:
                self.burning = True

    def isBurning(self):
        return self.burning