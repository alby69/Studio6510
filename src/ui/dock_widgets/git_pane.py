from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel
from utils.git_helper import GitHelper

class GitPane(QWidget):
    def __init__(self, repo_path, parent=None):
        super().__init__(parent)
        self.set_repo_path(repo_path)
        self._setup_ui()
        self.refresh()

    def set_repo_path(self, repo_path):
        self.git = GitHelper(repo_path)

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Branch Info
        self.branch_label = QLabel("Branch: unknown")
        layout.addWidget(self.branch_label)

        # Status List
        layout.addWidget(QLabel("Modified Files:"))
        self.status_list = QListWidget()
        layout.addWidget(self.status_list)

        # Commit UI
        self.commit_msg = QLineEdit()
        self.commit_msg.setPlaceholderText("Commit message...")
        layout.addWidget(self.commit_msg)

        btn_layout = QHBoxLayout()
        self.btn_commit = QPushButton("Commit")
        self.btn_commit.clicked.connect(self._on_commit)
        btn_layout.addWidget(self.btn_commit)

        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.clicked.connect(self.refresh)
        btn_layout.addWidget(self.btn_refresh)

        layout.addLayout(btn_layout)

        push_pull_layout = QHBoxLayout()
        self.btn_pull = QPushButton("Pull")
        self.btn_pull.clicked.connect(self._on_pull)
        push_pull_layout.addWidget(self.btn_pull)

        self.btn_push = QPushButton("Push")
        self.btn_push.clicked.connect(self._on_push)
        push_pull_layout.addWidget(self.btn_push)

        layout.addLayout(push_pull_layout)

    def refresh(self):
        self.branch_label.setText(f"Branch: {self.git.branch()}")
        self.status_list.clear()
        stdout, _, success = self.git.status()
        if success:
            for line in stdout.splitlines():
                self.status_list.addItem(line)

    def _on_commit(self):
        msg = self.commit_msg.text()
        if not msg:
            return
        self.git.add(".") # Simplified: add all
        self.git.commit(msg)
        self.commit_msg.clear()
        self.refresh()

    def _on_push(self):
        self.git.push()
        self.refresh()

    def _on_pull(self):
        self.git.pull()
        self.refresh()
