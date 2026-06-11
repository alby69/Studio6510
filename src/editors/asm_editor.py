from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from PySide6.QtGui import QFont
from editors.asm_highlighter import ASMHighlighter

class ASMEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.editor = QTextEdit()
        font = QFont("Courier New", 11)
        font.setFixedPitch(True)
        self.editor.setFont(font)
        self.editor.setAcceptRichText(False)

        self.highlighter = ASMHighlighter(self.editor.document())

        self.layout.addWidget(self.editor)

    def set_text(self, text):
        self.editor.setPlainText(text)

    def text(self):
        return self.editor.toPlainText()
