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

    def to_bytes(self):
        output = bytearray()
        for y in range(self.height):
            for x in range(self.width):
                output.append(self.data[y][x] & 0xFF)
        return output

    def to_asm(self):
        asm = "; Map Data\n"
        for y in range(self.height):
            asm += "    .byte "
            row_data = self.data[y]
            bytes_str = ", ".join([f"${b:02x}" for b in row_data])
            asm += f"{bytes_str}\n"
        return asm
