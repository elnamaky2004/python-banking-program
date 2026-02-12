from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QCheckBox, QHBoxLayout
)
import sys
from PyQt5.QtCore import Qt
import json
import theme
import sign_up as signup_module
from signed_in_window import window as SignedInWindow


class sign_in(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("sign in")
        self.setGeometry(100, 100, 400, 300)
        self.next_window = None
        self.initui()

    def initui(self):
        self.welcome_label = QLabel("Welcome", self)
        self.welcome_label.setObjectName("welcome")

        self.mode_label = QLabel(theme.theme_text(), self)
        self.mode_label.setObjectName("modeLabel")

        self.username_text = QLineEdit(self)
        self.username_text.setPlaceholderText("Username (Email)")
        self.username_text.setAlignment(Qt.AlignCenter)

        self.password_text = QLineEdit(self)
        self.password_text.setPlaceholderText("Password")
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setAlignment(Qt.AlignCenter)

        self.show_password_button = QCheckBox("Show Password", self)
        self.show_password_button.setCursor(Qt.PointingHandCursor)
        self.show_password_button.toggled.connect(self.show_password)

        self.signin_button = QPushButton("Sign In", self)
        self.signin_button.setObjectName("primary")
        self.signin_button.clicked.connect(self.sign_in_user)

        self.label2 = QLabel("dont have an account?", self)
        self.label2.setAlignment(Qt.AlignCenter)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.open_sign_up)

        self.mode_button = QCheckBox("", self)
        self.mode_button.setCursor(Qt.PointingHandCursor)
        self.mode_button.toggled.connect(self.toggle_mode)

        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        vbox = QVBoxLayout()
        vbox.setSpacing(12)
        vbox.setContentsMargins(18, 16, 18, 16)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self.welcome_label)
        top_layout.addStretch()
        top_layout.addWidget(self.mode_label, 0, Qt.AlignVCenter)
        top_layout.addWidget(self.mode_button, 0, Qt.AlignVCenter)

        vbox.addLayout(top_layout)
        vbox.addWidget(self.error_label)
        vbox.addWidget(self.username_text)
        vbox.addWidget(self.password_text)
        vbox.addWidget(self.show_password_button)
        vbox.addWidget(self.signin_button)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.signup_button)
        vbox.addStretch()

        self.setLayout(vbox)

        theme.sync_checkbox_to_theme(self.mode_button)
        self.mode_label.setText(theme.theme_text())

    def show_password(self, checked):
        self.password_text.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)

    def toggle_mode(self, checked):
        theme.set_global_theme(checked)
        self.mode_label.setText(theme.theme_text())

    def open_sign_up(self):
        self.next_window = signup_module.sign_up()
        self.next_window.show()
        self.close()

    def sign_in_user(self):
        user_name = self.username_text.text().strip()
        password = self.password_text.text().strip()

        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except Exception:
            users = {}

        if user_name in users and users[user_name].get("password") == password:
            if user_name in users and users[user_name].get("password") == password:
                self.next_window = SignedInWindow(user_name)  
                self.next_window.show()
                self.close()
                return

        self.error_label.setText("Invalid username or password")
        self.error_label.show()
    

if __name__ == "__main__":
    qt_app = QApplication(sys.argv)
    theme.set_global_theme(theme.THEME_IS_DARK)
    window = sign_in()
    window.show()
    sys.exit(qt_app.exec_())
