import sys
import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QApplication, QPushButton,
    QHBoxLayout, QCheckBox, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
import theme


class update_info(QWidget):
    def __init__(self, username, parent_window=None):
        super().__init__()
        self.username = username
        self.parent_window = parent_window

        self.setWindowTitle("Update Information")
        self.setGeometry(100, 100, 440, 420)

        self.init_ui()

        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

        self.load_current_data()

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

        header = QLabel("Update Your Info", self)
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("welcome")

        hint = QLabel("Leave fields empty to keep them unchanged.", self)
        hint.setAlignment(Qt.AlignCenter)
        hint.setObjectName("modeLabel")

        self.current_label = QLabel("", self)
        self.current_label.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("New Username (Email)")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("New Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.retry_password_input = QLineEdit(self)
        self.retry_password_input.setPlaceholderText("Retry Password")
        self.retry_password_input.setEchoMode(QLineEdit.Password)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_changes)

        self.back_button = QPushButton("Back", self)
        self.back_button.setObjectName("primary")
        self.back_button.clicked.connect(self.go_back)

        buttons_row = QHBoxLayout()
        buttons_row.addWidget(self.back_button)
        buttons_row.addWidget(self.save_button)

        vbox = QVBoxLayout()
        vbox.addLayout(mode_row)
        vbox.addWidget(header)
        vbox.addSpacing(6)
        vbox.addWidget(hint)
        vbox.addSpacing(10)
        vbox.addWidget(self.current_label)
        vbox.addSpacing(10)
        vbox.addWidget(self.username_input)
        vbox.addWidget(self.password_input)
        vbox.addWidget(self.retry_password_input)
        vbox.addSpacing(12)
        vbox.addLayout(buttons_row)

        self.setLayout(vbox)

    def toggle_mode(self):
        theme.set_global_theme(self.mode_switch.isChecked())
        self.mode_label.setText(theme.theme_text())

    def load_users(self):
        with open("users.json", "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

    def load_current_data(self):
        users = self.load_users()
        user_data = users.get(self.username, {})

        acc_num = user_data.get("account_number", "N/A")
        self.current_label.setText(f"Current Username: {self.username}\nAccount: {acc_num}")

    def set_parent_username(self, new_username):
        if not self.parent_window:
            return
        try:
            self.parent_window.username = new_username
        except Exception:
            pass

        try:
            if hasattr(self.parent_window, "refresh"):
                self.parent_window.refresh()
        except Exception:
            pass

    def save_changes(self):
        new_username = self.username_input.text().strip()
        new_password = self.password_input.text()
        retry_password = self.retry_password_input.text()

        if not new_username and not new_password and not retry_password:
            QMessageBox.information(self, "No Changes", "No fields were filled. Nothing to update.")
            return

        if (new_password or retry_password) and (new_password != retry_password):
            QMessageBox.warning(self, "Password Mismatch", "Password and retry password do not match.")
            return

        if (new_password or retry_password) and (not new_password or not retry_password):
            QMessageBox.warning(self, "Missing Data", "Please fill both password fields to update the password.")
            return

        users = self.load_users()
        if self.username not in users:
            QMessageBox.critical(self, "Error", "User not found in users.json.")
            return

        old_username = self.username
        user_record = users[old_username]

        if new_password:
            user_record["password"] = new_password

        if new_username:
            if new_username in users and new_username != old_username:
                QMessageBox.warning(self, "Username Exists", "This username already exists. Choose another one.")
                return

            users[new_username] = user_record
            if new_username != old_username:
                del users[old_username]

            self.username = new_username
            self.set_parent_username(new_username)

        self.save_users(users)
        self.username_input.clear()
        self.password_input.clear()
        self.retry_password_input.clear()

        self.load_current_data()
        QMessageBox.information(self, "Saved", "Your information has been updated.")

    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme.set_global_theme(False)
    window = update_info("elnamaky2004@icloud.com", None)
    window.show()
    sys.exit(app.exec_())
