from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from editors.map_editor import MapEditor
from models.map import TileMap

class ScreenDesigner(QWidget):
    def __init__(self):
        super().__init__()
        self.map_model = TileMap(40, 25) # Standard C64 screen

        layout = QVBoxLayout(self)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("Brush:"))
        self.brush_sel = QComboBox()
        for i in range(256):
            self.brush_sel.addItem(f"Char {i:02X}")
        toolbar.addWidget(self.brush_sel)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # The Editor
        self.map_editor = MapEditor(self.map_model, char_size=8, zoom=2)
        layout.addWidget(self.map_editor)

        self.setWindowTitle("Screen Designer")
