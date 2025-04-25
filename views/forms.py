"""Contain all forms related to form operation
like form creation, updating, deleting and etc.
"""

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
from PySide6.QtCore import Qt

from views import utils
from db.models import FormModel


class FormCreate:
    def __init__(self):
        ### UI
        self.ui = utils.load_ui(utils.FORM_DIR / "create.ui")
        self.field_index = 0

        ### Models
        self.model = FormModel()
        self.types = self.model.field_types()

        ### Events
        self.ui.add_button.clicked.connect(self.on_add)
        self.ui.remove_button.clicked.connect(self.on_remove)
        self.ui.save_button.clicked.connect(self.on_save)
        self.ui.checkall.stateChanged.connect(self.on_checkall)

        # First Field
        self.add_new_field()

    def on_checkall(self):
        for check in self.checks():
            check.setChecked(self.ui.checkall.isChecked())

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

        self.ui.body.layout().addWidget(frame)
        # must be here.
        field_name.setFocus()
        self.field_index += 1

    def rows(self):
        field_frames = self.row_frames()
        rows = []
        for frame in field_frames:
            name = frame.findChild(QLineEdit).text()
            types = frame.findChild(QComboBox).currentText()
            row = (name, types)
            rows.append(row)
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

    def is_empty(self):
        pass

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



    def on_save(self):
        if self.is_form_name_empty() or self.is_field_name_empty():
            return

        form_name = self.ui.form_name.text()
        self.model.save_form(form_name, self.rows())

        # form save
        # Access data and save it.

        # Message to say form stored successfuly.

        # After save
        # delete fields except first one and make form's name empty.

    def delete_field(self):
        pass


class FormUpdate:
    def __init__(self):
        pass


class FormDelete:
    def __init_(self):
        pass
