import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction 
from PySide6.QtUiTools import QUiLoader

### Global variables
UI_DIR = Path(__file__).parent.parent / "ui"



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()
        self.layout = QVBoxLayout()

        # Menubar
        self.menubar()
        self.main()
        self.statusbar()


    def init(self):
        self.setLayoutDirection(Qt.RightToLeft)
        self.setWindowTitle("Hesab System")
        self.resize(800, 600)

    def menubar(self):
        menubar = self.menuBar()
        menubar.setLayoutDirection(Qt.RightToLeft)

        ### Form menu
        form_menu = menubar.addMenu("فرم")
        form_create_action = QAction("ایجاد فرم", self)
        form_update_action = QAction("ویرایش فرم", self)
        form_delete_action = QAction("حذف فرم", self)
        form_menu.addActions([form_create_action, form_update_action, form_delete_action])

        ### Information menu
        info_menu = menubar.addMenu("اطلاعات")
        info_insert_action = QAction("افزودن اطلاعات", self)
        info_display_action = QAction("نمایش اطلاعات", self)
        info_menu.addActions([info_insert_action, info_display_action])
        
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
        form_create_action.triggered.connect(self.load_form_create_ui)


    def main(self):
        mainframe = QFrame()
        mainframe.setFrameShape(QFrame.StyledPanel)
        mainframe.setLineWidth(1)

        mainframe.setLayout(self.layout)
        self.setCentralWidget(mainframe)

    def statusbar(self):
        pass

    def load_ui(self, filename):
        loader = QUiLoader()
        ui = loader.load(UI_DIR / filename, self)
        return ui

    def load_form_create_ui(self):
        # Destroy form that is in main layout
        self.layout.takeAt(0)

        ui = self.load_ui("form_create.ui")
        self.layout.addWidget(ui)


    @classmethod
    def run(self):
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())




