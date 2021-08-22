import random

class TerrainTile():

    TERRAIN_TYPES = {
        'city': (0, 5000, 35),
        'river': (0, 0, 100),
        'forest': (1000, 10000, 20),
        'dry_forest': (200, 10000, 5),
        'brush': (500, 2500, 20),
        'dry_brush': (0, 2500, 0),
        'grass': (500, 500, 20),
        'dry_grass': (0, 500, 0)
    }

    def __init__(self, type):
        self.type = type
        self.set_params(*self.TERRAIN_TYPES.get(type))
    
    def set_params(self, moisture, material, resistance):
        self.is_burning = False
        self.is_burnt = False
        self.moisture = moisture
        self.material = material
        self.resistance = resistance

    def burn(self):
        if self.is_burning:
            if self.material >= 100:
                self.material -= 100
            else:
                self.material = 0
                self.is_burning = False
                self.is_burnt = True
                self.resistance = 100

    def light(self):
        if not self.is_burning:
            roll = random.randint(0, 100)
            if roll > self.resistance:
                if self.moisture >= 100:
                    self.moisture -= 100
                else:
                    self.moisture = 0
                    self.is_burning = True
                    return True
        return False

    def __str__(self):
        return self.type