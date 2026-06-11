from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel
from editors.sprite_editor import SpriteEditor
from models.sprite import Sprite

class SpriteEditorMain(QWidget):
    def __init__(self, sprite_model=None):
        super().__init__()
        if sprite_model is None:
            sprite_model = Sprite()
        self.sprite = sprite_model

        layout = QVBoxLayout(self)

        # Toolbar
        toolbar = QHBoxLayout()

        self.color_sel = QComboBox()
        for i in range(16):
            self.color_sel.addItem(f"Color {i}")
        self.color_sel.currentIndexChanged.connect(self._color_changed)
        toolbar.addWidget(QLabel("Pen:"))
        toolbar.addWidget(self.color_sel)

        self.mc_btn = QPushButton("Multicolor: OFF")
        self.mc_btn.setCheckable(True)
        self.mc_btn.toggled.connect(self._toggle_mc)
        toolbar.addWidget(self.mc_btn)

        export_btn = QPushButton("Export ASM")
        export_btn.clicked.connect(self._export_asm)
        toolbar.addWidget(export_btn)

        layout.addLayout(toolbar)

        # The Editor
        self.pixel_editor = SpriteEditor(self.sprite)
        layout.addWidget(self.pixel_editor)

    def _color_changed(self, index):
        self.pixel_editor.current_color = 1 # Simplified, index should map to sprite colors

    def _toggle_mc(self, checked):
        self.sprite.multicolor = checked
        self.mc_btn.setText(f"Multicolor: {'ON' if checked else 'OFF'}")
        # Update editor view...

    def _export_asm(self):
        print(self.sprite.to_asm())
