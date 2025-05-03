# Builtins
import sys
import os
import sqlite3
from pathlib import Path


from PySide6.QtCore import Qt, QRegularExpression, QFile
from PySide6.QtGui import QAction, QRegularExpressionValidator
from PySide6.QtUiTools import QUiLoader

# External
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QTextEdit,
    QTableWidgetItem,
    QFileDialog,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
)


# External Libs
import pandas as pd



class Database:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        if self.connection:
            return  # already connected

        try:
            with sqlite3.connect(self.db_filename) as conn:
                self.connection = conn
                self.cursor = conn.cursor()
                print("Succesfuly connect to db.")
        except sqlite3.OperationalError as e:
            print("Failed to open database:", e)

    def execute(self, query, params=()):
        if not self.connection:
            print("No database connection established")
            return

        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error executing query: {e}\nQuery: {query}")

    def executemany(self, query, params=()):
        if not self.connection:
            print("No database connection established")
            return

        try:
            self.cursor.executemany(query, params)
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error executing query: {e}\nQuery: {query}")

    def fetch_all(self, query, params=()):
        if not self.connection:
            print("No database connection established")

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}\nQuery: {query}")

    def fetch_one(self, query, params=()):
        if not self.connection:
            print("No database connection established")

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}\nQuery: {query}")


class FormModel:
    def __init__(self):
        self.db = Database("forms.db")

    def field_types(self):
        sql = """ SELECT name FROM types; """
        types = self.db.fetch_all(sql)
        return [value for item in types for value in item]

    def save_form(self, name, rows):
        # Save table name - form name
        sql = """INSERT INTO forms(name) VALUES (?)"""
        tid = self.db.execute(sql, (name,))

        sql = """ INSERT INTO fields (name, type, option_id, form_id) VALUES (?, ?, ?, ?)"""
        rows = [(*row, tid) for row in rows]
        self.db.executemany(sql, rows)
        print(f"Table {name} with id {tid} stored with fields succussfully.")

    def get_form_names(self):
        sql = """ SELECT name FROM forms; """
        names = self.db.fetch_all(sql)
        return [name for row in names for name in row]

    def get_form_fields(self, fid):
        sql = """ SELECT * FROM fields WHERE form_id = (?); """
        fields = self.db.fetch_all(sql, (fid,))
        # Field name and field type
        return [(field[1], field[2]) for field in fields]

    def get_form_fields_with_id(self, fid):
        sql = """ SELECT * FROM fields WHERE form_id = (?); """
        fields = self.db.fetch_all(sql, (fid,))
        # Field name and field type
        return fields

    def get_forms(self):
        sql = """ SELECT * FROM forms; """
        fidname = self.db.fetch_all(sql)
        return fidname

    def update_form_name(self, fid, new_name):
        sql = """ UPDATE forms SET name = ? WHERE id = ?;"""
        self.db.execute(sql, (new_name, fid))
        print("form name updated successfuly.")
        return True

    def update_form_fields(self, fields):
        sql = """ UPDATE fields 
                  SET name = ?, type = ?
                  WHERE id = ?;"""
        self.db.executemany(sql, fields)
        print("form name updated successfuly.")
        return True

    def delete_form(self, fid):
        sql = """ DELETE FROM forms
                  WHERE id = ?;
                  """
        self.db.execute(sql, (fid,))
        print(f"Table with id {fid} deleted successfuly.")
        return True


class DataModel:
    def __init__(self):
        self.db = Database("forms.db")

    def get_form_names(self):
        sql = """ SELECT name FROM forms; """
        names = self.db.fetch_all(sql)
        return [name for row in names for name in row]

    def get_form_id(self, name):
        sql = """ SELECT id FROM forms WHERE name = (?); """
        fid = self.db.fetch_one(sql, (name,))
        return fid[0]

    def get_form_name(self, fid):
        sql = """ SELECT name FROM forms WHERE id = (?); """
        form_name = self.db.fetch_one(sql, (fid,))
        print(form_name, type(form_name))
        if form_name is not None:
            return form_name[0]
        return None

    def get_form_fields(self, fid):
        sql = """ SELECT * FROM fields WHERE form_id = (?); """
        fields = self.db.fetch_all(sql, (fid,))
        # Field name and field type
        return [(field[1], field[2]) for field in fields]

    def get_field_option_id(self, form_id):
        sql = """ SELECT option_id FROM fields WHERE form_id = (?) AND type = "چند گزینه" ; """
        options_ids = self.db.fetch_all(sql, (form_id,))
        return options_ids

    def get_options(self, option_id):
        sql = """SELECT name FROM options WHERE option_id = ?;"""
        options = self.db.fetch_all(sql, (option_id,))
        return options


