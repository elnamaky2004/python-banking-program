import json
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFrame,
    QGridLayout,
)

import theme
from manage_users import ManageUsersWindow
from approve_loans import ApproveLoansWindow
from approve_transactions import ApproveTransactionsWindow
from view_reports import ViewReportsWindow
from manage_transactions import ManageTransactionsWindow
from audit_transactions import AuditTransactionsWindow
from view_logs import ViewLogsWindow


def _make_theme_switch(parent: QWidget):
    try:
        return theme.AnimatedToggleSwitch(parent)
    except Exception:
        fallback = QCheckBox("", parent)
        fallback.setObjectName("themeSwitch")
        fallback.setCursor(Qt.PointingHandCursor)
        return fallback


class WorkerSignedIn(QWidget):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.worker_data = self._load_worker_data()

        full_name = self.worker_data.get("full_name", self.username)
        self.setWindowTitle(full_name)
        self.setMinimumSize(520, 360)

        self._build_ui()

        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

    def _load_worker_data(self) -> dict:
        workers_path = Path(__file__).resolve().with_name("worker.json")
        try:
            with workers_path.open("r", encoding="utf-8") as f:
                workers = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            workers = {}

        return workers.get(self.username, {})

    def _build_ui(self):
        full_name = self.worker_data.get("full_name", self.username)
        role = self.worker_data.get("role", "Worker")
        employee_id = self.worker_data.get("employee_id", "-")
        department = self.worker_data.get("department", "N/A")
        permissions = self.worker_data.get("permissions", [])

        # ---------- Header (Title + Theme) ----------
        title_label = QLabel("Worker Dashboard", self)
        title_label.setStyleSheet("font-size: 18px; font-weight: 700;")

        self.mode_label = QLabel(theme.theme_text(), self)
        self.mode_label.setObjectName("modeLabel")

        self.mode_switch = _make_theme_switch(self)
        self.mode_switch.toggled.connect(self._toggle_mode)

        header_row = QHBoxLayout()
        header_row.setSpacing(10)
        header_row.addWidget(title_label)
        header_row.addStretch()
        header_row.addWidget(self.mode_label, 0, Qt.AlignVCenter)
        header_row.addWidget(self.mode_switch, 0, Qt.AlignVCenter)

        # ---------- Welcome ----------
        welcome_label = QLabel(f"Welcome {full_name}", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setObjectName("welcome")

        # ---------- Info Card ----------
        card = QFrame(self)
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(
            """
            QFrame {
                border-radius: 12px;
                padding: 12px;
            }
            """
        )

        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        info_layout.setContentsMargins(12, 10, 12, 10)

        role_label = QLabel(f"Role: {role}", self)
        employee_label = QLabel(f"Employee ID: {employee_id}", self)
        dept_label = QLabel(f"Department: {department}", self)

        role_label.setAlignment(Qt.AlignLeft)
        employee_label.setAlignment(Qt.AlignLeft)
        dept_label.setAlignment(Qt.AlignLeft)

        info_layout.addWidget(role_label)
        info_layout.addWidget(employee_label)
        info_layout.addWidget(dept_label)

        card.setLayout(info_layout)

        # ---------- Permission-Based Action Buttons ----------
        # Check if user is manager (has full_access permission)
        is_manager = "full_access" in permissions
        
        # Define all possible buttons with their required permissions
        button_configs = [
            ("Manage Users", "manage_users", self._manage_users),
            ("Verify Accounts", "manage_users", self._manage_users),
            ("Approve Loans", "approve_loans", self._approve_loans),
            ("Approve Transactions", "approve_transactions", self._approve_transactions),
            ("View Reports", "view_reports", self._view_reports),
            ("Transaction Mgmt", "deposit", self._manage_transactions),  # deposit, withdraw, transfer
            ("Audit Transactions", "audit_transactions", self._audit_transactions),
            ("View System Logs", "view_logs", self._view_logs),
            ("Staff Management", "manage_staff", self._manage_staff),
        ]
        
        # Create grid layout for buttons
        actions_grid = QGridLayout()
        actions_grid.setSpacing(10)
        
        row, col = 0, 0
        max_cols = 2
        
        for button_text, required_permission, callback in button_configs:
            # Show button if manager OR has specific permission
            if is_manager or required_permission in permissions:
                btn = QPushButton(button_text, self)
                btn.setMinimumHeight(45)
                if button_text in ["Manage Users", "Approve Loans", "Approve Transactions"]:
                    btn.setObjectName("primary")
                btn.clicked.connect(callback)
                
                actions_grid.addWidget(btn, row, col)
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

        # ---------- Sign out ----------
        self.sign_out_button = QPushButton("Sign Out", self)
        self.sign_out_button.setMinimumHeight(42)
        self.sign_out_button.clicked.connect(self._sign_out)

        # ---------- Main Layout ----------
        main_layout = QVBoxLayout()
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(20, 18, 20, 18)

        main_layout.addLayout(header_row)
        main_layout.addWidget(welcome_label)
        main_layout.addWidget(card)
        main_layout.addSpacing(10)
        main_layout.addLayout(actions_grid)
        main_layout.addStretch()
        main_layout.addWidget(self.sign_out_button)

        self.setLayout(main_layout)

    def _toggle_mode(self, checked: bool):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())

    def _manage_users(self):
        self.manage_users_window = ManageUsersWindow(self.username, self)
        self.manage_users_window.show()
        self.hide()
    
    def _approve_loans(self):
        self.approve_loans_window = ApproveLoansWindow(self.username, self)
        self.approve_loans_window.show()
        self.hide()
    
    def _approve_transactions(self):
        self.approve_transactions_window = ApproveTransactionsWindow(self.username, self)
        self.approve_transactions_window.show()
        self.hide()
    
    def _view_reports(self):
        self.view_reports_window = ViewReportsWindow(self.username, self)
        self.view_reports_window.show()
        self.hide()
    
    def _manage_transactions(self):
        self.manage_transactions_window = ManageTransactionsWindow(self.username, self)
        self.manage_transactions_window.show()
        self.hide()
    
    def _audit_transactions(self):
        self.audit_transactions_window = AuditTransactionsWindow(self.username, self)
        self.audit_transactions_window.show()
        self.hide()

    def _view_logs(self):
        self.view_logs_window = ViewLogsWindow(self.username, self)
        self.view_logs_window.show()
        self.hide()
    
    def _manage_staff(self):
        # Placeholder for staff management
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Staff Management", 
                              "Staff management module coming soon!")

    def _sign_out(self):
        from app import WorkerApp
        self._login_window = WorkerApp()
        self._login_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme.set_global_theme(theme.THEME_IS_DARK)

    window = WorkerSignedIn("osama.elnamki@bank.com")
    window.show()
    sys.exit(app.exec_())