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
        # Hide columns except for Name
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)

        self.layout.addWidget(self.tree)

    def set_project_path(self, path):
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
