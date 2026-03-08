from PyQt5.QtWidgets import QApplication, QAbstractButton
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPen

THEME_IS_DARK = False

CUSTOM_LIGHT_STYLE = """
QMainWindow {
    background-color:rgb(82, 82, 82);
}
QTextEdit {
    background-color:rgb(42, 42, 42);
    color: rgb(0, 255, 0);
}
QPushButton{
    border-style: outset;
    border-width: 2px;
    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-bottom-color: rgb(58, 58, 58);
    border-bottom-width: 1px;
    border-style: solid;
    color: rgb(255, 255, 255);
    padding: 2px;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
}
QPushButton:hover{
    border-style: outset;
    border-width: 2px;
    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
    border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
    border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(180, 180, 180, 255), stop:1 rgba(110, 110, 110, 255));
    border-bottom-color: rgb(115, 115, 115);
    border-bottom-width: 1px;
    border-style: solid;
    color: rgb(255, 255, 255);
    padding: 2px;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(157, 157, 157, 255));
}
QPushButton:pressed{
    border-style: outset;
    border-width: 2px;
    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(62, 62, 62, 255), stop:1 rgba(22, 22, 22, 255));
    border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-bottom-color: rgb(58, 58, 58);
    border-bottom-width: 1px;
    border-style: solid;
    color: rgb(255, 255, 255);
    padding: 2px;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
}
QPushButton:disabled{
    border-style: outset;
    border-width: 2px;
    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-bottom-color: rgb(58, 58, 58);
    border-bottom-width: 1px;
    border-style: solid;
    color: rgb(0, 0, 0);
    padding: 2px;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(57, 57, 57, 255), stop:1 rgba(77, 77, 77, 255));
}
QLineEdit {
    border-width: 1px; border-radius: 4px;
    border-color: rgb(58, 58, 58);
    border-style: inset;
    padding: 0 8px;
    color: rgb(255, 255, 255);
    background:rgb(100, 100, 100);
    selection-background-color: rgb(187, 187, 187);
    selection-color: rgb(60, 63, 65);
}
QLabel {
    color:rgb(0,0,0);	
}
QProgressBar {
    text-align: center;
    color: rgb(240, 240, 240);
    border-width: 1px; 
    border-radius: 10px;
    border-color: rgb(58, 58, 58);
    border-style: inset;
    background-color:rgb(77,77,77);
}
QProgressBar::chunk {
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 rgba(87, 97, 106, 255), stop:1 rgba(93, 103, 113, 255));
    border-radius: 5px;
}
QMenuBar {
    background:rgb(82, 82, 82);
}
QMenuBar::item {
    color:rgb(223,219,210);
    spacing: 3px;
    padding: 1px 4px;
    background: transparent;
}

QMenuBar::item:selected {
    background:rgb(115, 115, 115);
}
QMenu::item:selected {
    color:rgb(255,255,255);
    border-width:2px;
    border-style:solid;
    padding-left:18px;
    padding-right:8px;
    padding-top:2px;
    padding-bottom:3px;
    background:qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 rgba(87, 97, 106, 255), stop:1 rgba(93, 103, 113, 255));
    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(62, 62, 62, 255));
    border-bottom-color: rgb(58, 58, 58);
    border-bottom-width: 1px;
}
QMenu::item {
    color:rgb(223,219,210);
    background-color:rgb(78,78,78);
    padding-left:20px;
    padding-top:4px;
    padding-bottom:4px;
    padding-right:10px;
}
QMenu{
    background-color:rgb(78,78,78);
}
QTabWidget {
    color:rgb(0,0,0);
    background-color:rgb(247,246,246);
}
QTabWidget::pane {
        border-color: rgb(77,77,77);
        background-color:rgb(101,101,101);
        border-style: solid;
        border-width: 1px;
        	border-radius: 6px;
}
QTabBar::tab {
    padding:2px;
    color:rgb(250,250,250);
  	background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(77, 77, 77, 255), stop:1 rgba(97, 97, 97, 255));
    border-style: solid;
    border-width: 2px;
  	border-top-right-radius:4px;
   border-top-left-radius:4px;
    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(95, 92, 93, 255));
    border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(95, 92, 93, 255));
    border-left-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(115, 115, 115, 255), stop:1 rgba(95, 92, 93, 255));
    border-bottom-color: rgb(101,101,101);
}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
  	background-color:rgb(101,101,101);
  	margin-left: 0px;
  	margin-right: 1px;
}
QTabBar::tab:!selected {
    	margin-top: 1px;
        margin-right: 1px;
}
QCheckBox {
    color:rgb(223,219,210);
    padding: 2px;
}
QCheckBox:hover {
    border-radius:4px;
    border-style:solid;
    padding-left: 1px;
    padding-right: 1px;
    padding-bottom: 1px;
    padding-top: 1px;
    border-width:1px;
    border-color: rgb(87, 97, 106);
    background-color:qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 rgba(87, 97, 106, 150), stop:1 rgba(93, 103, 113, 150));
}
QCheckBox::indicator:checked {
    border-radius:4px;
    border-style:solid;
    border-width:1px;
    border-color: rgb(180,180,180);
  	background-color:qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:0.5, y2:0.3, stop:0 rgba(87, 97, 106, 255), stop:1 rgba(93, 103, 113, 255));
}
QCheckBox::indicator:unchecked {
    border-radius:4px;
    border-style:solid;
    border-width:1px;
    border-color: rgb(87, 97, 106);
  	background-color:rgb(255,255,255);
}
QStatusBar {
    color:rgb(240,240,240);
}
"""


