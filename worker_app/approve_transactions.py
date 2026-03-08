import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QCheckBox
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


class ApproveTransactionsWindow(QWidget):
    def __init__(self, worker_username, parent_window=None):
        super().__init__()
        self.worker_username = worker_username
        self.parent_window = parent_window
        self.setWindowTitle("Transaction Approvals")
        self.setMinimumSize(1000, 600)
        
        self._init_ui()
        self._load_approval_requests()
        
        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())
    
    def _init_ui(self):
        # Header
        title_label = QLabel("Transfer Request Approvals", self)
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
        info_label = QLabel("Pending transfer requests (amounts > 5000):", self)
        
        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Request ID", "From", "To", "Amount", "Date", "Status", "Approve", "Reject"
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        
        # Buttons
        back_btn = QPushButton("Back", self)
        back_btn.clicked.connect(self._go_back)
        back_btn.setMinimumHeight(40)
        
        refresh_btn = QPushButton("Refresh", self)
        refresh_btn.setObjectName("primary")
        refresh_btn.clicked.connect(self._load_approval_requests)
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
    
    def _load_approval_requests(self):
        approval_file = Path(__file__).parent / "approval_requests.json"
        try:
            with approval_file.open("r", encoding="utf-8") as f:
                requests = json.load(f)
        except Exception:
            requests = {}
        
        self.table.setRowCount(0)
        
        for request_id, request_data in requests.items():
            if isinstance(request_data, dict):
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                # Shorten request ID for display
                display_id = request_id.split("_")[-1] if "_" in request_id else request_id
                
                sender = f"{request_data.get('sender_name', 'N/A')} ({request_data.get('sender_account', 'N/A')})"
                recipient = f"{request_data.get('recipient_name', 'N/A')} ({request_data.get('recipient_account', 'N/A')})"
                amount = request_data.get('amount', 0)
                currency = request_data.get('currency', 'EGP')
                date = request_data.get('request_date', 'N/A')
                status = request_data.get('status', 'pending')
                
                self.table.setItem(row, 0, QTableWidgetItem(display_id))
                self.table.setItem(row, 1, QTableWidgetItem(sender))
                self.table.setItem(row, 2, QTableWidgetItem(recipient))
                self.table.setItem(row, 3, QTableWidgetItem(f"{amount:,.2f} {currency}"))
                self.table.setItem(row, 4, QTableWidgetItem(date))
                self.table.setItem(row, 5, QTableWidgetItem(status.capitalize()))
                
                # Action buttons (only for pending requests)
                if status == "pending":
                    approve_btn = QPushButton("Approve")
                    approve_btn.setObjectName("primary")
                    approve_btn.clicked.connect(
                        lambda checked, rid=request_id: self._approve_transfer(rid)
                    )
                    self.table.setCellWidget(row, 6, approve_btn)
                    
                    reject_btn = QPushButton("Reject")
                    reject_btn.setStyleSheet("background-color: #d32f2f; color: white;")
                    reject_btn.clicked.connect(
                        lambda checked, rid=request_id: self._reject_transfer(rid)
                    )
                    self.table.setCellWidget(row, 7, reject_btn)
    
    def _approve_transfer(self, request_id):
        # Load request
        approval_file = Path(__file__).parent / "approval_requests.json"
        try:
            with approval_file.open("r", encoding="utf-8") as f:
                requests = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load requests: {e}")
            return
        
        request_data = requests.get(request_id)
        if not request_data:
            QMessageBox.warning(self, "Error", "Request not found!")
            return
        
        sender_username = request_data.get("sender_username")
        recipient_username = request_data.get("recipient_username")
        amount = request_data.get("amount", 0)
        currency = request_data.get("currency", "EGP")
        
        reply = QMessageBox.question(
            self, "Confirm Approval",
            f"Approve transfer of {amount:,.2f} {currency}?\n\n"
            f"From: {request_data.get('sender_name', 'N/A')} ({request_data.get('sender_account', 'N/A')})\n"
            f"To: {request_data.get('recipient_name', 'N/A')} ({request_data.get('recipient_account', 'N/A')})",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Load users
        users_file = Path(__file__).parent.parent / "user_app" / "users.json"
        try:
            with users_file.open("r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {e}")
            return
        
        # Validate users exist
        if sender_username not in users or recipient_username not in users:
            QMessageBox.critical(self, "Error", "Sender or recipient not found in users database!")
            return
        
        sender_data = users[sender_username]
        recipient_data = users[recipient_username]
        
        # Get balances
        try:
            sender_balance = float(sender_data.get("account_balance", 0))
            recipient_balance = float(recipient_data.get("account_balance", 0))
        except (ValueError, TypeError):
            QMessageBox.critical(self, "Error", "Invalid account balance!")
            return
        
        # Check if sender still has sufficient funds
        if sender_balance < amount:
            QMessageBox.warning(
                self, "Insufficient Funds",
                f"Sender no longer has sufficient funds.\n"
                f"Current balance: {sender_balance:,.2f} {currency}\n"
                f"Required: {amount:,.2f} {currency}"
            )
            return
        
        # Perform transfer
        sender_data["account_balance"] = sender_balance - amount
        recipient_data["account_balance"] = recipient_balance + amount
        
        # Save users
        try:
            with users_file.open("w", encoding="utf-8") as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save users: {e}")
            return
        
        # Update request status
        request_data["status"] = "approved"
        request_data["processed_by"] = self.worker_username
        import datetime
        request_data["processed_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with approval_file.open("w", encoding="utf-8") as f:
                json.dump(requests, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update request status: {e}")
            return
        
        QMessageBox.information(
            self, "Success",
            f"Transfer approved and processed!\n\n"
            f"Amount: {amount:,.2f} {currency}\n"
            f"From: {request_data.get('sender_name', 'N/A')}\n"
            f"To: {request_data.get('recipient_name', 'N/A')}"
        )
        
        self._load_approval_requests()
    
    def _reject_transfer(self, request_id):
        # Load request
        approval_file = Path(__file__).parent / "approval_requests.json"
        try:
            with approval_file.open("r", encoding="utf-8") as f:
                requests = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load requests: {e}")
            return
        
        request_data = requests.get(request_id)
        if not request_data:
            QMessageBox.warning(self, "Error", "Request not found!")
            return
        
        amount = request_data.get("amount", 0)
        currency = request_data.get("currency", "EGP")
        
        reply = QMessageBox.question(
            self, "Confirm Rejection",
            f"Reject transfer request of {amount:,.2f} {currency}?\n\n"
            f"From: {request_data.get('sender_name', 'N/A')}\n"
            f"To: {request_data.get('recipient_name', 'N/A')}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Update request status
        request_data["status"] = "rejected"
        request_data["processed_by"] = self.worker_username
        import datetime
        request_data["processed_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with approval_file.open("w", encoding="utf-8") as f:
                json.dump(requests, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update request status: {e}")
            return
        
        QMessageBox.information(self, "Success", f"Transfer request rejected.")
        self._load_approval_requests()
    
    def _toggle_mode(self, checked):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())
    
    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()
