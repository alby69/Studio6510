from PySide6.QtWidgets import QMainWindow, QDockWidget, QTextEdit, QStatusBar, QMenuBar, QFileDialog
from PySide6.QtCore import Qt
from ui.dock_widgets.project_explorer import ProjectExplorer
from core.project import Project
from editors.asm_editor import ASMEditor
from compilers.kick_assembler import KickAssembler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C64 Studio Python")
        self.resize(1200, 800)

        self._setup_ui()

    def _setup_ui(self):
        self.current_project = None
        # Menu Bar
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("&File")
        new_project_action = file_menu.addAction("New Project...")
        open_project_action = file_menu.addAction("Open Project...")
        open_project_action.triggered.connect(self._open_project)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        edit_menu = self.menu_bar.addMenu("&Edit")
        view_menu = self.menu_bar.addMenu("&View")
        tools_menu = self.menu_bar.addMenu("&Tools")
        build_action = tools_menu.addAction("Build")
        build_action.setShortcut("Ctrl+B")
        build_action.triggered.connect(self._build_project)

        help_menu = self.menu_bar.addMenu("&Help")

        # Central Widget (Editors go here)
        self.asm_editor = ASMEditor()
        self.setCentralWidget(self.asm_editor)

        # Dock Widgets
        self._create_docks()

        # Status Bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

    def _create_docks(self):
        # Project Explorer
        self.project_dock = QDockWidget("Project Explorer", self)
        self.project_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.project_explorer = ProjectExplorer(self)
        self.project_dock.setWidget(self.project_explorer)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_dock)

        # Output Window
        self.output_dock = QDockWidget("Output", self)
        self.output_dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.output_window = QTextEdit()
        self.output_window.setReadOnly(True)
        self.output_dock.setWidget(self.output_window)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.output_dock)

    def _build_project(self):
        self.output_window.clear()
        self.output_window.append("Building...")

        # Placeholder for actual build logic
        kickass_path = "KickAss.jar" # Should come from settings
        compiler = KickAssembler(kickass_path)

        # Assume we are editing a file that needs compilation
        self.output_window.append("Executing: java -jar KickAss.jar ...")
        self.output_window.append("Error: KickAss.jar not found (this is expected in the skeleton)")

    def _open_project(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "C64 Project (*.c64proj)")
        if file_path:
            self.current_project = Project.load(file_path)
            self.project_explorer.set_project_path(self.current_project.path)
            self.statusBar().showMessage(f"Project Loaded: {self.current_project.name}")
