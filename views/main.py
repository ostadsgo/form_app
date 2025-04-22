import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow 
from PySide6.QtUiTools import QUiLoader

### Global variables
UI_DIR = Path(__file__).parent.parent / "ui"
print(UI_DIR)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load ui
        loader = QUiLoader()
        self.ui = loader.load(UI_DIR / "app.ui", self)
        self.setCentralWidget(self.ui)

        # # Database object
        # self.db = Database("forms.db")
        # # Form builder tab
        # self.form_builder = FormBuilder(self.ui, self.db)
        # self.form_edit = FormEdit(self.ui)
        # self.form_insert_data = FormInsertData(self.ui)
        # self.form_type = FormType(self.db)

        self.resize(600, 500)


    def run():
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
