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

    def to_bytes(self):
        output = bytearray()
        for y in range(self.height):
            for b in range(3):  # 3 bytes per row
                byte_val = 0
                if self.multicolor:
                    for p in range(4):  # 4 pixels per byte (double width)
                        pixel_x = (b * 4 + p) * 2
                        pixel_val = self.get_pixel(pixel_x, y) & 0x03
                        byte_val |= (pixel_val << (6 - p * 2))
                else:
                    for bit in range(8):
                        pixel_x = b * 8 + bit
                        pixel_val = self.get_pixel(pixel_x, y)
                        if pixel_val > 0:
                            byte_val |= (1 << (7 - bit))
                output.append(byte_val)
        # Pad to 64 bytes if it's a standard C64 sprite
        while len(output) < 64:
            output.append(0)
        return output

    def to_asm(self):
        # Convert sprite data to KickAss bytes
        data = self.to_bytes()
        asm = "; Sprite Data\n"
        for i in range(0, len(data), 8):
            chunk = data[i:i+8]
            bytes_str = ", ".join([f"${b:02x}" for b in chunk])
            asm += f"    .byte {bytes_str}\n"
        return asm
