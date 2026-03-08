import json
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QCheckBox, QFrame
)
from PyQt5.QtCore import Qt
import theme


def _make_theme_switch(parent: QWidget):
    try:
        return theme.AnimatedToggleSwitch(parent)
    except Exception:
        fallback = QCheckBox("", parent)
        fallback.setCursor(Qt.PointingHandCursor)
        return fallback


class ManageUsersWindow(QWidget):
    def __init__(self, worker_username, parent_window=None):
        super().__init__()
        self.worker_username = worker_username
        self.parent_window = parent_window
        self.setWindowTitle("Manage Users - Verification")
        self.setMinimumSize(800, 600)
        
        self._init_ui()
        self._load_users()
        
        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())
    
    def _init_ui(self):
        # Header
        title_label = QLabel("User Account Management", self)
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
        
        # Info label
        info_label = QLabel("Pending user verifications:", self)
        
        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Email", "Name", "Age", "Account Number", "Verified", "Action"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Buttons
        back_btn = QPushButton("Back", self)
        back_btn.clicked.connect(self._go_back)
        back_btn.setMinimumHeight(40)
        
        refresh_btn = QPushButton("Refresh", self)
        refresh_btn.setObjectName("primary")
        refresh_btn.clicked.connect(self._load_users)
        refresh_btn.setMinimumHeight(40)
        
        button_row = QHBoxLayout()
        button_row.addWidget(back_btn)
        button_row.addStretch()
        button_row.addWidget(refresh_btn)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 18, 20, 18)
        main_layout.addLayout(header_row)
        main_layout.addWidget(info_label)
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_row)
        
        self.setLayout(main_layout)
    
    def _load_users(self):
        users_file = Path(__file__).parent.parent / "user_app" / "users.json"
        try:
            with users_file.open("r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load users: {e}")
            return
        
        self.table.setRowCount(0)
        
        for email, data in users.items():
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(email))
            self.table.setItem(row, 1, QTableWidgetItem(data.get("name", "N/A")))
            self.table.setItem(row, 2, QTableWidgetItem(str(data.get("age", "N/A"))))
            self.table.setItem(row, 3, QTableWidgetItem(data.get("account_number", "N/A")))
            
            is_verified = data.get("is_verified", False)
            status_item = QTableWidgetItem("Yes" if is_verified else "No")
            self.table.setItem(row, 4, status_item)
            
            # Action button
            if not is_verified:
                verify_btn = QPushButton("Verify")
                verify_btn.setObjectName("primary")
                verify_btn.clicked.connect(lambda checked, e=email: self._verify_user(e))
                self.table.setCellWidget(row, 5, verify_btn)
            else:
                revoke_btn = QPushButton("Revoke")
                revoke_btn.setStyleSheet("background-color: #d32f2f; color: white;")
                revoke_btn.clicked.connect(lambda checked, e=email: self._revoke_verification(e))
                self.table.setCellWidget(row, 5, revoke_btn)
    
    def _verify_user(self, email):
        reply = QMessageBox.question(
            self, "Confirm Verification",
            f"Verify user account: {email}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            users_file = Path(__file__).parent.parent / "user_app" / "users.json"
            try:
                with users_file.open("r", encoding="utf-8") as f:
                    users = json.load(f)
                
                if email in users:
                    users[email]["is_verified"] = True
                    
                    with users_file.open("w", encoding="utf-8") as f:
                        json.dump(users, f, indent=4)
                    
                    QMessageBox.information(self, "Success", f"User {email} verified successfully!")
                    self._load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to verify user: {e}")
    
    def _revoke_verification(self, email):
        reply = QMessageBox.question(
            self, "Confirm Revocation",
            f"Revoke verification for: {email}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            users_file = Path(__file__).parent.parent / "user_app" / "users.json"
            try:
                with users_file.open("r", encoding="utf-8") as f:
                    users = json.load(f)
                
                if email in users:
                    users[email]["is_verified"] = False
                    
                    with users_file.open("w", encoding="utf-8") as f:
                        json.dump(users, f, indent=4)
                    
                    QMessageBox.information(self, "Success", f"Verification revoked for {email}!")
                    self._load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to revoke: {e}")
    
    def _toggle_mode(self, checked):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())
    
    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()
