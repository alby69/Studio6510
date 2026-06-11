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
