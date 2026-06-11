from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QBrush, QPen

C64_PALETTE = [
    "#000000", "#FFFFFF", "#880000", "#AAFFEE",
    "#CC44CC", "#00CC55", "#0000AA", "#EEEE77",
    "#DD8855", "#664400", "#FF7777", "#333333",
    "#777777", "#AAFF66", "#0088FF", "#BBBBBB"
]

class SpriteEditor(QGraphicsView):
    pixelChanged = Signal(int, int, int)

    def __init__(self, sprite_model):
        super().__init__()
        self.sprite = sprite_model
        self.scene = QGraphicsScene(0, 0, self.sprite.width * 20, self.sprite.height * 20)
        self.setScene(self.scene)
        self.setRenderHint(Qt.TransformationMode.FastTransformation)

        self.pixel_size = 20
        self.current_color = 1

        self._rects = []
        self._init_grid()

    def _init_grid(self):
        for y in range(self.sprite.height):
            row = []
            for x in range(self.sprite.width):
                rect = self.scene.addRect(x * self.pixel_size, y * self.pixel_size,
                                        self.pixel_size, self.pixel_size,
                                        QPen(Qt.lightGray, 0.5))
                color = QColor(C64_PALETTE[self.sprite.colors[self.sprite.get_pixel(x, y)]])
                rect.setBrush(QBrush(color))
                row.append(rect)
            self._rects.append(row)

    def mousePressEvent(self, event):
        self._handle_mouse(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self._handle_mouse(event)

    def _handle_mouse(self, event):
        pos = self.mapToScene(event.pos())
        x = int(pos.x() // self.pixel_size)
        y = int(pos.y() // self.pixel_size)

        if 0 <= x < self.sprite.width and 0 <= y < self.sprite.height:
            self.sprite.set_pixel(x, y, self.current_color)
            color = QColor(C64_PALETTE[self.sprite.colors[self.current_color]])
            self._rects[y][x].setBrush(QBrush(color))
            self.pixelChanged.emit(x, y, self.current_color)
