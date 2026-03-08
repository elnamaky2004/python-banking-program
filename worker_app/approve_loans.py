import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QCheckBox, QTextEdit
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


class ApproveLoansWindow(QWidget):
    def __init__(self, worker_username, parent_window=None):
        super().__init__()
        self.worker_username = worker_username
        self.parent_window = parent_window
        self.setWindowTitle("Loan Approvals")
        self.setMinimumSize(900, 600)
        
        self._init_ui()
        self._load_loan_requests()
        
        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())
    
    def _init_ui(self):
        # Header
        title_label = QLabel("Loan Request Approvals", self)
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
        info_label = QLabel("Pending loan requests:", self)
        
        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Request ID", "User", "Amount", "Purpose", "Status", "Approve", "Reject"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Buttons
        back_btn = QPushButton("Back", self)
        back_btn.clicked.connect(self._go_back)
        back_btn.setMinimumHeight(40)
        
        refresh_btn = QPushButton("Refresh", self)
        refresh_btn.setObjectName("primary")
        refresh_btn.clicked.connect(self._load_loan_requests)
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
    
    def _load_loan_requests(self):
        loans_file = Path(__file__).parent / "loan_requests.json"
        try:
            with loans_file.open("r", encoding="utf-8") as f:
                loans = json.load(f)
        except Exception:
            loans = []
        
        self.table.setRowCount(0)
        
        for loan in loans:
            if isinstance(loan, dict):
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                self.table.setItem(row, 0, QTableWidgetItem(loan.get("id", "N/A")))
                self.table.setItem(row, 1, QTableWidgetItem(loan.get("user", "N/A")))
                self.table.setItem(row, 2, QTableWidgetItem(f"{loan.get('amount', 0):,.2f} EGP"))
                self.table.setItem(row, 3, QTableWidgetItem(loan.get("purpose", "N/A")))
                self.table.setItem(row, 4, QTableWidgetItem(loan.get("status", "pending")))
                
                # Action buttons
                if loan.get("status") == "pending":
                    approve_btn = QPushButton("Approve")
                    approve_btn.setObjectName("primary")
                    approve_btn.clicked.connect(lambda checked, lid=loan.get("id"): self._approve_loan(lid))
                    self.table.setCellWidget(row, 5, approve_btn)
                    
                    reject_btn = QPushButton("Reject")
                    reject_btn.setStyleSheet("background-color: #d32f2f; color: white;")
                    reject_btn.clicked.connect(lambda checked, lid=loan.get("id"): self._reject_loan(lid))
                    self.table.setCellWidget(row, 6, reject_btn)
    
    def _approve_loan(self, loan_id):
        reply = QMessageBox.question(
            self, "Confirm Approval",
            f"Approve loan request {loan_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self._update_loan_status(loan_id, "approved")
    
    def _reject_loan(self, loan_id):
        reply = QMessageBox.question(
            self, "Confirm Rejection",
            f"Reject loan request {loan_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self._update_loan_status(loan_id, "rejected")
    
    def _update_loan_status(self, loan_id, new_status):
        loans_file = Path(__file__).parent / "loan_requests.json"
        try:
            with loans_file.open("r", encoding="utf-8") as f:
                loans = json.load(f)
            
            for loan in loans:
                if isinstance(loan, dict) and loan.get("id") == loan_id:
                    loan["status"] = new_status
                    loan["processed_by"] = self.worker_username
                    break
            
            with loans_file.open("w", encoding="utf-8") as f:
                json.dump(loans, f, indent=4)
            
            QMessageBox.information(self, "Success", f"Loan {loan_id} {new_status}!")
            self._load_loan_requests()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update loan: {e}")
    
    def _toggle_mode(self, checked):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())
    
    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()
