from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QFileDialog
from editors.map_editor import MapEditor
from models.map import TileMap
from models.charset import Charset

class ScreenDesigner(QWidget):
    def __init__(self, charset=None):
        super().__init__()
        self.map_model = TileMap(40, 25) # Standard C64 screen
        self.charset = charset or Charset()

        layout = QVBoxLayout(self)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("Brush:"))
        self.brush_sel = QComboBox()
        for i in range(256):
            self.brush_sel.addItem(f"Char {i:02X}")
        self.brush_sel.currentIndexChanged.connect(self._brush_changed)
        toolbar.addWidget(self.brush_sel)

        export_asm_btn = QPushButton("Export ASM")
        export_asm_btn.clicked.connect(self._export_asm)
        toolbar.addWidget(export_asm_btn)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        # The Editor
        self.map_editor = MapEditor(self.map_model, charset_model=self.charset, char_size=8, zoom=2)
        layout.addWidget(self.map_editor)

        self.setWindowTitle("Screen Designer")

    def _brush_changed(self, index):
        self.map_editor.current_char = index

    def _export_asm(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Map ASM", "", "Assembly Files (*.asm *.txt)")
        if path:
            with open(path, 'w') as f:
                f.write(self.map_model.to_asm())
