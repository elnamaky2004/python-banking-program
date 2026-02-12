from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QHBoxLayout, QCheckBox, QPushButton
)
from PyQt5.QtCore import Qt
import sys
import theme


class about_app(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window

        self.setWindowTitle("About app")
        self.setGeometry(100, 100, 420, 360)
        self.initui()

        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

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

        title_label = QLabel("About This App", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("welcome")

        desc_label = QLabel(
            "Simple Banking App\nA lightweight demo application "
            "for managing basic banking services.",
            self
        )
        desc_label.setAlignment(Qt.AlignCenter)

        author_label = QLabel("Created by Osama Elnamaky", self)
        author_label.setAlignment(Qt.AlignCenter)

        linkedin_label = QLabel(
            'LinkedIn: <a href="https://www.linkedin.com/in/osama-elnamaky-55a11324a/">osama elnamaky</a>',
            self
        )
        linkedin_label.setAlignment(Qt.AlignCenter)
        linkedin_label.setOpenExternalLinks(True)

        github_label = QLabel(
            'GitHub: <a href="https://github.com/elnamaky2004">elnamaky2004</a>',
            self
        )
        github_label.setAlignment(Qt.AlignCenter)
        github_label.setOpenExternalLinks(True)

        version_label = QLabel("Version 1.0.0", self)
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setObjectName("modeLabel")

        back_button = QPushButton("Back", self)
        back_button.setObjectName("primary")
        back_button.clicked.connect(self.go_back)

        vbox = QVBoxLayout()
        vbox.addLayout(mode_row)
        vbox.addSpacing(10)
        vbox.addWidget(title_label)
        vbox.addWidget(desc_label)
        vbox.addSpacing(6)
        vbox.addWidget(author_label)
        vbox.addSpacing(12)
        vbox.addWidget(linkedin_label)
        vbox.addWidget(github_label)
        vbox.addSpacing(15)
        vbox.addWidget(version_label)
        vbox.addSpacing(20)
        vbox.addWidget(back_button)
        vbox.addStretch()

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
    w = about_app()
    w.show()
    sys.exit(app.exec_())
