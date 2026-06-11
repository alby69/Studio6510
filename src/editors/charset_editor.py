from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QFileDialog
from ui.widgets.pixel_editor import PixelEditor
from models.charset import Charset

class CharsetEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.charset = Charset()
        self.current_char_index = 0

        layout = QHBoxLayout(self)

        # Left: Character List
        list_layout = QVBoxLayout()
        list_layout.addWidget(QLabel("Characters:"))
        self.char_list = QListWidget()
        for i in range(256):
            self.char_list.addItem(f"Char {i:02X}")
        self.char_list.currentRowChanged.connect(self._char_selected)
        list_layout.addWidget(self.char_list)
        layout.addLayout(list_layout, 1)

        # Right: Pixel Editor
        edit_layout = QVBoxLayout()
        self.pixel_editor = PixelEditor(8, 8, pixel_size=30)
        self.pixel_editor.pixelChanged.connect(self._pixel_changed)
        edit_layout.addWidget(self.pixel_editor)

        btns = QHBoxLayout()
        import_btn = QPushButton("Import Binary")
        import_btn.clicked.connect(self._import_bin)
        btns.addWidget(import_btn)

        export_btn = QPushButton("Export Binary")
        export_btn.clicked.connect(self._export_bin)
        btns.addWidget(export_btn)

        export_asm_btn = QPushButton("Export ASM")
        export_asm_btn.clicked.connect(self._export_asm)
        btns.addWidget(export_asm_btn)

        edit_layout.addLayout(btns)

        layout.addLayout(edit_layout, 2)

        self.char_list.setCurrentRow(0)

    def _char_selected(self, index):
        self.current_char_index = index
        self.pixel_editor.set_data(self.charset.chars[index])

    def _pixel_changed(self, x, y, val):
        self.charset.set_pixel(self.current_char_index, x, y, val)

    def _export_bin(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Charset", "", "Binary Files (*.bin *.chr)")
        if path:
            with open(path, 'wb') as f:
                f.write(self.charset.to_bytes())

    def _import_bin(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Charset", "", "Binary Files (*.bin *.chr)")
        if path:
            with open(path, 'rb') as f:
                data = f.read()
                self.charset.from_bytes(data)
            self._char_selected(self.current_char_index)

    def _export_asm(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Charset ASM", "", "Assembly Files (*.asm *.txt)")
        if path:
            with open(path, 'w') as f:
                f.write(self.charset.to_asm())
