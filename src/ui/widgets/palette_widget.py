from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QButtonGroup
from PySide6.QtCore import Signal, QSize

C64_PALETTE = [
    "#000000", "#FFFFFF", "#880000", "#AAFFEE",
    "#CC44CC", "#00CC55", "#0000AA", "#EEEE77",
    "#DD8855", "#664400", "#FF7777", "#333333",
    "#777777", "#AAFF66", "#0088FF", "#BBBBBB"
]

class PaletteWidget(QWidget):
    colorSelected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(2)

        self.button_group = QButtonGroup(self)
        self.buttons = []

        for i in range(16):
            btn = QPushButton()
            btn.setFixedSize(QSize(20, 20))
            btn.setCheckable(True)
            btn.setStyleSheet(f"background-color: {C64_PALETTE[i]}; border: 1px solid #555;")
            btn.setProperty("color_index", i)

            self.layout.addWidget(btn, i // 8, i % 8)
            self.button_group.addButton(btn, i)
            self.buttons.append(btn)

        self.button_group.idClicked.connect(self._color_clicked)
        self.buttons[1].setChecked(True) # Default to white

    def _color_clicked(self, color_idx):
        self.colorSelected.emit(color_idx)

    def set_selected_color(self, color_idx):
        if 0 <= color_idx < 16:
            self.buttons[color_idx].setChecked(True)
