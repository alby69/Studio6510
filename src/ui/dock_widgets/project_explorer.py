from PySide6.QtWidgets import QTreeView, QVBoxLayout, QWidget
from PySide6.QtGui import QFileSystemModel
from PySide6.QtCore import QDir

class ProjectExplorer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        self.tree.doubleClicked.connect(self._on_double_click)
        # Hide columns except for Name
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)

        self.layout.addWidget(self.tree)

    def _on_double_click(self, index):
        file_path = self.model.filePath(index)
        if QDir(file_path).exists():
            return # It's a directory

        # Call main window to open file
        # In a real app we'd use a better way to find the main window
        if hasattr(self.parent(), "open_file"):
            self.parent().open_file(file_path)
        elif hasattr(self.window(), "open_file"):
            self.window().open_file(file_path)

    def set_project_path(self, path):
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