class OptionModel:
    def __init__(self):
        self.db = Database("forms.db")

    def save_option(self, option_name):
        sql = """ INSERT INTO option (name) VALUES (?);"""
        option_id = self.db.execute(sql, (option_name,))
        return option_id

    def save_options(self, options):
        sql = """ INSERT INTO options (option_id, name) VALUES (?, ?);"""
        self.db.executemany(sql, options)
        return True

    def get_options(self):
        sql = """ SELECT * FROM option;"""
        options = self.db.fetch_all(sql)
        return options


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UI_DIR = BASE_DIR / "ui"
print(BASE_DIR)



def load_ui(filename):
    ui_file = QFile(UI_DIR / filename)
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    window = loader.load(ui_file)
    return window

# ==================
# -- Table --
# ==================
class TableCreateForm:
    def __init__(self):
        ### UI
        self.ui = load_ui("create.ui")
        self.field_index = 0
        self.row_widgets = []
        self.option_ids = []

        self.option_model = OptionModel()

        ### Models
        self.model = FormModel()
        self.types = self.model.field_types()

        ### Events
        self.ui.add_button.clicked.connect(self.on_add)
        self.ui.remove_button.clicked.connect(self.on_remove)
        self.ui.save_button.clicked.connect(self.on_save)
        self.ui.checkall.stateChanged.connect(self.on_checkall)

        # First row
        self.add_new_field()

    def add_new_field(self):
        # containers
        frame = QFrame()
        layout = QHBoxLayout(frame)
        frame.setObjectName(f"field_frame_{self.field_index}")
        layout.setObjectName(f"field_layout_{self.field_index}")

        # Widgets
        check = QCheckBox()
        field_name = QLineEdit()
        field_types = QComboBox()
        multichoice = QComboBox()

        field_name.setPlaceholderText("مانند: نام مشتری")
        field_types.addItems(self.types)
        multichoice.setEnabled(False)
        check.setObjectName(f"check_field_{self.field_index}")
        field_name.setObjectName(f"field_name_{self.field_index}")
        field_types.setObjectName(f"field_types_{self.field_index}")
        multichoice.setObjectName(f"multi_choice_{self.field_index}")

        # Add widgets to layout
        layout.addWidget(check)
        layout.addWidget(field_name)
        layout.addWidget(field_types)
        layout.addWidget(multichoice)
        layout.setStretchFactor(field_name, 1)
        layout.setStretchFactor(field_types, 1)
        layout.setStretchFactor(multichoice, 1)
        layout.addSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        self.row_widgets.append((field_name, field_types, multichoice))

        # for multi choice
        field_types.currentIndexChanged.connect(self.on_field_type)

        # Add frame to layout
        self.ui.body.layout().addWidget(frame)
        # must be here.
        field_name.setFocus()
        self.field_index += 1

    def on_field_type(self, index):
        field_type = self.types[index]
        all_option = self.option_model.get_options()
        option_names = [opt[1] for opt in all_option]
        self.option_ids = [opt[0] for opt in all_option]
        print(self.row_widgets)
        for row in self.row_widgets:
            row[2].clear()
            if row[1].currentText() == "چند گزینه":
                row[2].setEnabled(True)
                row[2].addItems(option_names)
            else:
                row[2].setEnabled(False)

    def rows(self):
        rows = []
        for widget in self.row_widgets:
            name = widget[0].text()
            types = widget[1].currentText()
            multichoice = widget[2]
            current_index = multichoice.currentIndex()
            if current_index == -1:
                rows.append((name, types, 0))
            else:
                rows.append((name, types, self.option_ids[current_index]))
            # else:
            #     rows.append((name, types))
        print(rows)
        return rows

    def row_frames(self):
        """Get all field frame in fields_frame"""
        return self.ui.body.findChildren(QFrame, options=Qt.FindDirectChildrenOnly)

    def extract_widget(self, widget):
        return [frame.findChild(widget) for frame in self.row_frames()]

    def names(self):
        return self.extract_widget(QLineEdit)

    def checks(self):
        return self.extract_widget(QCheckBox)

    def checkeds(self):
        return [check for check in self.checks() if check.isChecked()]

    def un_checkall(self):
        if self.ui.checkall.isChecked():
            self.ui.checkall.setChecked(False)

    def is_field_name_empty(self):
        """Check all field name widgets to not be empty."""
        for name in self.names():
            name.setStyleSheet("")
            if not name.text().strip():
                name.setStyleSheet("border: 2px solid red;")
                name.setFocus()
                return True
        return False

    def is_form_name_empty(self):
        if self.ui.form_name.text():
            self.ui.form_name.setStyleSheet("")
            return False

        self.ui.form_name.setStyleSheet("border: 2px solid red;")
        return True

    def clear_body(self):
        self.row_widgets = []
        for frame in self.row_frames():
            frame.deleteLater()

    def on_add(self):
        # use try / except for validation
        if self.is_field_name_empty():
            return

        self.add_new_field()

    def on_remove(self):
        for check in self.checkeds():
            check.parent().deleteLater()

        # if check all checked uncheck it
        self.un_checkall()

    def on_checkall(self):
        for check in self.checks():
            check.setChecked(self.ui.checkall.isChecked())

    def on_save(self):
        if self.is_form_name_empty() or self.is_field_name_empty():
            return

        form_name = self.ui.form_name.text()
        self.model.save_form(form_name, self.rows())
        self.clear_body()
        self.ui.form_name.clear()


