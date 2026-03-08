import json
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox,
    QMessageBox
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


class ViewLogsWindow(QWidget):
    def __init__(self, worker_username, parent_window=None):
        super().__init__()
        self.worker_username = worker_username
        self.parent_window = parent_window
        self.setWindowTitle("System Logs")
        self.setMinimumSize(1000, 600)
        
        self._init_ui()
        self._load_logs()
        
        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())
    
    def _init_ui(self):
        # Header
        title_label = QLabel("System Activity Logs", self)
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
        info_label = QLabel("Recent system activity:", self)
        
        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Timestamp", "User", "Action", "Details", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Buttons
        back_btn = QPushButton("Back", self)
        back_btn.clicked.connect(self._go_back)
        back_btn.setMinimumHeight(40)
        
        refresh_btn = QPushButton("Refresh", self)
        refresh_btn.setObjectName("primary")
        refresh_btn.clicked.connect(self._load_logs)
        refresh_btn.setMinimumHeight(40)
        
        clear_btn = QPushButton("Clear Logs", self)
        clear_btn.setStyleSheet("background-color: #d32f2f; color: white;")
        clear_btn.setMinimumHeight(40)
        clear_btn.clicked.connect(self._clear_logs)
        
        button_row = QHBoxLayout()
        button_row.addWidget(back_btn)
        button_row.addStretch()
        button_row.addWidget(clear_btn)
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
    
    def _load_logs(self):
        logs_file = Path(__file__).parent / "system_logs.json"
        try:
            if logs_file.exists():
                with logs_file.open("r", encoding="utf-8") as f:
                    logs = json.load(f)
            else:
                logs = []
        except Exception:
            logs = []
        
        self.table.setRowCount(0)
        
        # Show most recent first
        for log in reversed(logs[-100:]):  # Last 100 entries
            if isinstance(log, dict):
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                self.table.setItem(row, 0, QTableWidgetItem(log.get("timestamp", "N/A")))
                self.table.setItem(row, 1, QTableWidgetItem(log.get("user", "N/A")))
                self.table.setItem(row, 2, QTableWidgetItem(log.get("action", "N/A")))
                self.table.setItem(row, 3, QTableWidgetItem(log.get("details", "")))
                self.table.setItem(row, 4, QTableWidgetItem(log.get("status", "success")))
    
    def _clear_logs(self):
        reply = QMessageBox.question(
            self, "Confirm Clear",
            "Are you sure you want to clear all logs? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            logs_file = Path(__file__).parent / "system_logs.json"
            try:
                with logs_file.open("w", encoding="utf-8") as f:
                    json.dump([], f)
                
                QMessageBox.information(self, "Success", "All logs cleared!")
                self._load_logs()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to clear logs: {e}")
    
    def _toggle_mode(self, checked):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())
    
    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()


def log_action(user, action, details="", status="success"):
    """Helper function to add entries to the system log."""
    logs_file = Path(__file__).parent / "system_logs.json"
    try:
        if logs_file.exists():
            with logs_file.open("r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
        
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user,
            "action": action,
            "details": details,
            "status": status
        }
        
        logs.append(log_entry)
        
        with logs_file.open("w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4)
    except Exception:
        pass  # Fail silently if logging fails
