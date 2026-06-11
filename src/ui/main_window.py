from PySide6.QtWidgets import QMainWindow, QDockWidget, QTextEdit, QStatusBar, QMenuBar, QFileDialog
from PySide6.QtCore import Qt
from ui.dock_widgets.project_explorer import ProjectExplorer
from core.project import Project
from core.settings import Settings
from core.plugin_manager import PluginManager
from editors.asm_editor import ASMEditor
from compilers.kick_assembler import KickAssembler
from emulators.vice import Vice
from ui.widgets.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C64 Studio Python")
        self.resize(1200, 800)

        self._setup_ui()

    def _setup_ui(self):
        self.settings = Settings()
        self.plugin_manager = PluginManager()
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

        run_action = tools_menu.addAction("Run")
        run_action.setShortcut("F5")
        run_action.triggered.connect(self._run_project)

        tools_menu.addSeparator()
        settings_action = tools_menu.addAction("Settings...")
        settings_action.triggered.connect(self._open_settings)

        help_menu = self.menu_bar.addMenu("&Help")

        # Central Widget (Editors go here)
        self.asm_editor = ASMEditor()
        self.setCentralWidget(self.asm_editor)

        # Dock Widgets
        self._create_docks()

        # Status Bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

        # Load Plugins
        self.plugin_manager.load_plugins(self)

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

    def _open_settings(self):
        dlg = SettingsDialog(self.settings, self)
        dlg.exec()

    def _run_project(self):
        self.output_window.append("Launching VICE...")
        vice_bin = self.settings.get("vice_bin")
        if not vice_bin:
            self.output_window.append("Error: VICE executable not set. Please check Settings.")
            return

        # Attempt to run a placeholder or the last compiled PRG
        emulator = Vice(vice_bin)
        success, msg = emulator.run("main.prg")
        if success:
            self.output_window.append(f"VICE started: {msg}")
        else:
            self.output_window.append(f"Failed to start VICE: {msg}")

    def _build_project(self):
        self.output_window.clear()
        self.output_window.append("Building...")

        kickass_path = self.settings.get("kickass_jar")
        if not kickass_path or not os.path.exists(kickass_path):
            self.output_window.append("Error: KickAssembler JAR not set or not found. Please check Settings.")
            return

        compiler = KickAssembler(kickass_path)

        # Save current file to a temporary ASM and compile
        # For now we use a hardcoded source name if no project file is selected
        source_file = "main.asm"
        if not os.path.exists(source_file):
            with open(source_file, "w") as f:
                f.write("*=$0801\n.byte $0c,$08,$0a,$00,$9e,$20,$32,$30,$36,$32,$00,$00,$00\n*=$0810\ninc $d020\njmp $0810")

        result = compiler.compile(source_file)
        self.output_window.append(result.get("stdout", ""))
        self.output_window.append(result.get("stderr", ""))
        if result["success"]:
            self.output_window.append("Build Successful.")
        else:
            self.output_window.append("Build Failed.")

    def _open_project(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "C64 Project (*.c64proj)")
        if file_path:
            self.current_project = Project.load(file_path)
            self.project_explorer.set_project_path(self.current_project.path)
            self.statusBar().showMessage(f"Project Loaded: {self.current_project.name}")