class TableUpdateForm:
    def __init__(self):
        self.ui = load_ui("update.ui")
        self.model = FormModel()
        self.ui.form_names.addItems(self.model.get_form_names())
        self.ui.form_names.currentIndexChanged.connect(self.on_form_name_select)
        self.ui.update_button.clicked.connect(self.on_update)
        self.selected_form_id = 0
        self.selected_form_name = ""
        self.selected_form_fields = []
        self.form_frame = None
        self.widget_index = 0

    def clear_body(self):
        # if self.form_frame is not None:
        #     self.form_frame.deleteLater()

        for frame in self.ui.form_frame.findChildren(QFrame):
            frame.deleteLater()

        for frame in self.ui.body.findChildren(QFrame):
            frame.deleteLater()

    def make_update_form(self):
        self.clear_body()
        # Form name
        frame = QFrame()
        frame.setLayout(QHBoxLayout())
        label = QLabel("نام فرم")
        form_name = QLineEdit(self.selected_form_name)
        form_name.setObjectName(f"form_name")
        frame.layout().addWidget(label)
        frame.layout().addWidget(form_name)
        frame.setObjectName("form_frame_inner")
        self.ui.form_frame.layout().addWidget(frame)

        field_type_list = self.model.field_types()

        # Rows (each field name and type)
        # id: 0, name: 1, type: 2, form_id 3
        for row in self.selected_form_fields:
            row_frame = QFrame()
            row_frame.setLayout(QHBoxLayout())
            row_frame.setObjectName(f"row_frame_{self.widget_index}")
            # Widgets
            field_id = QLabel(str(row[0]))
            field_name = QLineEdit(row[1])
            field_types = QComboBox()
            field_id.setObjectName(str(field_id))
            field_name.setObjectName(f"field_name_{self.widget_index}")
            field_types.setObjectName(f"field_type_{self.widget_index}")

            field_types.addItems(field_type_list)
            field_types.setCurrentText(row[2])

            row_frame.layout().addWidget(field_id)
            row_frame.layout().addWidget(field_name)
            row_frame.layout().addWidget(field_types)
            row_frame.layout().setStretch(0, 0)
            row_frame.layout().setStretch(1, 1)
            row_frame.layout().setStretch(1, 1)
            row_frame.layout().setStretch(2, 1)

            self.ui.body.layout().addWidget(row_frame)
            self.widget_index += 1

    def on_form_name_select(self, index):
        forms = self.model.get_forms()
        # maybe some check required
        self.selected_form_id, self.selected_form_name = forms[index]
        self.selected_form_fields = self.model.get_form_fields_with_id(self.selected_form_id)
        self.make_update_form()
        self.ui.update_button.setEnabled(True)

    def on_update(self):
        ### Update Form Name
        form_name_widget = self.ui.form_frame.findChild(QLineEdit, "form_name")
        form_name = form_name_widget.text()
        self.model.update_form_name(self.selected_form_id, form_name)
        form_names = self.model.get_form_names()
        self.ui.form_names.clear()
        self.ui.form_names.addItems(form_names)
        self.ui.form_names.setCurrentText(form_name)

        ### Update Fields
        row_frames = self.ui.body.findChildren(QFrame, options=Qt.FindDirectChildrenOnly)
        fields = []
        for row_frame in row_frames:
            field_name = row_frame.findChild(QLineEdit).text()
            field_type = row_frame.findChild(QComboBox).currentText()
            field_id = row_frame.findChild(QLabel).text()
            fields.append((field_name, field_type, field_id))

        self.model.update_form_fields(fields)


class TableDeleteForm:
    def __init__(self):
        self.ui = load_ui("delete.ui")
        self.model = FormModel()
        self.form_data = self.model.get_forms()

        ### Table widget
        # Set columns
        self.ui.table.setColumnCount(2)
        self.ui.table.setRowCount(len(self.form_data))
        self.ui.table.setHorizontalHeaderLabels(["آی دی", "نام فرم"])
        self.populate_table()

        self.ui.delete_button.clicked.connect(self.on_delete)

    def populate_table(self):
        self.ui.table.setCurrentCell(0, 0)

        for row_index, form_row in enumerate(self.form_data):
            form_id = form_row[0]
            form_name = form_row[1]
            self.ui.table.setItem(row_index, 0, QTableWidgetItem(str(form_id)))
            self.ui.table.setItem(row_index, 1, QTableWidgetItem(form_name))

    def clear_all_rows(self):
        self.ui.table

    def get_selected_row(self):
        selected_row_index = self.ui.table.currentRow()
        selected_row = [
            self.ui.table.item(selected_row_index, col).text()
            for col in range(self.ui.table.columnCount())
        ]
        return selected_row

    def delete_selected_row(self):
        selected_row_index = self.ui.table.currentRow()
        self.ui.table.removeRow(selected_row_index)

    def on_delete(self):
        form_id, form_name = self.get_selected_row()
        # delete from table
        self.delete_selected_row()
        # delete operation on db
        self.model.delete_form(form_id)


