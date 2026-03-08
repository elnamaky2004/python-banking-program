import json
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QHBoxLayout,
)

import theme


def _make_theme_switch(parent: QWidget):
    """
    Prefer AnimatedToggleSwitch when available.
    Fall back to a styled QCheckBox if needed.
    """
    try:
        switch = theme.AnimatedToggleSwitch(parent)
        return switch
    except Exception:
        fallback = QCheckBox("", parent)
        fallback.setObjectName("themeSwitch")
        fallback.setCursor(Qt.PointingHandCursor)
        return fallback


class WorkerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Worker")
        self.setGeometry(100, 100, 420, 320)

        self._build_ui()
        self._sync_theme()

    def _build_ui(self):
        self.welcome_label = QLabel("Welcome", self)
        self.welcome_label.setObjectName("welcome")

        self.mode_label = QLabel(theme.theme_text(), self)
        self.mode_label.setObjectName("modeLabel")

        self.mode_switch = _make_theme_switch(self)
        self.mode_switch.toggled.connect(self._toggle_theme)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username (Email)")
        self.username_input.setAlignment(Qt.AlignCenter)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setAlignment(Qt.AlignCenter)

        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setCursor(Qt.PointingHandCursor)
        self.show_password_checkbox.toggled.connect(self._toggle_password_visibility)

        self.sign_in_button = QPushButton("Sign In", self)
        self.sign_in_button.setObjectName("primary")
        self.sign_in_button.clicked.connect(self._sign_in)

        self.error_label = QLabel("", self)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()

        self.username_input.textChanged.connect(self._clear_error)
        self.password_input.textChanged.connect(self._clear_error)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(18, 16, 18, 16)

        top_row = QHBoxLayout()
        top_row.setSpacing(8)
        top_row.addWidget(self.welcome_label)
        top_row.addStretch()
        top_row.addWidget(self.mode_label, 0, Qt.AlignVCenter)
        top_row.addWidget(self.mode_switch, 0, Qt.AlignVCenter)

        main_layout.addLayout(top_row)
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(self.show_password_checkbox)
        main_layout.addWidget(self.sign_in_button)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def _sync_theme(self):
        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

    def _toggle_theme(self, checked: bool):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())

    def _toggle_password_visibility(self, checked: bool):
        self.password_input.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)

    def _clear_error(self):
        self.error_label.hide()
        self.error_label.setText("")
        self.error_label.setStyleSheet("")

    def _load_workers(self) -> dict:
        workers_path = Path(__file__).resolve().with_name("worker.json")
        try:
            with workers_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _sign_in(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self._show_error("Please enter username and password.")
            return

        workers = self._load_workers()
        worker = workers.get(username)

        if not worker or worker.get("password") != password:
            self._show_error("Invalid username or password.")
            return

        if worker.get("status", "active").lower() != "active":
            self._show_error("This account is not active.")
            return

        # Local import avoids circular import issues.
        from worker_signed_in import WorkerSignedIn

        self.signed_in_window = WorkerSignedIn(username)
        self.signed_in_window.show()
        self.close()

    def _show_error(self, message: str):
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setText(message)
        self.error_label.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme.set_global_theme(theme.THEME_IS_DARK)

    window = WorkerApp()
    window.show()
    sys.exit(app.exec_())