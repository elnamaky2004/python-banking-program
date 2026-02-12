import sys
import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QApplication, QPushButton,
    QHBoxLayout, QCheckBox, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
import theme


class transfer_money(QWidget):
    def __init__(self, username, parent_window=None):
        super().__init__()
        self.username = username
        self.parent_window = parent_window

        self.setWindowTitle("Transfer Money")
        self.setGeometry(100, 100, 420, 320)

        self.initui()

        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

        self.refresh_sender_info()

    def initui(self):
        self.mode_label = QLabel(theme.theme_text(), self)
        self.mode_label.setObjectName("modeLabel")

        self.mode_switch = QCheckBox(self)
        self.mode_switch.stateChanged.connect(self.toggle_mode)

        mode_row = QHBoxLayout()
        mode_row.addStretch()
        mode_row.addWidget(self.mode_label)
        mode_row.addWidget(self.mode_switch)
        mode_row.addStretch()

        self.title_label = QLabel("Transfer Money", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("welcome")

        self.acc_info_label = QLabel("", self)
        self.acc_info_label.setAlignment(Qt.AlignCenter)

        self.transfer_to_text = QLineEdit(self)
        self.transfer_to_text.setPlaceholderText("Recipient Account Number")

        self.amount_text = QLineEdit(self)
        self.amount_text.setPlaceholderText("Amount")

        self.transfer_button = QPushButton("Transfer", self)
        self.back_button = QPushButton("Back", self)
        self.back_button.setObjectName("primary")

        self.transfer_button.clicked.connect(self.transfer_money)
        self.back_button.clicked.connect(self.go_back)

        buttons_row = QHBoxLayout()
        buttons_row.addWidget(self.back_button)
        buttons_row.addWidget(self.transfer_button)

        vbox = QVBoxLayout()
        vbox.addLayout(mode_row)
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.acc_info_label)
        vbox.addWidget(self.transfer_to_text)
        vbox.addWidget(self.amount_text)
        vbox.addLayout(buttons_row)

        self.setLayout(vbox)

    def toggle_mode(self):
        theme.set_global_theme(self.mode_switch.isChecked())
        self.mode_label.setText(theme.theme_text())

    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def load_users(self):
        with open("users.json", "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

    def to_number(self, value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    def find_user_by_account_number(self, users, acc_number: str):
        for uname, data in users.items():
            if str(data.get("account_number", "")).strip() == acc_number:
                return uname
        return None

    def refresh_sender_info(self):
        users = self.load_users()
        sender = users.get(self.username, {})
        self.sender_acc = str(sender.get("account_number", "")).strip()
        self.sender_balance = self.to_number(sender.get("account_balance", 0.0), 0.0)

        self.acc_info_label.setText(
            f"Your Account Number: {self.sender_acc}\n"
            f"Your Account Balance: ${self.sender_balance:.2f}"
        )

    def transfer_money(self):
        recipient_acc = self.transfer_to_text.text().strip()
        amount_text = self.amount_text.text().strip()

        if not recipient_acc or not amount_text:
            QMessageBox.warning(self, "Missing Data", "Please enter recipient account number and amount.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Amount", "Amount must be a valid number.")
            return

        if amount <= 0:
            QMessageBox.warning(self, "Invalid Amount", "Amount must be greater than 0.")
            return

        users = self.load_users()

        if self.username not in users:
            QMessageBox.critical(self, "Error", "Sender user not found in users.json.")
            return

        sender_data = users[self.username]
        sender_acc = str(sender_data.get("account_number", "")).strip()
        sender_balance = self.to_number(sender_data.get("account_balance", 0.0), 0.0)

        if recipient_acc == sender_acc:
            QMessageBox.warning(self, "Invalid Transfer", "You cannot transfer to your own account.")
            return

        recipient_username = self.find_user_by_account_number(users, recipient_acc)
        if recipient_username is None:
            QMessageBox.warning(self, "Account Not Found", "Recipient account number not found.")
            return

        if amount > sender_balance:
            QMessageBox.warning(self, "Insufficient Funds", "Insufficient funds for this transfer.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Transfer",
            f"Transfer ${amount:.2f} to {recipient_acc}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        recipient_data = users[recipient_username]
        recipient_balance = self.to_number(recipient_data.get("account_balance", 0.0), 0.0)

        sender_data["account_balance"] = sender_balance - amount
        recipient_data["account_balance"] = recipient_balance + amount

        self.save_users(users)

        self.refresh_sender_info()
        self.transfer_to_text.clear()
        self.amount_text.clear()

        QMessageBox.information(self, "Success", f"Transferred ${amount:.2f} to {recipient_acc} successfully.")


if __name__ == "__main__":
    qt_app = QApplication(sys.argv)
    theme.set_global_theme(False)

    w = transfer_money("elnamaky2004@icloud.com")
    w.show()
    sys.exit(qt_app.exec_())