# ==================
# -- Data --
# ==================
class DataInsertForm:
    DATA_DIR = BASE_DIR / "data"

    def __init__(self):
        self.ui = load_ui("insert.ui")
        self.model = DataModel()
        self.index = 0
        self.header = []
        self.rows = []
        self.data = []
        self.mc_index = 0

        # get form names and set it to combobox
        names = self.model.get_form_names()
        self.ui.form_names.addItems(names)
        self.ui.form_names.setCurrentText("")
        self.ui.form_names.currentTextChanged.connect(self.on_form_name_select)

        # on save
        self.ui.save_button.clicked.connect(self.on_save)

    def clear_form_content(self):
        for widgets in self.rows:
            for widget in widgets:
                if isinstance(widget, QLineEdit):
                    widget.clear()
                elif isinstance(widget, QLineEdit):
                    widget.clear()
                else:
                    print(f"Uknow widget to clear content of it {widget}")

    def row_frames(self):
        """Get all field frame in fields_frame"""
        return self.ui.body.findChildren(QFrame, options=Qt.FindDirectChildrenOnly)

    def is_empty(self):
        """Check all field name widgets to not be empty."""

        flag = False
        for frame in self.row_frames():
            for child in frame.findChildren(QWidget):
                child.setStyleSheet("")

        for frame in self.row_frames():
            for child in frame.findChildren(QWidget):
                if isinstance(child, QLineEdit):
                    if not child.text().strip():
                        child.setStyleSheet("border: 2px solid red;")
                        flag = True
        return flag

    def get_header(self):
        return [label.text() for label in self.header]

    def get_row(self):
        """list contain data of a form.
        each field store as element of list
        ex: ["John", "1234-4445-3333-1231", "1234555555"]
        """
        data = []

        for widgets in self.rows:
            row = []
            for widget in widgets:
                if isinstance(widget, QLineEdit):
                    row.append(widget.text())
                elif isinstance(widget, QComboBox):
                    row.append(widget.currentText())
                elif isinstance(widget, QTextEdit):
                    row.append(widget.toPlainText())
                else:
                    print(f"Can't get the wiget data. {widget}")
            data.append(row)

        # join row that have more that one widget
        data = ["-".join(row) for row in data]
        return data

    def on_save(self):
        header = self.get_header()
        row = self.get_row()
        if self.is_empty():
            return

        selected_form_name = self.ui.form_names.currentText()
        fid = self.model.get_form_id(selected_form_name)
        csv_file = f"{fid}.csv"

        if self.is_csv_exist(csv_file):
            self.append_csv(csv_file, row)
        else:
            self.create_csv(csv_file, header)
            self.append_csv(csv_file, row)

        # After save: delete inserted data to able to add new data.
        self.clear_form_content()
        print(f"{csv_file} Saved succesfully.")

    def is_csv_exist(self, filename):
        print(filename in os.listdir(self.DATA_DIR))
        return filename in os.listdir(self.DATA_DIR)

    def create_csv(self, filename, header):
        pd.DataFrame(columns=header).to_csv(self.DATA_DIR / filename, index=False)

    def append_csv(self, filename, row):
        df = pd.DataFrame([row])
        df.to_csv(self.DATA_DIR / filename, mode="a", index=False, header=False)
        print(f"{self.DATA_DIR}/{filename} saved.")

    def on_form_name_select(self):
        # delete form_frame if there is a form
        self.clear_form()
        selected_form_name = self.ui.form_names.currentText()
        form_id = self.model.get_form_id(selected_form_name)
        fields = self.model.get_form_fields(form_id)
        self.build_form(fields, self.ui.body)

    def clear_form(self):
        while self.ui.form_layout.count():
            child = self.ui.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def continer(self):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        frame.setObjectName(f"frame_{self.index}")
        layout.setObjectName(f"layout_{self.index}")
        frame.setFrameShape(QFrame.NoFrame)
        return frame, layout

    def build_form(self, fields, base):
        # base is the place frame will shown
        self.header = []
        self.rows = []
        self.widgets = []  # list widgets that created in the form
        # Types
        field_type_handlers = {
            "متن": self.input_type,  # Done
            "عدد": self.number_type,  # Done
            "مبلغ": self.amount_type,  # Done
            "شماره حساب": self.account_nubmer_type,
            "شماره کارت": self.card_number_type,
            "شماره شبا": self.shaba_number_type,
            "توضیحات": self.detail_type,
            "تاریخ شمسی": self.shamsi_date_type,
            "شماره تماس": self.phone_type,
            "کد ملی": self.code_meli_type,
            "چند گزینه": self.multichoice_type,
        }

        for field_index, field in enumerate(fields):
            name = field[0]
            ftype = field[1]
            self.field_name_label = name
            frame, layout = self.continer()
            self.name_type(name, layout)

            if handler := field_type_handlers.get(ftype):
                handler(layout)
            else:
                print(f"Field type not recognized: '{ftype}'. No widget created.")

            base.layout().addWidget(frame)
            self.index += 1

    def name_type(self, name, layout):
        label = QLabel(name)
        label.setObjectName(f"label_{self.index}")
        layout.addWidget(label)
        layout.setStretchFactor(label, 1)
        self.header.append(label)

    def input_type(self, layout):
        """abc123"""
        e = QLineEdit()
        e.setObjectName(f"line_edit_{self.index}")
        layout.addWidget(e)
        layout.setStretchFactor(e, 3)
        self.rows.append([e])

    def number_type(self, layout):
        """12341212"""
        e = QLineEdit()
        e.setObjectName(f"number_edit_{self.index}")
        e.setValidator(self.number_validator())
        layout.addWidget(e)
        layout.setStretchFactor(e, 4)
        self.rows.append([e])

    def amount_type(self, layout):
        """123,000,000"""
        # TODO: it has bug not sperate properly.
        e = QLineEdit()
        e.setObjectName(f"amount_edit_{self.index}")
        e.setValidator(self.number_validator())
        e.textEdited.connect(lambda: self.format_amount(e))
        layout.addWidget(e)
        layout.setStretchFactor(e, 4)
        self.rows.append([e])

    def account_nubmer_type(self, layout):
        # jump to next lineedit after fill 4 numbers
        # TODO: remeber order of line edits when grabing data
        """1234-1234-1234-1234"""
        edits = []
        e1 = QLineEdit()
        e2 = QLineEdit()
        e3 = QLineEdit()
        e4 = QLineEdit()
        edits.extend([e4, e3, e2, e1])
        for e in edits:
            e.setObjectName(f"account_number_{self.index}")
            e.setMaxLength(4)  # 16 digits + 3 dashes
            e.setValidator(self.number_validator())
            self.index += 1
            layout.addWidget(e)
            layout.setStretchFactor(e, 3)
        self.rows.append(edits[::-1])

    def card_number_type(self, layout):
        """1234-1234-1234-1234"""
        edits = []
        e1 = QLineEdit()
        e2 = QLineEdit()
        e3 = QLineEdit()
        e4 = QLineEdit()
        edits.extend([e4, e3, e2, e1])
        for e in edits:
            e.setObjectName(f"card_number_{self.index}")
            e.setMaxLength(4)  # 16 digits + 3 dashes
            e.setValidator(self.number_validator())
            self.index += 1
            layout.addWidget(e)
            layout.setStretchFactor(e, 3)
        self.rows.append(edits[::-1])

    def shaba_number_type(self, layout):
        """IRXX1234567890123456789012"""
        edits = []
        # Widgets
        e1 = QLineEdit()
        e2 = QLineEdit()
        e3 = QLineEdit()
        e4 = QLineEdit()
        e5 = QLineEdit()
        e6 = QLineEdit()
        e7 = QLineEdit()
        e8 = QLineEdit()
        e1.setText("IR")
        e1.setEnabled(False)
        edits.extend([e8, e7, e6, e5, e4, e3, e2, e1])
        for e in edits:
            e.setObjectName(f"shaba_number_{self.index}")
            e.setMaxLength(4)
            layout.addWidget(e)
            self.index += 1
        # Validation
        e1.setValidator(self.number_validator())
        e2.setValidator(self.number_validator())
        e3.setValidator(self.number_validator())
        e4.setValidator(self.number_validator())
        e5.setValidator(self.number_validator())
        e6.setValidator(self.number_validator())
        e7.setValidator(self.number_validator())

        layout.setStretchFactor(e1, 1)
        layout.setStretchFactor(e2, 6)
        layout.setStretchFactor(e3, 6)
        layout.setStretchFactor(e4, 6)
        layout.setStretchFactor(e5, 6)
        layout.setStretchFactor(e6, 6)
        layout.setStretchFactor(e7, 6)
        layout.setStretchFactor(e8, 1)
        # we must do this.
        self.rows.append(edits[::-1])

    def shamsi_date_type(self, layout):
        """Year - Month - Day"""
        y = QComboBox()
        m = QComboBox()
        d = QComboBox()
        y.setObjectName(f"shamsi_year_{self.index}")
        m.setObjectName(f"shamsi_month{self.index}")
        d.setObjectName(f"shamsi_day{self.index}")
        months_shamsi = [
            "فروردین",
            "اردیبهشت",
            "خرداد",
            "تیر",
            "مرداد",
            "شهریور",
            "مهر",
            "آبان",
            "آذر",
            "دی",
            "بهمن",
            "اسفند",
        ]
        y.addItems([str(i) for i in range(1390, 1410)])
        y.setCurrentText(str(1404))
        m.addItems(months_shamsi)
        d.addItems([str(i) for i in range(1, 32)])

        layout.addWidget(d)
        layout.addWidget(m)
        layout.addWidget(y)
        self.rows.append([y, m, d])

    def detail_type(self, layout):
        """Text widget ."""
        text = QTextEdit()
        text.setObjectName(f"text_{self.index}")
        layout.addWidget(text)
        self.rows.append([text])

    def multichoice_type(self, layout):
        combo = QComboBox()
        combo.setObjectName(f"multi_choice_{self.index}")
        layout.addWidget(combo)

        # db quries
        # remeber you cannot use option_ids.pop(0) cuz option_ids populated
        #   every time a multi choice field created.
        selected_form_name = self.ui.form_names.currentText()
        form_id = self.model.get_form_id(selected_form_name)
        option_ids = self.model.get_field_option_id(form_id)
        option_ids = [oid[0] for oid in option_ids]
        options = self.model.get_options(option_ids[self.mc_index])
        print(options)
        #
        combo.addItems([item[0] for item in options])
        self.rows.append([combo])
        self.mc_index += 1

    def phone_type(self, layout):
        e = QLineEdit()
        e.setObjectName(f"phone_number_{self.index}")
        e.setMaxLength(11)
        e.setValidator(self.number_validator())
        layout.addWidget(e)
        self.rows.append([e])

    def code_meli_type(self, layout):
        e = QLineEdit()
        e.setObjectName(f"code_meli_{self.index}")
        e.setMaxLength(10)
        e.setValidator(self.number_validator())
        layout.addWidget(e)
        self.rows.append([e])

    def number_validator(self):
        validator = QRegularExpressionValidator(QRegularExpression("[۰-۹]*"))
        return validator

    def format_amount(self, line_edit):
        text = line_edit.text()
        text = text.replace(",", "")
        cursor_pos = line_edit.cursorPosition()
        formatted = ",".join([text[i : i + 3] for i in range(0, len(text), 3)])
        line_edit.setText(formatted)
        line_edit.setCursorPosition(cursor_pos + formatted.count(","))


