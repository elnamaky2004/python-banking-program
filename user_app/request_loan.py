from PyQt5.QtWidgets import (
    QLineEdit, QWidget, QLabel, QVBoxLayout, QApplication, QPushButton,
    QHBoxLayout, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt
import json
import os
import sys
import datetime
import theme
def load_users():
    users_file = os.path.join(os.path.dirname(__file__), "users.json")
    try:
        with open(users_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    users_file = os.path.join(os.path.dirname(__file__), "users.json")
    try:
        with open(users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        raise Exception(f"Failed to save users: {e}")

def load_loan_requests():
    loan_file = os.path.join(os.path.dirname(__file__), "..", "worker_app", "loan_requests.json")
    try:
        with open(loan_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_loan_requests(loan_requests):
    loan_file = os.path.join(os.path.dirname(__file__), "..", "worker_app", "loan_requests.json")
    try:
        with open(loan_file, "w", encoding="utf-8") as f:
            json.dump(loan_requests, f, indent=4)
    except Exception as e:
        raise Exception(f"Failed to save loan requests: {e}")
def _make_theme_switch(parent: QWidget):
    try:
        return theme.AnimatedToggleSwitch(parent)
    except Exception:
        fallback = QCheckBox(parent)
        fallback.setCursor(Qt.PointingHandCursor)
        return fallback
    
class RequestLoanWindow(QWidget):
    def __init__(self, username, parent_window=None):
        super().__init__()
        self.username = username
        self.parent_window = parent_window

        users = load_users()
        user_data = users.get(username, {})
        self.user_name = user_data.get("name", username)
        self.user_title = user_data.get("title", "")
        self.user_password = user_data.get("password", None)
        self.account_number = user_data.get("account_number", "N/A")

        self.setWindowTitle(f"Request Loan - {self.user_name}")
        self.setMinimumSize(500, 550)

        self.init_ui()

        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

    def init_ui(self):
        # Header with theme toggle
        self.mode_label = QLabel(theme.theme_text(), self)
        self.mode_label.setObjectName("modeLabel")

        self.mode_switch = _make_theme_switch(self)
        self.mode_switch.toggled.connect(self.toggle_mode)

        mode_row = QHBoxLayout()
        mode_row.addStretch()
        mode_row.addWidget(self.mode_label)
        mode_row.addWidget(self.mode_switch)

        # Title
        title_label = QLabel("Request Loan", self)
        title_label.setObjectName("welcome")
        title_label.setAlignment(Qt.AlignCenter)

        # User info
        user_info_label = QLabel(f"Account: {self.account_number} | Name: {self.user_name}", self)
        user_info_label.setAlignment(Qt.AlignCenter)
        user_info_label.setStyleSheet("font-size: 12px; color: #888888;")

        # Loan amount input
        loan_amount_label = QLabel("Loan Amount (EGP):", self)
        self.loan_input = QLineEdit(self)
        self.loan_input.setPlaceholderText("Enter amount (e.g., 10000)")

        # Loan purpose input
        purpose_label = QLabel("Purpose of Loan:", self)
        self.purpose_input = QLineEdit(self)
        self.purpose_input.setPlaceholderText("e.g., Home renovation, Business expansion")

        # Repayment period input
        period_label = QLabel("Repayment Period (months):", self)
        self.period_input = QLineEdit(self)
        self.period_input.setPlaceholderText("Enter number of months (e.g., 12, 24, 36)")

        # Password input
        password_label = QLabel("Confirm Password:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter your password to confirm")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Buttons
        submit_btn = QPushButton("Submit Loan Request", self)
        submit_btn.setObjectName("primary")
        submit_btn.setMinimumHeight(40)
        submit_btn.clicked.connect(self.submit_loan_request)

        back_btn = QPushButton("Back", self)
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(self.go_back)

        button_row = QHBoxLayout()
        button_row.addWidget(back_btn)
        button_row.addStretch()
        button_row.addWidget(submit_btn)

        # Layout
        vbox = QVBoxLayout()
        vbox.setSpacing(12)
        vbox.setContentsMargins(20, 18, 20, 18)
        vbox.addLayout(mode_row)
        vbox.addWidget(title_label)
        vbox.addWidget(user_info_label)
        vbox.addSpacing(10)
        vbox.addWidget(loan_amount_label)
        vbox.addWidget(self.loan_input)
        vbox.addWidget(purpose_label)
        vbox.addWidget(self.purpose_input)
        vbox.addWidget(period_label)
        vbox.addWidget(self.period_input)
        vbox.addWidget(password_label)
        vbox.addWidget(self.password_input)
        vbox.addSpacing(10)
        vbox.addLayout(button_row)
        vbox.addStretch()

        self.setLayout(vbox)

    def toggle_mode(self):
        theme.set_global_theme(self.mode_switch.isChecked())
        self.mode_label.setText(theme.theme_text())

    def submit_loan_request(self):
        # Get input values
        loan_amount_str = self.loan_input.text().strip()
        purpose = self.purpose_input.text().strip()
        period_str = self.period_input.text().strip()
        password = self.password_input.text().strip()

        # Validate inputs
        if not loan_amount_str:
            QMessageBox.warning(self, "Missing Information", "Please enter the loan amount.")
            return

        if not purpose:
            QMessageBox.warning(self, "Missing Information", "Please enter the purpose of the loan.")
            return

        if not period_str:
            QMessageBox.warning(self, "Missing Information", "Please enter the repayment period.")
            return

        if not password:
            QMessageBox.warning(self, "Missing Information", "Please enter your password to confirm.")
            return

        # Validate password
        if password != self.user_password:
            QMessageBox.critical(self, "Authentication Failed", "Incorrect password. Please try again.")
            self.password_input.clear()
            return

        # Validate loan amount
        try:
            loan_amount = float(loan_amount_str)
            if loan_amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            QMessageBox.warning(self, "Invalid Amount", "Please enter a valid positive number for the loan amount.")
            return

        # Validate repayment period
        try:
            repayment_period = int(period_str)
            if repayment_period <= 0:
                raise ValueError("Period must be positive")
        except ValueError:
            QMessageBox.warning(self, "Invalid Period", "Please enter a valid positive integer for the repayment period in months.")
            return

        # Load existing loan requests
        try:
            loan_requests = load_loan_requests()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load loan requests: {e}")
            return

        # Create loan request entry
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request_id = f"{self.username}_{timestamp.replace(' ', '_').replace(':', '-')}"

        loan_request = {
            "username": self.username,
            "name": self.user_name,
            "account_number": self.account_number,
            "amount": loan_amount,
            "purpose": purpose,
            "repayment_period_months": repayment_period,
            "request_date": timestamp,
            "status": "pending"
        }

        loan_requests[request_id] = loan_request

        # Save loan requests
        try:
            save_loan_requests(loan_requests)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save loan request: {e}")
            return

        # Show success message
        QMessageBox.information(
            self,
            "Request Submitted",
            f"Your loan request for {loan_amount:,.2f} EGP has been submitted successfully.\n\n"
            f"Request ID: {request_id}\n"
            f"Status: Pending Approval\n\n"
            f"Please wait for a worker to review your request."
        )

        # Clear form
        self.loan_input.clear()
        self.purpose_input.clear()
        self.period_input.clear()
        self.password_input.clear()

    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RequestLoanWindow("elnamaky2004@icloud.com")
    window.show()
    sys.exit(app.exec_())