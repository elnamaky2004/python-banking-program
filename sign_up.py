from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QCheckBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
import json
import sys
import theme


class sign_up(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("sign up")
        self.setGeometry(100, 100, 400, 300)
        self.next_window = None
        self.initui()

    def initui(self):
        self.sign_up_label = QLabel("Sign Up", self)

        self.mode_label = QLabel(theme.theme_text(), self)
        self.mode_label.setObjectName("modeLabel")

        self.mode_switch = QCheckBox("", self)
        self.mode_switch.setCursor(Qt.PointingHandCursor)
        self.mode_switch.toggled.connect(self.toggle_mode)

        self.name_text = QLineEdit(self)
        self.name_text.setPlaceholderText("Name")

        self.title_text = QLineEdit(self)
        self.title_text.setPlaceholderText("Title (e.g., Eng, Dr, etc)")

        self.username_text = QLineEdit(self)
        self.username_text.setPlaceholderText("Username (Email)")

        self.password_text = QLineEdit(self)
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setPlaceholderText("Password")

        self.show_password_cb = QCheckBox("Show", self)
        self.show_password_cb.setCursor(Qt.PointingHandCursor)
        self.show_password_cb.toggled.connect(self.toggle_show_password)

        self.retype_password_text = QLineEdit(self)
        self.retype_password_text.setEchoMode(QLineEdit.Password)
        self.retype_password_text.setPlaceholderText("Retype Password")

        self.age_text = QLineEdit(self)
        self.age_text.setPlaceholderText("Age")

        self.account_balance_text = QLineEdit(self)
        self.account_balance_text.setPlaceholderText("Account Balance")

        self.account_number_text = QLineEdit(self)
        self.account_number_text.setPlaceholderText("Account Number")

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.sign_up_user)

        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        vbox = QVBoxLayout()
        vbox.setSpacing(12)
        vbox.setContentsMargins(18, 16, 18, 16)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self.sign_up_label)
        top_layout.addStretch()
        top_layout.addWidget(self.mode_label, 0, Qt.AlignVCenter)
        top_layout.addWidget(self.mode_switch, 0, Qt.AlignVCenter)

        vbox.addLayout(top_layout)
        vbox.addWidget(self.error_label)
        vbox.addWidget(self.name_text)
        vbox.addWidget(self.title_text)
        vbox.addWidget(self.username_text)

        password_row = QHBoxLayout()
        password_row.setSpacing(8)
        password_row.addWidget(self.password_text)
        password_row.addWidget(self.show_password_cb, 0, Qt.AlignVCenter)
        vbox.addLayout(password_row)

        vbox.addWidget(self.retype_password_text)
        vbox.addWidget(self.age_text)
        vbox.addWidget(self.account_balance_text)
        vbox.addWidget(self.account_number_text)
        vbox.addWidget(self.signup_button)
        vbox.addStretch()

        self.setLayout(vbox)

        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

    def toggle_mode(self, checked):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())

    def toggle_show_password(self, checked):
        self.password_text.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)

    def sign_up_user(self):
        name = self.name_text.text().strip()
        title = self.title_text.text().strip()
        username = self.username_text.text().strip()
        password = self.password_text.text().strip()
        retype_password = self.retype_password_text.text().strip()
        age = self.age_text.text().strip()
        account_balance = self.account_balance_text.text().strip()
        account_number = self.account_number_text.text().strip()

        if not all([name, title, username, password, retype_password, age, account_balance, account_number]):
            self.error_label.setText("Please fill all fields")
            self.error_label.show()
            return

        if password != retype_password:
            self.error_label.setText("Passwords do not match")
            self.error_label.show()
            return

        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except Exception:
            users = {}

        if username in users:
            self.error_label.setText("Username already exists")
            self.error_label.show()
            return
        if len(password) < 6:
            self.error_label.setText("password must be at least 6 characters")
            self.error_label.show()
            return
        if not age.isdigit() or int(age) < 18:
            self.error_label.setText("invalid age") if not age.isdigit() else self.error_label.setText("age must be at least 18")
            self.error_label.show()
            return
        users[username] = {
            "name": name,
            "title": title,
            "password": password,
            "age": age,
            "account_balance": account_balance,
            "account_number": account_number
        }

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

        from app import sign_in
        self.next_window = sign_in()
        self.next_window.show()
        self.close()
if __name__ == "__main__":
    qt_app = QApplication(sys.argv)
    theme.set_global_theme(theme.THEME_IS_DARK)
    window = sign_up()
    window.show()
    sys.exit(qt_app.exec_())