# view/update/delete
class DataManageUI:
    def __init__(self):
        self.ui = load_ui("view.ui")
        # load form names
        files = os.listdir(DATA_DIR)
        # extract form ids
        form_ids = [int(file.removesuffix(".csv")) for file in files if file.endswith(".csv")]
        # get form name
        self.model = DataModel()

        # Extract forms that has csv file aka data.
        form_names = []
        for form_id in form_ids:
            form_name = self.model.get_form_name(form_id)
            if form_name is not None:
                form_names.append(form_name)

        self.ui.form_names.addItems(form_names)
        self.ui.form_names.currentTextChanged.connect(self.on_form_select)
        self.ui.save_button.clicked.connect(self.on_save_table)
        self.ui.delete_row.clicked.connect(self.on_delete)
        self.ui.update_row.clicked.connect(self.on_update)
        self.header = []
        self.rows = []
        self.csv_file = ""

    def on_form_select(self, form_name):
        form_id = self.model.get_form_id(form_name)
        self.csv_file = DATA_DIR / f"{form_id}.csv"
        self.df = pd.read_csv(self.csv_file)
        self.populate_to_table(self.df)
        self.ui.save_button.setEnabled(True)

    def populate_to_table(self, df):
        table = self.ui.table
        row_count = df.shape[0]
        column_count = df.shape[1]
        # table widget config
        table.setRowCount(row_count)
        table.setColumnCount(column_count)
        table.setHorizontalHeaderLabels(df.columns.tolist())
        self.header = df.columns.tolist()
        # Populate the table with data
        for row in range(row_count):
            for col in range(column_count):
                item = QTableWidgetItem(str(df.iat[row, col]))
                table.setItem(row, col, item)

        # NOTE: reverse data before save make it LTR; The table is RTL
        self.rows = [row[::-1] for row in df.values.tolist()]

    def on_save_table(self):
        if not self.rows:
            print("There is no records to save!!!")
            self.ui.save_button.setEnabled(False)
            return

        # There is Data: Save data
        csv_filename, _ = QFileDialog.getSaveFileName(
            None, "Save File", "file.csv", "CSV Files (*.csv)"
        )

        print("filename: ", csv_filename)
        if csv_filename:
            # check if user add csv extention to filename
            if not csv_filename.endswith(".csv"):
                csv_filename += ".csv"

            # save file which now has a name and csv extention
            df = pd.DataFrame(self.rows, columns=self.header[::-1])
            df.to_csv(csv_filename, index=False)
            print(f"{csv_filename} saved succesfully.")

    def save_table(self):
        self.df.to_csv(self.csv_file, index=False)
        print("Re-Save table.")

    def refresh_table(self):
        # delete everything in table
        self.ui.table.clear()
        self.populate_to_table(self.df)
        print("refresh table.")

    def on_delete(self):
        selected_row = self.ui.table.currentRow()
        if selected_row >= 0:  # -1 if no selection
            self.ui.table.removeRow(selected_row)
        self.df = self.df.drop(self.df.index[selected_row]).reset_index(drop=True)
        self.save_table()
        self.refresh_table()

    def get_column_names(self):
        column_names = [
            self.ui.table.horizontalHeaderItem(col).text()
            for col in range(self.ui.table.columnCount())
        ]
        return column_names

    def on_update(self):
        selected_row = self.ui.table.currentRow()
        # populate form with the selected row data
        form = DataInsertForm()
        fields = []
        # detect fields type. and make pair
        if selected_row >= 0:  # -1 if no selection
            header = self.get_column_names()
            # first row to detect fields type.
            row = [
                self.ui.table.item(selected_row, col).text()
                for col in range(self.ui.table.columnCount())
            ]
            data_row = []
            for column, cell in zip(header, row):
                minus_num = cell.count("-")
                if minus_num == 2:  # date
                    field = (column, "تاریخ شمسی")
                elif minus_num == 4:
                    field = (column, "شماره کارت")
                elif minus_num == 8:
                    field = (column, "شماره شبا")
                else:
                    field = (column, "متن")
                fields.append(field)
                data_row.append(cell.split("-"))

            # build form
            self.win = QMainWindow()
            self.win.setLayoutDirection(Qt.RightToLeft)
            frame = QFrame()
            layout = QVBoxLayout()
            frame.setLayout(layout)
            form.build_form(fields, frame)
            # Add button at the bottom
            button = QPushButton("ذخیره")
            layout.addWidget(button)
            layout.addStretch()
            self.win.setCentralWidget(frame)
            self.win.show()
            # populate selected row data over form widgets
            for widgets, values in zip(form.rows, data_row):
                for widget, value in zip(widgets, values):
                    if isinstance(widget, QLineEdit):
                        widget.setText(value)
                    elif isinstance(widget, QComboBox):
                        widget.setCurrentText(value)
                    else:
                        print(f"{widget} uknow to set value to it.")
            button.clicked.connect(lambda: self.on_update_row(form.rows, selected_row))

    def update_selected_row(self, selected_row, values):
        for col, value in enumerate(values):
            self.ui.table.setItem(selected_row, col, QTableWidgetItem(str(value)))

    def on_update_row(self, rows, selected_row):
        values = []
        for widgets in rows:
            value = []
            for widget in widgets:
                if isinstance(widget, QLineEdit):
                    value.append(widget.text())
                elif isinstance(widget, QComboBox):
                    value.append(widget.currentText())
                else:
                    print(f"Cann't get of the value {widget}")
            values.append(value)

        values = ["-".join(v) for v in values]
        self.update_selected_row(selected_row, values)
        # close and delete win after doing update
        self.win.close()
        self.win.deleteLater()
        # update dataframe
        self.df.iloc[selected_row] = values
        # update csv file and refresh tableo
        self.save_table()
        self.refresh_table()


