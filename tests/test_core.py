import unittest
from models.sprite import Sprite
from models.charset import Charset
from core.project import Project
import os
import shutil

class TestC64Models(unittest.TestCase):
    def test_sprite_creation(self):
        sprite = Sprite(24, 21)
        self.assertEqual(sprite.width, 24)
        self.assertEqual(sprite.height, 21)
        sprite.set_pixel(0, 0, 1)
        self.assertEqual(sprite.get_pixel(0, 0), 1)

    def test_charset_creation(self):
        charset = Charset()
        self.assertEqual(len(charset.chars), 256)
        charset.set_pixel(0, 0, 0, 1)
        self.assertEqual(charset.get_pixel(0, 0, 0), 1)

    def test_project_save_load(self):
        test_dir = "test_proj"
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)

        proj = Project("TestProject", test_dir)
        proj.save()

        proj_path = os.path.join(test_dir, "TestProject.c64proj")
        self.assertTrue(os.path.exists(proj_path))

        loaded_proj = Project.load(proj_path)
        self.assertEqual(loaded_proj.name, "TestProject")

        shutil.rmtree(test_dir)

if __name__ == "__main__":
    unittest.main()
