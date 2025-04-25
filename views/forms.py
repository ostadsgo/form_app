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
        self.data = []
        self.field_index = 0
        self.recent_frame = None
        self.ui.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.container.layout().setAlignment(Qt.AlignTop)

        ### Models
        self.model = FormModel()
        self.types = self.model.field_types()

        ### Events
        self.ui.add_button.clicked.connect(self.on_add_field)
        self.ui.save_button.clicked.connect(self.on_save)
        
        # First Field
        self.add_new_field()

        
    def config_field_layout(self, layout):
        """Set `field_layout` property to `layout`"""
        field_layout = self.ui.field_layout
        stretch = [field_layout.stretch(i) for i in range(field_layout.count())]
        spacing = field_layout.spacing()
        margins = field_layout.getContentsMargins()
        # apply stretch to layout
        for index, factor in enumerate(stretch):
            layout.setStretch(index, factor)

        layout.setSpacing(spacing)
        layout.setContentsMargins(*margins)

    def add_new_field(self):
        # containers
        frame = QFrame()
        layout = QHBoxLayout(frame)
        frame.setObjectName(f"field_frame_{self.field_index}")
        layout.setObjectName(f"field_layout_{self.field_index}")
        self.recent_frame = frame

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

        # Add frame to fields_frame
        self.ui.body.layout().addWidget(frame)

        # Add config to layout to be look like field_layout designed in qt desinger
        # self.config_field_layout(layout)

        field_name.setFocus()
        # stretch = [field_layout.stretch(i) for i in range(field_layout.count())]


        self.field_index += 1


    def find_frame(self):
        children = self.ui.fields_frame.findChildren(QFrame)
        for child in children:
            if child.objectName().startswidth("field_frame"):
                self.field_frames.append(child)

    def field_values(self):
        field_frames = self.ui.fields_frame.findChildren(QFrame, "field_frame")

        self.form_data = []

        for frame in field_frames:
            field_value = {}
            field_name = frame.findChild(QLineEdit, "field_name")
            field_types = frame.findChild(QComboBox, "field_types")
            field_value["name"] = field_name.text()
            field_value["type"] = field_types.currentText()
            self.form_data.append(field_value)

    def get_field(self):
        pass

    def get_fields(self):
        pass

    def get_field_frames(self):
        """ Get all field frame in fields_frame"""
        return self.ui.body.findChildren(QFrame, options=Qt.FindDirectChildrenOnly)

    def get_all_field_name(self):
        # extract all QLineEdits in a field(row) - column 1
        return [frame.findChild(QLineEdit) for frame in self.get_field_frames()]

    def get_field_values(self):
        pass

    def is_empty(self):
        """ check all QLineEidt to make sure none of the are empty."""

    def is_field_name_empty(self):
        """ Check all field name widgets to not be empty."""
        for field_name in self.get_all_field_name():
            field_name.setStyleSheet("")
            if not field_name.text().strip():
                field_name.setStyleSheet("border: 2px solid red;")
                field_name.setFocus()
                return True
        return False

    def is_form_name_empty(self):
        if self.ui.form_name.text():
            self.ui.form_name.setStyleSheet("")
            return False

        self.ui.form_name.setStyleSheet("border: 2px solid red;")
        return

    def on_delete_field(self):
        field_frame = self.delete_me.parent().parent()
        field_frame.layout().removeWidget(field_frame)
        field_frame.deleteLater()

    def on_add_field(self):
        if self.is_field_name_empty():
            return

        self.add_new_field()

    def on_save(self):
        if self.is_form_name_empty() or self.is_field_name_empty():
            return
        #
        # # set data to self.form_data
        # self.field_values()
        # form_name = self.ui.form_name.text()
        # self.model.save_form(form_name, self.form_data)

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
