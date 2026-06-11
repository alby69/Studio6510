class Sprite:
    def __init__(self, width=24, height=21):
        self.width = width
        self.height = height
        self.multicolor = False
        self.data = [0] * (width * height) # 0-3 for colors
        self.colors = [0, 1, 2, 3] # C64 Palette indexes

    def set_pixel(self, x, y, color_index):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.data[y * self.width + x] = color_index

    def get_pixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y * self.width + x]
        return 0

    def to_asm(self):
        # Convert sprite data to KickAss / ACME bytes
        # This is a simplified version
        asm = "; Sprite Data\n"
        for y in range(self.height):
            byte_val = 0
            # Logic to pack bits into bytes based on multicolor/singlecolor
            # ...
        return asm
