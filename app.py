import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QComboBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt  

UI_DIR = Path(__file__).parent / "ui"


class FormBuilder:
    def __init__(self, ui):
        self.fields = []
        self.ui = ui

        # add field
        self.ui.add_field_button.clicked.connect(self.add_field)

    def add_field(self):
        field_name = QLineEdit()
        field_name.setPlaceholderText("نام فیلد")
        field_name.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        field_type = QComboBox()
        field_type.addItems(
            ["متن", "عدد", "مبلغ", "شماره کارت", "شماره شبا", "توضیحات"]
        )

        self.ui.fields_layout.addRow(field_name, field_type)

    def save_form(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load ui
        loader = QUiLoader()
        self.ui = loader.load(UI_DIR / "main.ui", self)
        self.setCentralWidget(self.ui)

        # Form builder tab
        self.form_builder = FormBuilder(self.ui)

        # Main window settings
        self.win_config()

    def win_config(self):
        self.resize(500, 400)
        self.setWindowTitle("فرم")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
