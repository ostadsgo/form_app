""" Contain all forms related to form operation
like form creation, updating, deleting and etc.
"""
from PySide6.QtWidgets import (QFormLayout, QWidget, QLineEdit, 
                               QComboBox, QFrame, QHBoxLayout,
                               QLabel)
from PySide6.QtCore import Qt

from views import utils
from db.models import FormModel

class FormCreate:
    def __init__(self):
        # Load ui / config
        self.ui = utils.load_ui(utils.FORM_DIR / "create.ui")

        # Database operation
        self.model = FormModel()
        self.types = self.model.field_types()

        # Add types to field_types combobox
        self.ui.field_types.addItems(self.types)

        # Events
        self.ui.add_field.clicked.connect(self.on_add_field)
        self.ui.save_form.clicked.connect(self.on_save)

    def _config_field_layout(self, layout):
        field_layout = self.ui.field_layout
        stretch = [field_layout.stretch(i) for i in range(field_layout.count())]
        spacing = field_layout.spacing()
        margins = field_layout.getContentsMargins()
        # Should be after creating widgets
        for index, factor in enumerate(stretch):
            layout.setStretch(index, factor)

        layout.setSpacing(spacing)
        layout.setContentsMargins(*margins)

    def _add_new_field(self):
        # containers
        frame = QFrame()
        layout = QHBoxLayout(frame)

        # widgets
        field_name = QLineEdit()
        field_types = QComboBox()
        hidden_label = QLabel()

        # Add widgets to layout
        layout.addWidget(field_name)
        layout.addWidget(utils.vertical_line())
        layout.addWidget(field_types)
        layout.addWidget(utils.vertical_line())
        layout.addWidget(hidden_label)

        # widgets config
        field_name.setPlaceholderText("مانند: نام مشتری")
        field_name.setFocus()
        field_types.addItems(self.types)

        # Add frame to fields_frame
        self.ui.fields_frame.layout().addWidget(frame)

        # Add config to layout to be look like field_layout designed in qt desinger
        self._config_field_layout(layout)


    def on_add_field(self):
        self._add_new_field()

        

    def on_save(self):
        print("on save")






class FormUpdate:
    def __init__(self):
        pass


class FormDelete:
    def __init_(self):
        pass
