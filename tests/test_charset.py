import unittest
from models.charset import Charset
import os

class TestC64Charset(unittest.TestCase):
    def test_charset_to_from_bytes(self):
        charset = Charset()
        # Set some pixels in char 1
        charset.set_pixel(1, 0, 0, 1)
        charset.set_pixel(1, 7, 7, 1)

        data = charset.to_bytes()
        self.assertEqual(len(data), 2048)

        new_charset = Charset()
        new_charset.from_bytes(data)
        self.assertEqual(new_charset.get_pixel(1, 0, 0), 1)
        self.assertEqual(new_charset.get_pixel(1, 7, 7), 1)
        self.assertEqual(new_charset.get_pixel(1, 1, 1), 0)

if __name__ == "__main__":
    unittest.main()
