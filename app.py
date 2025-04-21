# QUESTIONS:
# is it must tab oriented ?

# MAYBE: 
# write some helper functions like is_empty
# border style used two times 

import json
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QComboBox, QFormLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt

UI_DIR = Path(__file__).parent / "ui"


class File:
    @classmethod
    def save_form(self, data, filename):
        with open(filename, "w") as json_file:
            json.dump(data, json_file)
            print("forms.json saved!")

    @classmethod
    def load_forms(self, filename):
        with open(filename, "r") as json_file:
            data = json.load(json_file)
        return data


class FormBuilder:
    def __init__(self, ui):
        self.rows = File.load_forms("forms.json")
        self.ui = ui
        # [1] TODO: before save form check fields to not be empty
        # TODO: Form name lineedit
        # TODO: Remove field
        # TODO:

        self.ui.field_name.setFocus()
        # buttons event
        self.ui.add_field_button.clicked.connect(self.add_field)
        self.ui.save_form_button.clicked.connect(self.save_form)

    def add_field(self):
        # TODO: Set focus to field name
        # check if last row not invalid
        last_row = self.ui.fields_layout.rowCount() - 1
        field_name = self.ui.fields_layout.itemAt(last_row, QFormLayout.LabelRole).widget()
        field_name.setStyleSheet("")

        ### Validation of last row
        if not field_name.text():
            # make last field_name red becuase it's empty
            field_name.setStyleSheet("border: 2px solid red;")
            return

        ### Make a row
        field_name = QLineEdit()
        field_name.setPlaceholderText("نام فیلد")
        field_name.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        field_name.setFocuse()

        field_type = QComboBox()
        field_type.addItems(["متن", "عدد", "مبلغ", "شماره کارت", "شماره شبا", "توضیحات"])
        field_type.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.ui.fields_layout.addRow(field_name, field_type)

    def remove_fields(self):
        pass

    def save_form(self):
        # TODO: check form name not be empty
        # TODO: check at last one row with field name and type exist in the form layout

        if not self.ui.form_name.text():
            self.ui.form_name.setStyleSheet("border: 2px solid red;")
            return

        form_name = self.ui.form_name.text()
        for row in range(self.ui.fields_layout.rowCount()):
            field_name = self.ui.fields_layout.itemAt(row, QFormLayout.LabelRole).widget()
            field_type = self.ui.fields_layout.itemAt(row, QFormLayout.FieldRole).widget()
            row = {"field_name": field_name.text(), "field_type": field_type.currentText()}
            self.rows.append(row)

        File.save_form(self.rows, "forms.json")


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