def _palette(is_dark: bool) -> dict:
    if is_dark:
        return {
            "bg": "#0B0F14",
            "panel": "#0F1722",
            "text": "#E8EEF6",
            "muted": "#9AA4B2",
            "border": "#1E2A3A",
            "input_bg": "#0F1722",
            "hover": "#162233",
            "pressed": "#0C131D",
            "primary": "#4F8CFF",
            "primary_hover": "#3D7CFF",
            "primary_pressed": "#2D6CFF",
            "focus": "#4F8CFF",
            "switch_track_off": "#273246",
            "switch_track_on": "#4F8CFF",
            "switch_knob": "#FFFFFF",
        }
    return {
        "bg": "#F6F8FC",
        "panel": "#FFFFFF",
        "text": "#121826",
        "muted": "#667085",
        "border": "#D0D5DD",
        "input_bg": "#FFFFFF",
        "hover": "#EEF2F7",
        "pressed": "#E4E9F2",
        "primary": "#3A6FF7",
        "primary_hover": "#2F5DE0",
        "primary_pressed": "#274FC0",
        "focus": "#3A6FF7",
        "switch_track_off": "#C7CFDC",
        "switch_track_on": "#3A6FF7",
        "switch_knob": "#FFFFFF",
    }


def _build_qss(is_dark: bool) -> str:
    if not is_dark:
        return CUSTOM_LIGHT_STYLE

    try:
        import qdarkstyle

        qdark_qss = qdarkstyle.load_stylesheet_pyqt5()
        return qdark_qss + """
QLabel#modeLabel {
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
    except Exception:
        pass

    return """
* {
    font-family: "Segoe UI", "Inter", "Arial";
    font-size: 14px;
    color: #E6EAF2;
}

QWidget {
    background-color: #0F1420;
}

QMainWindow {
    background-color: #0D111B;
}

QLabel {
    color: #E6EAF2;
}

QLabel#welcome {
    font-size: 26px;
    font-weight: 700;
    color: #F5F8FF;
    padding: 10px 0;
}

QLabel#modeLabel {
    font-size: 11px;
    color: #9AA7BE;
}

QLineEdit, QTextEdit, QListWidget, QComboBox {
    background-color: #141C2C;
    border: 1px solid #24334C;
    border-radius: 10px;
    color: #E6EAF2;
    selection-background-color: #4F8CFF;
    selection-color: #FFFFFF;
}

QLineEdit {
    padding: 10px 12px;
}

QTextEdit, QListWidget {
    padding: 8px;
}

QLineEdit:focus, QTextEdit:focus, QListWidget:focus, QComboBox:focus {
    border: 1px solid #4F8CFF;
}

QComboBox {
    padding: 8px 12px;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    border: 1px solid #2B3D5D;
    background-color: #121A2A;
    selection-background-color: #2A4064;
    selection-color: #FFFFFF;
    outline: 0;
}

