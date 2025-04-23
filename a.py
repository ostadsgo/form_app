from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

app = QApplication([])

loader = QUiLoader()
window = loader.load("ui/form_create.ui")  # Directly load from file path

window.show()
app.exec()
