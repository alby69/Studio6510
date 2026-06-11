from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen

class MapEditor(QGraphicsView):
    def __init__(self, map_model, char_size=8, zoom=2):
        super().__init__()
        self.map_model = map_model
        self.char_size = char_size
        self.zoom = zoom
        self.pixel_size = char_size * zoom

        self.scene = QGraphicsScene(0, 0,
                                   self.map_model.width * self.pixel_size,
                                   self.map_model.height * self.pixel_size)
        self.setScene(self.scene)

        self._rects = []
        self._init_grid()

    def _init_grid(self):
        for y in range(self.map_model.height):
            row = []
            for x in range(self.map_model.width):
                rect = self.scene.addRect(x * self.pixel_size, y * self.pixel_size,
                                        self.pixel_size, self.pixel_size,
                                        QPen(Qt.darkGray, 0.2))
                rect.setBrush(QBrush(QColor("#222222")))
                row.append(rect)
            self._rects.append(row)

    def mousePressEvent(self, event):
        self._handle_mouse(event)

    def _handle_mouse(self, event):
        pos = self.mapToScene(event.pos())
        x = int(pos.x() // self.pixel_size)
        y = int(pos.y() // self.pixel_size)

        if 0 <= x < self.map_model.width and 0 <= y < self.map_model.height:
            # For now, just set a color to show it's working
            self._rects[y][x].setBrush(QBrush(QColor("blue")))
