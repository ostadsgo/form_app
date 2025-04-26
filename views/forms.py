"""Contain all forms related to form operation
like form creation, updating, deleting and etc.
"""

# Builtins
from pathlib import Path

# External
from PySide6.QtWidgets import (
    QFormLayout,
    QWidget,
    QLineEdit,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QToolButton,
    QCheckBox,
    QScrollArea,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QLocale
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIntValidator
# Project
from views import utils
from db import models


class UI:
    BASE_DIR = Path(__file__).parent.parent
    UI_DIR = BASE_DIR / "ui"
    FORM_DIR = UI_DIR / "form"

    @classmethod
    def load_ui(cls, filename):
        loader = QUiLoader()
        return loader.load(cls.FORM_DIR / filename)


# ==================
# -- Table --
# ==================
class TableCreateForm:
    def __init__(self):
        ### UI
        self.ui = UI.load_ui("create.ui")
        self.field_index = 0

        ### Models
        self.model = models.FormModel()
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

        # Add frame to layout
        self.ui.body.layout().addWidget(frame)
        # must be here.
        field_name.setFocus()
        self.field_index += 1

    def rows(self):
        rows = []
        for frame in self.row_frames():
            name = frame.findChild(QLineEdit).text()
            types = frame.findChild(QComboBox).currentText()
            rows.append((name, types))
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
        pass


class TableDeleteForm:
    def __init_(self):
        pass


# ==================
# -- Data --
# ==================
class DataInsertForm:
    def __init__(self):
        self.ui = UI.load_ui("insert.ui")
        self.model = models.DataModel()
        self.index = 0

        # get form names and set it to combobox
        names = self.model.get_form_names()
        self.ui.form_names.addItems(names)
        self.ui.form_names.setCurrentText("")
        self.ui.form_names.currentTextChanged.connect(self.on_form_name_select)

    def on_form_name_select(self):
        # delete form_frame if there is a form
        self.clear_form()
        self.build_form()

    def clear_form(self):
        while self.ui.form_layout.count():
            child = self.ui.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def build_form(self):
        selected_form_name = self.ui.form_names.currentText()
        form_id = self.model.get_form_id(selected_form_name)
        fields = self.model.get_form_fields(form_id)
        # a row in form
        for name, ftype in fields:
            # row frame
            frame = QFrame()
            layout = QHBoxLayout(frame)
            frame.setObjectName(f"frame_{self.index}")
            layout.setObjectName(f"layout_{self.index}")
            frame.setFrameShape(QFrame.NoFrame)

            # choice widget type
            self.name_type(name, layout)
            if ftype == "متن":
                self.input_type(layout)
            elif ftype == "عدد":
                self.number_type(layout)


            self.ui.form_frame.layout().addWidget(frame)
            self.index += 1
            

    def name_type(self, name, layout):
        label = QLabel(name)
        label.setObjectName(f"label_{self.index}")
        layout.addWidget(label)
        layout.setStretchFactor(label, 1)

    def input_type(self, layout):
        line_edit = QLineEdit()
        line_edit.setObjectName(f"line_edit_{self.index}")
        layout.addWidget(line_edit)
        layout.setStretchFactor(line_edit, 4)

    def number_type(self, layout):
        line_edit = QLineEdit()
        line_edit.setObjectName(f"number_edit_{self.index}")
        validator = QIntValidator()
        validator.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))  # Uses commas
        line_edit.setValidator(validator)
        layout.addWidget(line_edit)
        layout.setStretchFactor(line_edit, 4)

    def amount_type(self):
        pass

    def account_nubmer_type(self):
        pass

    def card_number_type(self):
        pass

    def shaba_number_type(self):
        pass

    def multichoice_type(self):
        pass

    def detail_type(self):
        pass




class DataViewForm:
    def __init__(self):
        pass


# ==================
# -- MultiChoice --
# ==================
class MultiChoiceCreateForm:
    def __init__(self):
        pass


class MultiChoiceUpdateForm:
    def __init__(self):
        pass


class MultiChoiceDeleteForm:
    def __init__(self):
        pass
