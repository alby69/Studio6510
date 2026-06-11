from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt

class DebuggerWindow(QWidget):
    def __init__(self, debugger, parent=None):
        super().__init__(parent)
        self.debugger = debugger
        self.debugger.registersUpdated.connect(self._update_registers)
        self.debugger.connected.connect(self._on_connected)

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Controls
        controls = QHBoxLayout()
        self.btn_run = QPushButton("Run (G)")
        self.btn_run.clicked.connect(self.debugger.run)
        controls.addWidget(self.btn_run)

        self.btn_step = QPushButton("Step (Z)")
        self.btn_step.clicked.connect(self.debugger.step)
        controls.addWidget(self.btn_step)

        self.btn_break = QPushButton("Break")
        self.btn_break.clicked.connect(self.debugger.break_exec)
        controls.addWidget(self.btn_break)

        self.btn_conn = QPushButton("Connect")
        self.btn_conn.clicked.connect(self._toggle_connect)
        controls.addWidget(self.btn_conn)

        layout.addLayout(controls)

        # Status
        self.status_label = QLabel("Disconnected")
        layout.addWidget(self.status_label)

        # Registers
        self.reg_table = QTableWidget(1, 6)
        self.reg_table.setHorizontalHeaderLabels(["PC", "A", "X", "Y", "SP", "Flags"])
        self.reg_table.verticalHeader().setVisible(False)
        self.reg_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.reg_table)

        layout.addStretch()

    def _on_connected(self, connected):
        if connected:
            self.status_label.setText("Connected to VICE")
            self.btn_conn.setText("Disconnect")
        else:
            self.status_label.setText("Disconnected")
            self.btn_conn.setText("Connect")

    def _toggle_connect(self):
        if self.debugger.running:
            self.debugger.disconnect()
        else:
            self.debugger.connect()

    def _update_registers(self, regs):
        # PC is often ADDR in VICE
        pc = regs.get("ADDR", regs.get("PC", "----"))
        self.reg_table.setItem(0, 0, QTableWidgetItem(pc))
        self.reg_table.setItem(0, 1, QTableWidgetItem(regs.get("A", "--")))
        self.reg_table.setItem(0, 2, QTableWidgetItem(regs.get("X", "--")))
        self.reg_table.setItem(0, 3, QTableWidgetItem(regs.get("Y", "--")))
        self.reg_table.setItem(0, 4, QTableWidgetItem(regs.get("SP", "--")))
        self.reg_table.setItem(0, 5, QTableWidgetItem(regs.get("FLAGS", "--")))
