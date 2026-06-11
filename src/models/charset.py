class Charset:
    def __init__(self):
        self.chars = [] # List of 64-byte lists (8x8)
        for _ in range(256):
            self.chars.append([0] * 64)

    def set_pixel(self, char_index, x, y, value):
        if 0 <= char_index < 256 and 0 <= x < 8 and 0 <= y < 8:
            self.chars[char_index][y * 8 + x] = value

    def get_pixel(self, char_index, x, y):
        if 0 <= char_index < 256 and 0 <= x < 8 and 0 <= y < 8:
            return self.chars[char_index][y * 8 + x]
        return 0

    def to_bytes(self):
        # Convert to 2048 bytes (256 * 8)
        output = bytearray()
        for char in self.chars:
            for row in range(8):
                byte_val = 0
                for col in range(8):
                    if char[row * 8 + col] > 0:
                        byte_val |= (1 << (7 - col))
                output.append(byte_val)
        return output

    def from_bytes(self, data):
        if len(data) < 2048:
            return
        for i in range(256):
            for row in range(8):
                byte_val = data[i * 8 + row]
                for col in range(8):
                    pixel_val = 1 if (byte_val & (1 << (7 - col))) else 0
                    self.chars[i][row * 8 + col] = pixel_val

    def to_asm(self):
        data = self.to_bytes()
        asm = "; Charset Data\n"
        for i in range(0, len(data), 8):
            row_data = data[i:i+8]
            bytes_str = ", ".join([f"${b:02x}" for b in row_data])
            asm += f"    .byte {bytes_str}\n"
        return asm
