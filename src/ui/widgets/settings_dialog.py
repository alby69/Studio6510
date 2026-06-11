from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Settings")
        self.resize(500, 200)

        layout = QVBoxLayout(self)

        # KickAss Path
        ka_layout = QHBoxLayout()
        ka_layout.addWidget(QLabel("KickAssembler JAR:"))
        self.ka_path = QLineEdit(self.settings.get("kickass_jar", ""))
        ka_layout.addWidget(self.ka_path)
        ka_btn = QPushButton("...")
        ka_btn.clicked.connect(self._browse_ka)
        ka_layout.addWidget(ka_btn)
        layout.addLayout(ka_layout)

        # VICE Path
        vice_layout = QHBoxLayout()
        vice_layout.addWidget(QLabel("VICE Executable:"))
        self.vice_path = QLineEdit(self.settings.get("vice_bin", ""))
        vice_layout.addWidget(self.vice_path)
        vice_btn = QPushButton("...")
        vice_btn.clicked.connect(self._browse_vice)
        vice_layout.addWidget(vice_btn)
        layout.addLayout(vice_layout)

        # Buttons
        btns = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._save)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btns.addStretch()
        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)
        layout.addLayout(btns)

    def _browse_ka(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select KickAssembler JAR", "", "JAR Files (*.jar)")
        if path:
            self.ka_path.setText(path)

    def _browse_vice(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select VICE Executable")
        if path:
            self.vice_path.setText(path)

    def _save(self):
        self.settings.set("kickass_jar", self.ka_path.text())
        self.settings.set("vice_bin", self.vice_path.text())
        self.accept()