QPushButton {
    background-color: qlineargradient(
        spread:pad, x1:0, y1:0, x2:0, y2:1,
        stop:0 #27354D, stop:1 #1E2A3F
    );
    border: 1px solid #314763;
    border-radius: 10px;
    padding: 9px 12px;
    font-weight: 600;
    color: #EAF1FF;
}

QPushButton:hover {
    background-color: qlineargradient(
        spread:pad, x1:0, y1:0, x2:0, y2:1,
        stop:0 #314565, stop:1 #243552
    );
    border: 1px solid #44608A;
}

QPushButton:pressed {
    background-color: #1A2638;
    border: 1px solid #3A5278;
}

QPushButton:disabled {
    background-color: #1A2232;
    border: 1px solid #28364D;
    color: #6E7F9D;
}

QPushButton#primary {
    background-color: qlineargradient(
        spread:pad, x1:0, y1:0, x2:0, y2:1,
        stop:0 #5A99FF, stop:1 #3F79E8
    );
    border: 1px solid #4F8CFF;
    color: #FFFFFF;
}

QPushButton#primary:hover {
    background-color: qlineargradient(
        spread:pad, x1:0, y1:0, x2:0, y2:1,
        stop:0 #70A7FF, stop:1 #4D86F0
    );
    border: 1px solid #6AA4FF;
}

QPushButton#primary:pressed {
    background-color: #3566C8;
    border: 1px solid #2F5CAF;
}

QCheckBox {
    spacing: 8px;
    color: #D7DFEE;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #4A6085;
    background-color: #162132;
}

QCheckBox::indicator:checked {
    background-color: #4F8CFF;
    border: 1px solid #4F8CFF;
}

QCheckBox#themeSwitch::indicator {
    width: 52px;
    height: 28px;
    border: none;
}

QCheckBox#themeSwitch::indicator:unchecked {
    background-color: #2A3850;
    border-radius: 14px;
}

QCheckBox#themeSwitch::indicator:checked {
    background-color: #4F8CFF;
    border-radius: 14px;
}

QProgressBar {
    border: 1px solid #2A3B58;
    border-radius: 10px;
    text-align: center;
    color: #EAF0FB;
    background-color: #141D2D;
}

QProgressBar::chunk {
    border-radius: 8px;
    background-color: qlineargradient(
        spread:pad, x1:0, y1:0, x2:1, y2:0,
        stop:0 #4F8CFF, stop:1 #66A2FF
    );
}

QMenuBar {
    background-color: #111827;
}

QMenuBar::item {
    color: #D8E0F0;
    spacing: 4px;
    padding: 4px 8px;
    background: transparent;
    border-radius: 6px;
}

QMenuBar::item:selected {
    background: #1F2E45;
}

QMenu {
    background-color: #121A2A;
    border: 1px solid #2A3D5D;
    padding: 6px;
}

QMenu::item {
    color: #D8E0F0;
    padding: 6px 22px 6px 12px;
    border-radius: 6px;
}

QMenu::item:selected {
    color: #FFFFFF;
    background-color: #2A4064;
}

QTabWidget::pane {
    border: 1px solid #2A3B58;
    background-color: #111A2A;
    border-radius: 8px;
    top: -1px;
}

QTabBar::tab {
    color: #CBD6EA;
    background-color: #1A273A;
    border: 1px solid #2E4465;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-width: 88px;
    padding: 7px 12px;
    margin-right: 4px;
}

QTabBar::tab:hover {
    background-color: #22334D;
    color: #EAF1FF;
}

QTabBar::tab:selected {
    background-color: #2A4064;
    color: #FFFFFF;
    border: 1px solid #4F8CFF;
    border-bottom: none;
}

QStatusBar {
    color: #CCD8ED;
}
"""


def set_global_theme(is_dark: bool):
    global THEME_IS_DARK
    THEME_IS_DARK = is_dark
    app = QApplication.instance()
    if app is not None:
        app.setStyleSheet(_build_qss(is_dark))


def sync_checkbox_to_theme(toggle_widget):
    toggle_widget.blockSignals(True)
    toggle_widget.setChecked(THEME_IS_DARK)
    # Update position for AnimatedToggleSwitch without animation
    if hasattr(toggle_widget, 'set_pos'):
        toggle_widget.set_pos(1.0 if THEME_IS_DARK else 0.0)
    toggle_widget.blockSignals(False)


def theme_text() -> str:
    return "dark_mode" if THEME_IS_DARK else "light_mode"


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