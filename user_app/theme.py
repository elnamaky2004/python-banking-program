from PyQt5.QtWidgets import QApplication, QAbstractButton
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPen

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
        if is_dark:
            try:
                import qdarkstyle
                qdark_qss = qdarkstyle.load_stylesheet_pyqt5()
                app_specific = """
* {
    font-family: "Segoe UI", "Inter", "Arial";
    font-size: 14px;
}

QLabel {
    font-size: 14px;
}

QLabel#welcome {
    font-size: 26px;
    font-weight: 700;
    padding: 10px 0;
}

QLabel#modeLabel {
    font-size: 11px;
    color: #A8B3C7;
}

QPushButton#primary {
    background-color: #4F8CFF;
    border: 1px solid #4F8CFF;
    color: #FFFFFF;
    border-radius: 4px;
    padding: 6px 10px;
    font-weight: 600;
}

QPushButton#primary:hover {
    background-color: #3D7CFF;
    border: 1px solid #3D7CFF;
}

QPushButton#primary:pressed {
    background-color: #2D6CFF;
    border: 1px solid #2D6CFF;
}
"""
                app.setStyleSheet(qdark_qss + app_specific)
            except Exception:
                app.setStyleSheet(DARK_STYLE)
        else:
            app.setStyleSheet(LIGHT_STYLE)

def sync_checkbox_to_theme(checkbox):
    checkbox.blockSignals(True)
    checkbox.setChecked(THEME_IS_DARK)
    # Update position for AnimatedToggleSwitch without animation
    if hasattr(checkbox, 'set_pos'):
        checkbox.set_pos(1.0 if THEME_IS_DARK else 0.0)
    checkbox.blockSignals(False)

def theme_text():
    return "dark_mode" if THEME_IS_DARK else "light_mode"


def _palette(is_dark: bool) -> dict:
    """Color palette for AnimatedToggleSwitch"""
    if is_dark:
        return {
            "border": "#2C2C2C",
            "focus": "#3A6FF7",
            "switch_track_off": "#666666",
            "switch_track_on": "#3A6FF7",
            "switch_knob": "#FFFFFF",
        }
    return {
        "border": "#D0D5DD",
        "focus": "#3A6FF7",
        "switch_track_off": "#B0B0B0",
        "switch_track_on": "#3A6FF7",
        "switch_knob": "#FFFFFF",
    }


class AnimatedToggleSwitch(QAbstractButton):
    def __init__(self, parent=None, width: int = 52, height: int = 28):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)

        self._w = int(width)
        self._h = int(height)
        self.setFixedSize(self._w, self._h)

        # Initialize position based on global theme, not current checked state
        self._pos = 1.0 if THEME_IS_DARK else 0.0

        self._anim = QPropertyAnimation(self, b"pos", self)
        self._anim.setDuration(180)
        self._anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.toggled.connect(self._animate)

    def _animate(self, checked: bool):
        self._anim.stop()
        self._anim.setStartValue(self._pos)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()

    def get_pos(self) -> float:
        return self._pos

    def set_pos(self, value: float):
        self._pos = float(value)
        self.update()

    pos = pyqtProperty(float, fget=get_pos, fset=set_pos)

    def paintEvent(self, _event):
        p = _palette(THEME_IS_DARK)

        track_radius = self._h / 2.0
        margin = 3
        knob_d = self._h - 2 * margin
        x_min = margin
        x_max = self._w - margin - knob_d
        knob_x = x_min + (x_max - x_min) * self._pos

        track_color = QColor(p["switch_track_on"] if self.isChecked() else p["switch_track_off"])
        knob_color = QColor(p["switch_knob"])
        border_color = QColor(p["border"])

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(track_color)
        painter.drawRoundedRect(0, 0, self._w, self._h, float(track_radius), float(track_radius))

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(knob_color)
        painter.drawEllipse(int(knob_x), int(margin), int(knob_d), int(knob_d))

        if self.hasFocus():
            focus = QColor(p["focus"])
            focus.setAlpha(120)
            painter.setPen(QPen(focus, 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(1, 1, self._w - 2, self._h - 2, float(track_radius), float(track_radius))

        painter.end()
