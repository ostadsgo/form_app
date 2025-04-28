from pathlib import Path
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFrame

BASE_DIR = Path(__file__).parent.parent
UI_DIR = BASE_DIR / "ui"
FORM_DIR = UI_DIR / "form"


def load_ui(filename):
    loader = QUiLoader()
    ui = loader.load(UI_DIR / filename)
    return ui


def vertical_line():
    vertical_line = QFrame()
    vertical_line.setFrameShape(QFrame.VLine)
    vertical_line.setFrameShadow(QFrame.Sunken)
    return vertical_line


def toggle_visibility(widget):
    if widget.isVisible():
        widget.setVisible(False)
    else:
        widget.setVisible(True)
