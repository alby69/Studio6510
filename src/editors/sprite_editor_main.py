from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import QTimer, Qt
from editors.sprite_editor import SpriteEditor
from models.sprite import Sprite
from ui.widgets.palette_widget import PaletteWidget

class SpriteEditorMain(QWidget):
    def __init__(self, sprite_model=None):
        super().__init__()
        if sprite_model is None:
            sprite_model = Sprite()
        self.sprite = sprite_model

        layout = QVBoxLayout(self)

        # Toolbar
        toolbar = QHBoxLayout()

        self.palette = PaletteWidget()
        self.palette.colorSelected.connect(self._color_changed)
        toolbar.addWidget(QLabel("Pen:"))
        toolbar.addWidget(self.palette)

        self.mc_btn = QPushButton("Multicolor: OFF")
        self.mc_btn.setCheckable(True)
        self.mc_btn.toggled.connect(self._toggle_mc)
        toolbar.addWidget(self.mc_btn)

        export_btn = QPushButton("Export ASM")
        export_btn.clicked.connect(self._export_asm)
        toolbar.addWidget(export_btn)

        layout.addLayout(toolbar)

        # Main Content (Editor + Preview)
        content_layout = QHBoxLayout()

        # The Editor
        self.pixel_editor = SpriteEditor(self.sprite)
        content_layout.addWidget(self.pixel_editor)

        # Preview Area
        preview_layout = QVBoxLayout()
        self.preview_label = QLabel("Preview")
        preview_layout.addWidget(self.preview_label)

        from PySide6.QtGui import QPixmap, QImage, QPainter
        self.preview_view = QLabel()
        self.preview_view.setFixedSize(24*2, 21*2) # 2x zoom
        self.preview_view.setStyleSheet("background-color: black; border: 1px solid gray;")
        preview_layout.addWidget(self.preview_view)

        self.play_btn = QPushButton("Animate (N/A)")
        self.play_btn.setEnabled(False)
        preview_layout.addWidget(self.play_btn)

        preview_layout.addStretch()
        content_layout.addLayout(preview_layout)

        layout.addLayout(content_layout)

        self.pixel_editor.pixelChanged.connect(self._update_preview)
        self._update_preview()

    def _update_preview(self):
        from PySide6.QtGui import QPixmap, QImage, QColor
        from utils.colors import C64_PALETTE_HEX as C64_PALETTE

        img = QImage(24, 21, QImage.Format_RGB32)
        for y in range(21):
            for x in range(24):
                color_idx = self.sprite.get_pixel(x, y)
                if self.sprite.multicolor:
                    # Basic MC preview logic
                    color_idx = self.sprite.colors[color_idx % 4]
                else:
                    color_idx = self.sprite.colors[color_idx % 2]

                img.setPixelColor(x, y, QColor(C64_PALETTE[color_idx]))

        pixmap = QPixmap.fromImage(img).scaled(48, 42, Qt.KeepAspectRatio)
        self.preview_view.setPixmap(pixmap)

    def _color_changed(self, index):
        self.pixel_editor.current_color = index

    def _toggle_mc(self, checked):
        self.sprite.multicolor = checked
        self.mc_btn.setText(f"Multicolor: {'ON' if checked else 'OFF'}")

    def _toggle_animation(self, checked):
        if checked:
            self.anim_timer.start(100) # 10 FPS
        else:
            self.anim_timer.stop()

    def _export_asm(self):
        print(self.sprite.to_asm())
