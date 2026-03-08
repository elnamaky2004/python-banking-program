import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout,
    QLineEdit, QComboBox, QMessageBox, QCheckBox, QFrame
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


class ManageTransactionsWindow(QWidget):
    def __init__(self, worker_username, parent_window=None):
        super().__init__()
        self.worker_username = worker_username
        self.parent_window = parent_window
        self.setWindowTitle("Manage Transactions")
        self.setMinimumSize(600, 500)
        
        self._init_ui()
        
        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())
    
    def _init_ui(self):
        # Header
        title_label = QLabel("Transaction Management", self)
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
        
        # Transaction type selector
        type_label = QLabel("Transaction Type:", self)
        self.transaction_type = QComboBox(self)
        self.transaction_type.addItems(["Deposit", "Withdraw", "Transfer"])
        self.transaction_type.setMinimumHeight(35)
        
        # User email input
        email_label = QLabel("User Email:", self)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("user@example.com")
        
        # Amount input
        amount_label = QLabel("Amount (EGP):", self)
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("0.00")
        
        # Recipient (for transfers)
        recipient_label = QLabel("Recipient Account:", self)
        self.recipient_input = QLineEdit(self)
        self.recipient_input.setPlaceholderText("Account number (for transfers)")
        
        # Process button
        process_btn = QPushButton("Process Transaction", self)
        process_btn.setObjectName("primary")
        process_btn.setMinimumHeight(45)
        process_btn.clicked.connect(self._process_transaction)
        
        # Back button
        back_btn = QPushButton("Back", self)
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(self._go_back)
        
        # Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 18, 20, 18)
        
        main_layout.addLayout(header_row)
        main_layout.addSpacing(10)
        main_layout.addWidget(type_label)
        main_layout.addWidget(self.transaction_type)
        main_layout.addWidget(email_label)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(amount_label)
        main_layout.addWidget(self.amount_input)
        main_layout.addWidget(recipient_label)
        main_layout.addWidget(self.recipient_input)
        main_layout.addStretch()
        main_layout.addWidget(process_btn)
        main_layout.addWidget(back_btn)
        
        self.setLayout(main_layout)
    
    def _process_transaction(self):
        trans_type = self.transaction_type.currentText()
        email = self.email_input.text().strip()
        amount_text = self.amount_input.text().strip()
        recipient = self.recipient_input.text().strip()
        
        if not email or not amount_text:
            QMessageBox.warning(self, "Missing Data", "Please fill in all required fields.")
            return
        
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            QMessageBox.warning(self, "Invalid Amount", "Please enter a valid positive number.")
            return
        
        users_file = Path(__file__).parent.parent / "user_app" / "users.json"
        try:
            with users_file.open("r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {e}")
            return
        
        if email not in users:
            QMessageBox.warning(self, "User Not Found", f"No user with email: {email}")
            return
        
        current_balance = users[email].get("account_balance", 0)
        
        if trans_type == "Deposit":
            users[email]["account_balance"] = current_balance + amount
            msg = f"Deposited {amount:.2f} EGP to {email}"
        
        elif trans_type == "Withdraw":
            if current_balance < amount:
                QMessageBox.warning(self, "Insufficient Funds", 
                                  f"User balance ({current_balance:.2f}) is less than withdrawal amount.")
                return
            users[email]["account_balance"] = current_balance - amount
            msg = f"Withdrew {amount:.2f} EGP from {email}"
        
        elif trans_type == "Transfer":
            if not recipient:
                QMessageBox.warning(self, "Missing Recipient", "Please enter recipient account number.")
                return
            
            # Find recipient by account number
            recipient_email = None
            for e, data in users.items():
                if data.get("account_number") == recipient:
                    recipient_email = e
                    break
            
            if not recipient_email:
                QMessageBox.warning(self, "Recipient Not Found", f"No account with number: {recipient}")
                return
            
            if current_balance < amount:
                QMessageBox.warning(self, "Insufficient Funds",
                                  f"User balance ({current_balance:.2f}) is less than transfer amount.")
                return
            
            users[email]["account_balance"] = current_balance - amount
            recipient_balance = users[recipient_email].get("account_balance", 0)
            users[recipient_email]["account_balance"] = recipient_balance + amount
            msg = f"Transferred {amount:.2f} EGP from {email} to {recipient_email}"
        
        # Save changes
        try:
            with users_file.open("w", encoding="utf-8") as f:
                json.dump(users, f, indent=4)
            
            QMessageBox.information(self, "Success", msg)
            self._clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save transaction: {e}")
    
    def _clear_inputs(self):
        self.email_input.clear()
        self.amount_input.clear()
        self.recipient_input.clear()
    
    def _toggle_mode(self, checked):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())
    
    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()
