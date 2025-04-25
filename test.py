from PySide6.QtWidgets import (QApplication, QPushButton, 
                              QVBoxLayout, QWidget, QLineEdit, 
                              QScrollArea)
from PySide6.QtCore import Qt

app = QApplication([])

# Main window
window = QWidget()
layout = QVBoxLayout(window)

# Scrollable setup
scroll = QScrollArea()
scroll.setWidgetResizable(True)
container = QWidget()
container.setLayout(QVBoxLayout())
scroll.setWidget(container)

# Add button
add_btn = QPushButton("Add LineEdit")
layout.addWidget(add_btn)
layout.addWidget(scroll)

# Logic
def add_lineedit():
    container.layout().addWidget(QLineEdit())

add_btn.clicked.connect(add_lineedit)

window.show()
app.exec()
