class Tile:
    def __init__(self, width=2, height=2):
        self.width = width
        self.height = height
        self.chars = [[0 for _ in range(width)] for _ in range(height)]

class TileMap:
    def __init__(self, width=40, height=25):
        self.width = width
        self.height = height
        self.data = [[0 for _ in range(width)] for _ in range(height)]
