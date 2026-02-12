from PyQt5.QtWidgets import QApplication

THEME_IS_DARK = False

DARK_STYLE = """
* {
    font-family: "Segoe UI", "Inter", "Arial";
    font-size: 14px;
    color: #E6E6E6;
}

QWidget { background-color: #121212; }
QLabel { color: #EAEAEA; }

QLabel#welcome {
    font-size: 26px;
    font-weight: 700;
    padding: 10px 0;
}

QLabel#modeLabel {
    font-size: 11px;
    color: #BDBDBD;
}

QLineEdit {
    background-color: #1E1E1E;
    border: 1px solid #2C2C2C;
    border-radius: 10px;
    padding: 10px 12px;
    selection-background-color: #3A6FF7;
}

QLineEdit:focus { border: 1px solid #3A6FF7; }

QPushButton {
    background-color: #2A2A2A;
    border: 1px solid #3A3A3A;
    border-radius: 10px;
    padding: 10px 12px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #333333;
    border: 1px solid #4A4A4A;
}

QPushButton:pressed { background-color: #242424; }

QPushButton#primary {
    background-color: #3A6FF7;
    border: 1px solid #3A6FF7;
    color: #FFFFFF;
}

QPushButton#primary:hover {
    background-color: #2F5DE0;
    border: 1px solid #2F5DE0;
}

QPushButton#primary:pressed {
    background-color: #274FC0;
    border: 1px solid #274FC0;
}

QCheckBox { spacing: 0px; }

QCheckBox::indicator {
    width: 50px;
    height: 26px;
}

QCheckBox::indicator:unchecked {
    background-color: #666666;
    border-radius: 13px;
}

QCheckBox::indicator:checked {
    background-color: #3A6FF7;
    border-radius: 13px;
}

QCheckBox::indicator { border: none; }
"""

LIGHT_STYLE = """
* {
    font-family: "Segoe UI", "Inter", "Arial";
    font-size: 14px;
    color: #222222;
}

QWidget { background-color: #F4F6F9; }
QLabel { color: #333333; }

QLabel#welcome {
    font-size: 26px;
    font-weight: 700;
    color: #111111;
    padding: 10px 0;
}

QLabel#modeLabel {
    font-size: 11px;
    color: #7A7A7A;
}

QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #D0D5DD;
    border-radius: 10px;
    padding: 10px 12px;
    selection-background-color: #3A6FF7;
}

QLineEdit:focus { border: 1px solid #3A6FF7; }

QPushButton {
    background-color: #E4E7EC;
    border: 1px solid #D0D5DD;
    border-radius: 10px;
    padding: 10px 12px;
    font-weight: 600;
}

QPushButton:hover { background-color: #DCE0E6; }
QPushButton:pressed { background-color: #C9CDD4; }

QPushButton#primary {
    background-color: #3A6FF7;
    border: 1px solid #3A6FF7;
    color: #FFFFFF;
}

QPushButton#primary:hover { background-color: #2F5DE0; }
QPushButton#primary:pressed { background-color: #274FC0; }

QCheckBox { spacing: 0px; }

QCheckBox::indicator {
    width: 50px;
    height: 26px;
}

QCheckBox::indicator:unchecked {
    background-color: #B0B0B0;
    border-radius: 13px;
}

QCheckBox::indicator:checked {
    background-color: #3A6FF7;
    border-radius: 13px;
}

QCheckBox::indicator { border: none; }
"""

def set_global_theme(is_dark: bool):
    global THEME_IS_DARK
    THEME_IS_DARK = is_dark
    app = QApplication.instance()
    if app is not None:
        app.setStyleSheet(DARK_STYLE if is_dark else LIGHT_STYLE)

def sync_checkbox_to_theme(checkbox):
    checkbox.blockSignals(True)
    checkbox.setChecked(THEME_IS_DARK)
    checkbox.blockSignals(False)

def theme_text():
    return "dark_mode" if THEME_IS_DARK else "light_mode"
