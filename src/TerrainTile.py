import random

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

class TerrainTile():
    """
    This class represents a terrain tile of a pre-defined type. Terrain
    properties and names are defined in the TERRAIN_TYPES dictionary of
    TerrainTile. Each terrain type has three main parameters assigned
    when initiated:
    1) moisture - acts as a buffer to burning and prevents the tile from
    burning until the parameter reaches 0
    2) material - determines how long the tile will burn for
    3) resistance - the chance of completely ignoring an attempt to light
    the terrain tile.
    Each tile also has two additional parameters, is_burning and is_burnt,
    which indicate the burn state of the tile.
    """

    def __init__(self, type):
        """
        Constructor for a TerrainTile. Accepts a string indicating the
        tile type, defined in the TERRAIN_TYPES dictionary.

        Args:
            type (string): the type of terrain (city, river, forest,
            dry_forest, brush, dry_brush, grass, dry_grass)
        """
        self.type = type
        self.set_params(*TERRAIN_TYPES.get(type))
    
    def set_params(self, moisture, material, resistance):
        """
        Sets burnt and burning default states to False and sets the
        passed in parameters to the TerrainTile's state.

        Args:
            moisture (int): the amount of moisture (burn buffer)
            material (int): the amount of material (burn period)
            resistance (int): the chance of ignoring a fire lighting
            attempt, as a whole number between 0 and 100 inclusive
        """
        self.is_burning = False
        self.is_burnt = False
        self.moisture = moisture
        self.material = material
        self.resistance = resistance

    def burn(self):
        """
        Progesses the burn state if the tile is_burning. Burning
        tiles will lose material until no material remains, then
        become burnt. Burnt tiles have 100% resistance to burning.
        """
        if self.is_burning:
            if self.material >= 100:
                self.material -= 100
            else:
                self.material = 0
                self.is_burning = False
                self.is_burnt = True
                self.resistance = 100

    def light(self):
        """
        Attemps to light the tile on fire if not already burning.
        A random number between 0 and 100 inclusive is generated.
        If this number is larger than the resistance of the tile,
        it lights on fire. If there is still moisture, it will be
        reduced and prevent burning.

        Returns:
            (bool): True if a fire was successfully lit
        """
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
        """
        Returns a string representing the type of terrain the tile
        represents.

        Returns:
            (string): the name of the terrain type
        """
        return self.type