# -- MultiChoice --
# ==================
class MultiChoiceCreateForm:
    def __init__(self):
        self.ui = load_ui("multichoice_create.ui")
        self.model = OptionModel()
        self.option_line_edits = []

        self.ui.mc_add.clicked.connect(self.on_mc_add)
        self.ui.mc_save.clicked.connect(self.on_mc_save)
        self.index = 0
        self.create_multichoice()

    def create_multichoice(self):
        # Frame
        frame = QFrame()
        frame.setLayout(QHBoxLayout())
        frame.setObjectName(f"mc_row_frame_{self.index}")

        # Widgets of the frame
        check = QCheckBox()
        name = QLineEdit()
        self.option_line_edits.append(name)
        check.setObjectName(f"check_{self.index}")
        name.setObjectName(f"name_{self.index}")
        name.setPlaceholderText("مانند: فورد")
        frame.layout().addWidget(check)
        frame.layout().addWidget(name)

        self.ui.mc_frame.layout().addWidget(frame)
        self.index += 1

    def on_mc_add(self):
        if self.is_input_empty():
            return

        self.create_multichoice()

    def is_input_empty(self):
        """Check all field name widgets to not be empty."""
        # Check multi choice name
        self.ui.mc_name.setStyleSheet("")
        if not self.ui.mc_name.text():
            self.ui.mc_name.setStyleSheet("border: 2px solid red;")

        # all options of the multi choice
        for name in self.option_line_edits:
            name.setStyleSheet("")
            if not name.text().strip():
                name.setStyleSheet("border: 2px solid red;")
                return True
        return False

    def on_mc_save(self):
        # todo:  Check no field been empty
        if self.is_input_empty():
            return

        # save name of multi choice
        option_name = self.ui.mc_name.text()
        option_id = self.model.save_option(option_name)
        print(f"table {option_id} saved successfully.")
        names = []
        if option_id:
            for le in self.option_line_edits:
                names.append((option_id, le.text()))

        self.model.save_options(names)
        print(f"options saved. {names}")


