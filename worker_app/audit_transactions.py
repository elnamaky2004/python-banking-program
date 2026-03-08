import json
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout,
    QCheckBox, QMessageBox, QLineEdit, QTextEdit,
    QComboBox, QListWidget, QListWidgetItem
)

import theme


def _make_theme_switch(parent: QWidget):
    try:
        return theme.AnimatedToggleSwitch(parent)
    except Exception:
        fallback = QCheckBox("", parent)
        fallback.setCursor(Qt.PointingHandCursor)
        return fallback


class AuditTransactionsWindow(QWidget):
    def __init__(self, worker_username, parent_window=None):
        super().__init__()
        self.worker_username = worker_username
        self.parent_window = parent_window
        self.users = {}

        self.setWindowTitle("Audit Transactions")
        self.setMinimumSize(950, 650)

        self._init_ui()
        self._load_users()

        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

    def _init_ui(self):
        title_label = QLabel("Transaction Audit", self)
        title_label.setStyleSheet("font-size: 18px; font-weight: 700;")

        self.mode_label = QLabel(theme.theme_text(), self)
        self.mode_label.setObjectName("modeLabel")

        self.mode_switch = _make_theme_switch(self)
        self.mode_switch.toggled.connect(self._toggle_mode)

        header_row = QHBoxLayout()
        header_row.addWidget(title_label)
        header_row.addStretch()
        header_row.addWidget(self.mode_label)
        header_row.addWidget(self.mode_switch)

        self.search_type_box = QComboBox(self)
        self.search_type_box.addItems(["Search by Email", "Search by Name"])
        self.search_type_box.currentIndexChanged.connect(self._update_search_placeholder)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("user@example.com")

        search_btn = QPushButton("Search", self)
        search_btn.setObjectName("primary")
        search_btn.clicked.connect(self._search_user)

        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Search Type:", self))
        search_row.addWidget(self.search_type_box)
        search_row.addWidget(self.search_input)
        search_row.addWidget(search_btn)

        self.matches_label = QLabel("Closest Matches:", self)
        self.matches_label.setStyleSheet("font-weight: 600;")
        self.matches_label.hide()

        self.matches_list = QListWidget(self)
        self.matches_list.hide()
        self.matches_list.itemDoubleClicked.connect(self._select_user_from_list)

        self.select_user_btn = QPushButton("Open Selected User", self)
        self.select_user_btn.setObjectName("primary")
        self.select_user_btn.clicked.connect(self._select_user_from_list)
        self.select_user_btn.hide()

        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("Search results will appear here...")

        back_btn = QPushButton("Back", self)
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(self._go_back)

        audit_all_btn = QPushButton("Generate Full Audit Report", self)
        audit_all_btn.setObjectName("primary")
        audit_all_btn.setMinimumHeight(40)
        audit_all_btn.clicked.connect(self._generate_full_audit)

        button_row = QHBoxLayout()
        button_row.addWidget(back_btn)
        button_row.addStretch()
        button_row.addWidget(audit_all_btn)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 18, 20, 18)
        main_layout.addLayout(header_row)
        main_layout.addLayout(search_row)
        main_layout.addWidget(self.matches_label)
        main_layout.addWidget(self.matches_list)
        main_layout.addWidget(self.select_user_btn)
        main_layout.addWidget(self.result_display)
        main_layout.addLayout(button_row)

        self.setLayout(main_layout)

    def _update_search_placeholder(self):
        if self.search_type_box.currentText() == "Search by Email":
            self.search_input.setPlaceholderText("user@example.com")
        else:
            self.search_input.setPlaceholderText("Enter full or partial name")

    def _load_users(self):
        users_file = Path(__file__).parent.parent / "user_app" / "users.json"
        try:
            with users_file.open("r", encoding="utf-8") as f:
                self.users = json.load(f)
        except Exception as e:
            self.users = {}
            QMessageBox.critical(self, "Error", f"Failed to load users: {e}")

    def _search_user(self):
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Missing Input", "Please enter a value to search.")
            return

        if not self.users:
            QMessageBox.warning(self, "No Data", "Users data is not loaded.")
            return

        self.matches_list.clear()
        self.matches_list.hide()
        self.matches_label.hide()
        self.select_user_btn.hide()
        self.result_display.clear()

        search_type = self.search_type_box.currentText()

        if search_type == "Search by Email":
            self._search_by_email(query)
        else:
            self._search_by_name(query)

    def _search_by_email(self, email):
        if email not in self.users:
            self.result_display.setPlainText(f"User not found: {email}")
            return

        self._display_user_report(email, self.users[email])

    def _search_by_name(self, name_query):
        name_query = name_query.lower()

        matches = []
        for email, data in self.users.items():
            user_name = str(data.get("name", "")).strip()
            lowered_name = user_name.lower()

            if name_query in lowered_name:
                score = 0
                if lowered_name == name_query:
                    score = 3
                elif lowered_name.startswith(name_query):
                    score = 2
                else:
                    score = 1

                matches.append((score, user_name, email, data))

        if not matches:
            self.result_display.setPlainText(f"No users found with a name close to: {name_query}")
            return

        matches.sort(key=lambda x: (-x[0], x[1].lower()))

        self.matches_label.show()
        self.matches_list.show()
        self.select_user_btn.show()

        for _, user_name, email, data in matches:
            account_number = data.get("account_number", "N/A")
            item_text = f"{user_name} | {email} | Account: {account_number}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, email)
            self.matches_list.addItem(item)

        self.result_display.setPlainText(
            "Select a user from the closest matches list, then press 'Open Selected User' "
            "or double-click the user."
        )

    def _select_user_from_list(self, item=None):
        if isinstance(item, bool):
            item = None

        if item is None:
            item = self.matches_list.currentItem()

        if item is None:
            QMessageBox.warning(self, "No Selection", "Please select a user first.")
            return

        email = item.data(Qt.UserRole)
        if email not in self.users:
            QMessageBox.warning(self, "User Missing", "Selected user could not be found.")
            return

        self._display_user_report(email, self.users[email])

    def _display_user_report(self, email, user_data):
        balance = self._as_float(user_data.get('account_balance', 0))
        report = f"""
╔════════════════════════════════════════╗
║         USER AUDIT REPORT              ║
╚════════════════════════════════════════╝

Email: {email}
Name: {user_data.get('name', 'N/A')}
Account Number: {user_data.get('account_number', 'N/A')}
Current Balance: {balance:,.2f} EGP
Age: {user_data.get('age', 'N/A')}
Verified: {'Yes' if user_data.get('is_verified', False) else 'No'}
Currency: {user_data.get('currency', 'N/A')}

Audited by: {self.worker_username}
"""
        self.result_display.setPlainText(report)

    def _generate_full_audit(self):
        if not self.users:
            QMessageBox.warning(self, "No Data", "Users data is not loaded.")
            return

        total_balance = sum(
            self._as_float(u.get("account_balance", 0))
            for u in self.users.values()
            if isinstance(u, dict)
        )
        verified_count = sum(
            1
            for u in self.users.values()
            if isinstance(u, dict) and u.get("is_verified", False)
        )

        report = f"""
╔════════════════════════════════════════╗
║         FULL AUDIT REPORT              ║
╚════════════════════════════════════════╝

Total Users: {len(self.users)}
Verified Users: {verified_count}
Unverified Users: {len(self.users) - verified_count}

Total System Balance: {total_balance:,.2f} EGP
Average Balance: {(total_balance / len(self.users)) if self.users else 0:,.2f} EGP

User Details:
"""

        for email, data in self.users.items():
            if not isinstance(data, dict):
                continue

            balance = self._as_float(data.get('account_balance', 0))
            report += f"\n• {email}"
            report += f"\n  Name: {data.get('name', 'N/A')}"
            report += f"\n  Balance: {balance:,.2f} EGP"
            report += f" | Verified: {'Yes' if data.get('is_verified', False) else 'No'}\n"

        report += f"\nAudited by: {self.worker_username}"
        self.result_display.setPlainText(report)

    def _toggle_mode(self, checked):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())

    @staticmethod
    def _as_float(value, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = AuditTransactionsWindow(worker_username="test_worker")
    window.show()
    sys.exit(app.exec_())