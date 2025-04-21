import json
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QComboBox, QFormLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt

UI_DIR = Path(__file__).parent / "ui"


class File:
    @classmethod
    def save_form(cls, data, filename):
        with open(filename, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
            print("forms.json saved!")
            return True

    @classmethod
    def load_forms(cls, filename, encoding='utf-8'):
        with open(filename, "r") as json_file:
            data = json.load(json_file)
        return data

class FormEdit:
    def __init__(self, ui):
        self.ui = ui
        self.forms = File.load_forms("forms.json")
        self.form_index = 0

        self.set_form_names()

        self.ui.update_form_button.clicked.connect(self.on_update_form)

    def set_form_names(self):
        form_names = [form.get("name") for form in self.forms]

        # set form name to the combo
        for form_name in form_names:
            self.ui.form_list_combo.addItem(form_name)

        self.ui.form_list_combo.currentIndexChanged.connect(self.on_select_form)

    def on_select_form(self, index):
        # Clear ef_fields_layout 
        for row_number in reversed(range(self.ui.ef_fields_layout.rowCount())):
            self.ui.ef_fields_layout.removeRow(row_number)
            

        form_name_edit = QLineEdit()
        form_name_edit.setText(self.forms[index]["name"])
        self.ui.ef_fields_layout.insertRow(0, "نام فرم", form_name_edit)

        fields = self.forms[index]["fields"]
        for rownum, field in enumerate(fields, 1):
            # fill the fields_layout
            field_name = QLineEdit()
            field_name.setText(field.get("field_name"))

            field_types = QComboBox()
            field_types.addItems(["متن", "عدد", "مبلغ", "شماره کارت", "شماره شبا", "توضیحات"])
            field_types.setCurrentText(field["field_type"])

            self.ui.ef_fields_layout.insertRow(rownum, field_name, field_types)

        # index of the form that will updated
        self.form_index = index
        # Enable button to update form
        self.ui.update_form_button.setEnabled(True)


    def on_update_form(self):
        form = {"name": "", "fields": []}
        # extract form name 
        form_name_edit= self.ui.ef_fields_layout.itemAt(0, QFormLayout.FieldRole).widget()
        form["name"] = form_name_edit.text()


        # we want skipe first row which is the form name
        # This code extract fields from the form layout
        for row_count in range(1, self.ui.ef_fields_layout.rowCount()):
            field_name = self.ui.ef_fields_layout.itemAt(row_count, QFormLayout.LabelRole).widget()
            field_type = self.ui.ef_fields_layout.itemAt(row_count, QFormLayout.FieldRole).widget()
            row = {"field_name": field_name.text(), "field_type": field_type.currentText()}
            form["fields"].append(row)
        # update forms
        self.forms[self.form_index] = form
        print(self.forms)
        # save in the file
        File.save_form(self.forms, "forms.json")



class FormBuilder:
    def __init__(self, ui):
        self.forms = File.load_forms("forms.json")
        self.ui = ui

        self.ui.field_name.setFocus()
        # buttons event
        self.ui.add_field_button.clicked.connect(self.add_field)
        self.ui.save_form_button.clicked.connect(self.save_form)

    def add_field(self):
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

        field_type = QComboBox()
        field_type.addItems(["متن", "عدد", "مبلغ", "شماره کارت", "شماره شبا", "توضیحات"])
        field_type.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.ui.fields_layout.addRow(field_name, field_type)
        field_name.setFocus()

    def remove_fields(self):
        pass

    def save_form(self):
        if not self.ui.form_name.text():
            self.ui.form_name.setStyleSheet("border: 2px solid red;")
            return

        form = {"name": "", "fields": []}
        form["name"] = self.ui.form_name.text().strip()
        for row_count in range(self.ui.fields_layout.rowCount()):
            field_name = self.ui.fields_layout.itemAt(row_count, QFormLayout.LabelRole).widget()
            field_type = self.ui.fields_layout.itemAt(row_count, QFormLayout.FieldRole).widget()
            row = {"field_name": field_name.text(), "field_type": field_type.currentText()}
            form["fields"].append(row)

        self.forms.append(form)
        File.save_form(self.forms, "forms.json")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load ui
        loader = QUiLoader()
        self.ui = loader.load(UI_DIR / "main.ui", self)
        self.setCentralWidget(self.ui)

        # Form builder tab
        self.form_builder = FormBuilder(self.ui)
        self.form_edit = FormEdit(self.ui)

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
