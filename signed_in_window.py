from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QApplication, QPushButton,
    QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import Qt
import json
import sys
import theme
import transfer_money
import account_information
import about_app
import update_info


class window(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username

        with open("users.json", "r") as f:
            users = json.load(f)

        user_data = users.get(username, {})
        self.user_name = user_data.get("name", username)
        self.user_title = user_data.get("title", "")

        self.setWindowTitle(f"{self.user_name}")
        self.setGeometry(100, 100, 400, 260)

        self.init_ui()

        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

    def init_ui(self):
        self.mode_label = QLabel(theme.theme_text(), self)
        self.mode_label.setObjectName("modeLabel")

        self.mode_switch = QCheckBox(self)
        self.mode_switch.stateChanged.connect(self.toggle_mode)

        mode_row = QHBoxLayout()
        mode_row.addStretch()
        mode_row.addWidget(self.mode_label)
        mode_row.addWidget(self.mode_switch)
        mode_row.addStretch()

        welcome_label = QLabel(
            f"Welcome {self.user_title} {self.user_name}!", self
        )
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setObjectName("welcome")

        options_label = QLabel(
            "please select your service from below", self
        )
        options_label.setAlignment(Qt.AlignCenter)

        transfer_button = QPushButton("Transfer Money", self)
        account_info_button = QPushButton("Account Information", self)
        request_money_button = QPushButton("Request Money", self)
        request_loan_button = QPushButton("Request Loan", self)
        app_info_button = QPushButton("About app", self)
        update_button = QPushButton("Update info", self)

        transfer_button.clicked.connect(self.transfer_money)
        account_info_button.clicked.connect(self.account_information)
        request_money_button.clicked.connect(self.request_money)
        request_loan_button.clicked.connect(self.request_loan)
        app_info_button.clicked.connect(self.open_about_app)
        update_button.clicked.connect(self.update_info)

        vbox = QVBoxLayout()
        vbox.addLayout(mode_row)
        vbox.addWidget(welcome_label)
        vbox.addWidget(options_label)
        vbox.addWidget(transfer_button)
        vbox.addWidget(account_info_button)
        vbox.addWidget(request_money_button)
        vbox.addWidget(request_loan_button)
        vbox.addWidget(update_button)
        vbox.addWidget(app_info_button)

        self.setLayout(vbox)

    def transfer_money(self):
        self.next_window = transfer_money.transfer_money(self.username, self)
        self.next_window.show()
        self.hide()


    def account_information(self):
        self.next_window = account_information.account_info(self.username, self)
        self.next_window.show()
        self.hide()

    def request_money(self):
        pass

    def request_loan(self):
        pass

    def open_about_app(self):
        self.next_window = about_app.about_app(self)
        self.next_window.show()
        self.hide()

    def update_info(self):
        self.next_window = update_info.update_info(self.username, self)
        self.next_window.show()
        self.hide()

    def toggle_mode(self):
        theme.set_global_theme(self.mode_switch.isChecked())
        self.mode_label.setText(theme.theme_text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme.set_global_theme(False)

    app_window = window("elnamaky2004@icloud.com")
    app_window.show()
    sys.exit(app.exec_())
