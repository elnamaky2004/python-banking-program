import sys
import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QApplication, QPushButton,
    QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import Qt
import theme


class account_info(QWidget):
    def __init__(self, username, parent_window=None):
        super().__init__()
        self.username = username
        self.parent_window = parent_window

        self.setWindowTitle("Account Information")
        self.setGeometry(100, 100, 420, 320)

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

        with open("users.json", "r") as f:
            users = json.load(f)

        user_data = users.get(self.username, {})
        name = user_data.get("name", "N/A")
        title = user_data.get("title", "")
        age = user_data.get("age", "N/A")
        account_balance = user_data.get("account_balance", "N/A")
        account_number = user_data.get("account_number", "N/A")

        header = QLabel("Account Information", self)
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("welcome")

        name_label = QLabel(f"Name: {title} {name}".strip(), self)
        age_label = QLabel(f"Age: {age}", self)
        balance_label = QLabel(f"Account Balance: ${account_balance}", self)
        account_number_label = QLabel(f"Account Number: {account_number}", self)

        name_label.setAlignment(Qt.AlignCenter)
        age_label.setAlignment(Qt.AlignCenter)
        balance_label.setAlignment(Qt.AlignCenter)
        account_number_label.setAlignment(Qt.AlignCenter)

        back_button = QPushButton("Back", self)
        back_button.setObjectName("primary")
        back_button.clicked.connect(self.go_back)

        vbox = QVBoxLayout()
        vbox.addLayout(mode_row)
        vbox.addWidget(header)
        vbox.addSpacing(10)
        vbox.addWidget(name_label)
        vbox.addWidget(age_label)
        vbox.addWidget(balance_label)
        vbox.addWidget(account_number_label)
        vbox.addStretch()
        vbox.addWidget(back_button)

        self.setLayout(vbox)

    def toggle_mode(self):
        theme.set_global_theme(self.mode_switch.isChecked())
        self.mode_label.setText(theme.theme_text())

    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme.set_global_theme(False)
    demo = account_info("elnamaky2004@icloud.com", None)
    demo.show()
    sys.exit(app.exec_())
