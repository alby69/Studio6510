from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen

class MapEditor(QGraphicsView):
    def __init__(self, map_model, charset_model=None, char_size=8, zoom=2):
        super().__init__()
        self.map_model = map_model
        self.charset = charset_model
        self.char_size = char_size
        self.zoom = zoom
        self.pixel_size = char_size * zoom
        self.current_char = 0

        self.scene = QGraphicsScene(0, 0,
                                   self.map_model.width * self.pixel_size,
                                   self.map_model.height * self.pixel_size)
        self.setScene(self.scene)

        self._items = []
        self._init_grid()

    def _init_grid(self):
        from PySide6.QtWidgets import QGraphicsPixmapItem

        for y in range(self.map_model.height):
            row = []
            for x in range(self.map_model.width):
                item = QGraphicsPixmapItem()
                item.setPos(x * self.pixel_size, y * self.pixel_size)
                self.scene.addItem(item)
                row.append(item)
            self._items.append(row)

        for y in range(self.map_model.height):
            for x in range(self.map_model.width):
                self._update_cell(x, y)

    def _update_cell(self, x, y):
        from PySide6.QtGui import QPixmap, QImage, QColor
        from utils.colors import C64_PALETTE_HEX as C64_PALETTE

        char_idx = self.map_model.data[y][x]

        img = QImage(8, 8, QImage.Format_RGB32)
        if self.charset:
            char_data = self.charset.chars[char_idx]
            for cy in range(8):
                for cx in range(8):
                    pixel_val = char_data[cy * 8 + cx]
                    color = QColor(C64_PALETTE[1 if pixel_val else 0])
                    img.setPixelColor(cx, cy, color)
        else:
            img.fill(QColor("#222222"))

        pixmap = QPixmap.fromImage(img).scaled(self.pixel_size, self.pixel_size)
        self._items[y][x].setPixmap(pixmap)

    def mousePressEvent(self, event):
        self._handle_mouse(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self._handle_mouse(event)

    def _handle_mouse(self, event):
        pos = self.mapToScene(event.pos())
        x = int(pos.x() // self.pixel_size)
        y = int(pos.y() // self.pixel_size)

        if 0 <= x < self.map_model.width and 0 <= y < self.map_model.height:
            self.map_model.data[y][x] = self.current_char
            self._update_cell(x, y)
