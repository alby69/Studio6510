from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QBrush, QPen

C64_PALETTE = [
    "#000000", "#FFFFFF", "#880000", "#AAFFEE",
    "#CC44CC", "#00CC55", "#0000AA", "#EEEE77",
    "#DD8855", "#664400", "#FF7777", "#333333",
    "#777777", "#AAFF66", "#0088FF", "#BBBBBB"
]

class PixelEditor(QGraphicsView):
    pixelChanged = Signal(int, int, int)

    def __init__(self, width, height, pixel_size=20):
        super().__init__()
        self.w = width
        self.h = height
        self.pixel_size = pixel_size
        self.current_color_idx = 1 # Palette index

        self.scene = QGraphicsScene(0, 0, self.w * self.pixel_size, self.h * self.pixel_size)
        self.setScene(self.scene)

        self._rects = []
        self._data = [0] * (self.w * self.h)
        self._init_grid()

    def _init_grid(self):
        for y in range(self.h):
            row = []
            for x in range(self.w):
                rect = self.scene.addRect(x * self.pixel_size, y * self.pixel_size,
                                        self.pixel_size, self.pixel_size,
                                        QPen(Qt.lightGray, 0.5))
                rect.setBrush(QBrush(QColor(C64_PALETTE[0])))
                row.append(rect)
            self._rects.append(row)

    def set_pixel_color(self, x, y, color_idx):
        if 0 <= x < self.w and 0 <= y < self.h:
            self._data[y * self.w + x] = color_idx
            self._rects[y][x].setBrush(QBrush(QColor(C64_PALETTE[color_idx])))

    def mousePressEvent(self, event):
        self._handle_mouse(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self._handle_mouse(event)

    def _handle_mouse(self, event):
        pos = self.mapToScene(event.pos())
        x = int(pos.x() // self.pixel_size)
        y = int(pos.y() // self.pixel_size)

        if 0 <= x < self.w and 0 <= y < self.h:
            self.set_pixel_color(x, y, self.current_color_idx)
            self.pixelChanged.emit(x, y, self.current_color_idx)

    def set_data(self, data):
        self._data = list(data)
        for y in range(self.h):
            for x in range(self.w):
                idx = self._data[y * self.w + x]
                self._rects[y][x].setBrush(QBrush(QColor(C64_PALETTE[idx])))

    def get_data(self):
        return self._data
