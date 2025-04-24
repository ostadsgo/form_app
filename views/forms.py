""" Contain all forms related to form operation
like form creation, updating, deleting and etc.
"""
from PySide6.QtWidgets import (QFormLayout, QWidget, QLineEdit, 
                               QComboBox, QFrame, QHBoxLayout,
                               QLabel, QToolButton)
from PySide6.QtCore import Qt

from views import utils
from db.models import FormModel

class FormCreate:
    def __init__(self):
        # Load ui / config
        self.ui = utils.load_ui(utils.FORM_DIR / "create.ui")
        self.form_data = []
        self.last_field_name = None

        # Database operation
        self.model = FormModel()
        self.types = self.model.field_types()

        # Add types to field_types combobox
        self.ui.field_types.addItems(self.types)

        # Events
        self.ui.delete_button.clicked.connect(self.on_delete_field)
        self.ui.add_field.clicked.connect(self.on_add_field)
        self.ui.save_form.clicked.connect(self.on_save)


    def config_field_layout(self, layout):
        """ Set `field_layout` property to `layout` """
        field_layout = self.ui.field_layout
        stretch = [field_layout.stretch(i) for i in range(field_layout.count())]
        print(stretch)
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
        frame.setObjectName("field_frame")
        layout.setObjectName("field_layout")

        # widgets
        delete_button = QToolButton() 
        field_name = QLineEdit()
        field_types = QComboBox()
        multichoice = QComboBox()

        # widgets config
        delete_button.setText("X")
        # tool_button.setIcon(icon)
        field_name.setPlaceholderText("مانند: نام مشتری")
        field_types.addItems(self.types)
        multichoice.setEnabled(False)
        delete_button.setObjectName("delete_button")
        field_name.setObjectName("field_name")
        field_types.setObjectName("field_types")
        multichoice.setObjectName("multi_choice")

        # Add widgets to layout
        layout.addWidget(delete_button)
        layout.addWidget(field_name)
        layout.addWidget(utils.vertical_line())
        layout.addWidget(field_types)
        layout.addWidget(utils.vertical_line())
        layout.addWidget(multichoice)

        # Add frame to fields_frame
        self.ui.fields_frame.layout().addWidget(frame)

        # Add config to layout to be look like field_layout designed in qt desinger
        self.config_field_layout(layout)

        # # set focus to new row's lineEdit
        field_name.setFocus()

        # Events
        delete_button.clicked.connect(self.on_delete_field)

    def field_values(self):
        field_frames = self.ui.fields_frame.findChildren(QFrame, "field_frame")
        self.form_data = []

        for frame in field_frames:
            field_value = {}
            field_name = frame.findChild(QLineEdit, "field_name")
            field_types = frame.findChild(QComboBox, "field_types")
            field_value["field_name"] = field_name.text()
            field_value["field_types"] = field_types.currentText()
            self.form_data.append(field_value)


    def is_field_name_empty(self):
        #TODO: Add message to status bar
        # Field name cannot be empty
        frames = self.ui.fields_frame.findChildren(QFrame, "field_frame")
        if frames:
            self.last_field_name = frames[-1].findChild(QLineEdit, "field_name")

        if self.last_field_name.text().strip():
            self.last_field_name.setStyleSheet("")
            return False

        self.last_field_name.setStyleSheet("border: 2px solid red;")
        self.last_field_name.setFocus()
        return True

    def on_delete_field(self):
        pass

    def on_add_field(self):
        if self.is_field_name_empty():
            return

        self.add_new_field()
        self.field_values()
        

    def on_save(self):
        self.ui.form_name.setStyleSheet("")
        if not self.ui.form_name.text():
            self.ui.form_name.setStyleSheet("border: 2px solid red;")
            #TODO: Add message to status bar
            # Form name cannot be empty
            return

        # Access data and save it.
        # Message to say form stored successfuly.


class FormUpdate:
    def __init__(self):
        pass


class FormDelete:
    def __init_(self):
        pass
