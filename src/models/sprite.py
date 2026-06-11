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
        # Convert sprite data to KickAss bytes
        asm = "; Sprite Data\n"
        for y in range(self.height):
            asm += "    .byte "
            bytes_row = []
            for b in range(3): # 3 bytes per row (24 pixels)
                byte_val = 0
                for bit in range(8):
                    pixel_x = b * 8 + bit
                    pixel_val = self.get_pixel(pixel_x, y)
                    if self.multicolor:
                        # In multicolor, 2 bits per pixel
                        # This logic needs refinement but for now:
                        pass
                    else:
                        if pixel_val > 0:
                            byte_val |= (1 << (7 - bit))
                bytes_row.append(f"${byte_val:02x}")
            asm += ", ".join(bytes_row) + "\n"
        return asm