class MultiChoiceUpdateForm:
    def __init__(self):
        pass


class MultiChoiceDeleteForm:
    def __init__(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()
        self.layout = QVBoxLayout()
        self.frame = None

        # Menubar
        self.menubar()
        self.main()
        self.statusbar()

        # *Temperory* --> Test
        self.load_table_create_form()
        # self.load_data_insert_form()
        # self.load_data_view()
        # self.load_table_update_form()
        # self.load_table_delete_form()
        # self.load_mc_create_form()

    def init(self):
        self.setLayoutDirection(Qt.RightToLeft)
        self.setWindowTitle("Hesab System")
        self.resize(800, 600)

    def menubar(self):
        menubar = self.menuBar()
        menubar.setLayoutDirection(Qt.RightToLeft)

        ### form menu
        table_from_menu = menubar.addMenu("فرم")
        table_create_form_action = QAction("ایجاد فرم", self)
        table_update_form_action = QAction("ویرایش فرم", self)
        table_delete_form_action = QAction("حذف فرم", self)
        table_from_menu.addActions(
            [table_create_form_action, table_update_form_action, table_delete_form_action]
        )

        ### Data menu
        data_form_menu = menubar.addMenu("داده")
        data_insert_from_action = QAction("افزودن داده", self)
        data_manage_action = QAction("مدیریت داده", self)
        data_form_menu.addActions([data_insert_from_action, data_manage_action])

        ### Multichoice
        mc_menu = menubar.addMenu("چند گزینه")
        mc_create_form_action = QAction("ایجاد چند گزینه", self)
        mc_update_form_action = QAction("بروزرسانی چند گزینه", self)
        mc_menu.addActions([mc_create_form_action, mc_update_form_action])

        ### Report Menu
        report_menu = menubar.addMenu("گزارشات")
        report_yearly_action = QAction("گزارش ماهانه", self)
        report_menu.addAction(report_yearly_action)

        ### Help Menu
        help_menu = menubar.addMenu("راهنمایی")
        help_action = QAction("مستندات برنامه", self)
        help_contact_action = QAction("تماس با ما", self)
        help_about_action = QAction("درباره برنامه", self)
        help_menu.addActions([help_action, help_contact_action, help_about_action])

        ### EVENTS
        # Table Form
        table_create_form_action.triggered.connect(self.load_table_create_form)
        table_update_form_action.triggered.connect(self.load_table_update_form)
        table_delete_form_action.triggered.connect(self.load_table_delete_form)
        # Data
        data_insert_from_action.triggered.connect(self.load_data_insert_form)
        data_manage_action.triggered.connect(self.load_data_manage)
        # Multichoice
        mc_create_form_action.triggered.connect(self.load_mc_create_form)

    def main(self):
        mainframe = QFrame()
        mainframe.setFrameShape(QFrame.StyledPanel)
        mainframe.setLineWidth(1)
        mainframe.setLayout(self.layout)
        self.setCentralWidget(mainframe)

    def statusbar(self):
        pass

    def clear_mainframe(self, index=0):
        item = self.layout.takeAt(index)
        if item:
            item.widget().deleteLater()

    def load_table_create_form(self):
        self.clear_mainframe()
        self.frame = TableCreateForm()
        self.layout.addWidget(self.frame.ui)

    def load_data_insert_form(self):
        self.clear_mainframe()
        self.frame = DataInsertForm()
        self.layout.addWidget(self.frame.ui)

    def load_data_manage(self):
        self.clear_mainframe()
        self.frame = DataManageUI()
        self.layout.addWidget(self.frame.ui)

    def load_table_update_form(self):
        self.clear_mainframe()
        self.frame = TableUpdateForm()
        self.layout.addWidget(self.frame.ui)
        print("Table update")

    def load_table_delete_form(self):
        self.clear_mainframe()
        self.frame = TableDeleteForm()
        self.layout.addWidget(self.frame.ui)
        print("Table delete")

    # Multichoice
    def load_mc_create_form(self):
        self.clear_mainframe()
        self.frame = MultiChoiceCreateForm()
        self.layout.addWidget(self.frame.ui)
        print("Multichoice create")

    @classmethod
    def run(self):
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    MainWindow.run()
