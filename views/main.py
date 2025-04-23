from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
### Global variables
UI_DIR = Path(__file__).parent.parent / "ui"


class MainWindow(QMainWindow):
    def __init__(self):
        # super().__init__()
        #
        # # Load ui
        # loader = QUiLoader()
        # self.ui = loader.load(UI_DIR / "app2.ui", self)
        # print(UI_DIR / "app.ui")
        # self.setCentralWidget(self.ui)
        # # self.resize(600, 500)
        # #
        # # self.setWindowTitle("hello world!")
        # print(self.ui.pushButton)
        super().__init__()
        
        # Load the UI file
        loader = QUiLoader()
        file = QFile(UI_DIR / "app.ui")  # Your UI file path
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()
        
        # Set up the main window
        self.setCentralWidget(self.ui)
        self.setWindowTitle("My Application")

        self.ui.action.triggered.connect(self.on_create_form)


    def on_create_form(self):
        print('hello')

