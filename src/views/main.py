import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from . import utils, forms


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()
        self.layout = QVBoxLayout()
        self.frame = None

        # Menubar
        self.menubar()
        self.main()
        self.statusbar()

        # *Temperory* --> Test
        # self.load_data_insert_form()
        # self.load_data_view()
        # self.load_table_update_form()
        self.load_table_delete_form()


    def init(self):
        self.setLayoutDirection(Qt.RightToLeft)
        self.setWindowTitle("Hesab System")
        self.resize(800, 600)

    def menubar(self):
        menubar = self.menuBar()
        menubar.setLayoutDirection(Qt.RightToLeft)

        ### frame menu
        table_from_menu = menubar.addMenu("فرم")
        table_create_form_action = QAction("ایجاد فرم", self)
        table_update_form_action = QAction("ویرایش فرم", self)
        table_delete_form_action = QAction("حذف فرم", self)
        table_from_menu.addActions(
            [table_create_form_action, table_update_form_action, table_delete_form_action]
        )

        ### Information menu
        data_form_menu = menubar.addMenu("داده")
        data_insert_from_action = QAction("افزودن داده", self)
        data_view_action = QAction("نمایش داده", self)
        data_manage_action = QAction("مدیریت داده", self)
        data_form_menu.addActions([data_insert_from_action, data_view_action, data_manage_action])

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
        # Table Form
        table_create_form_action.triggered.connect(self.load_table_create_form)
        table_update_form_action.triggered.connect(self.load_table_update_form)
        table_delete_form_action.triggered.connect(self.load_table_delete_form)
        # Data
        data_insert_from_action.triggered.connect(self.load_data_insert_form)
        data_view_action.triggered.connect(self.load_data_view)
        # Multichoice

    def main(self):
        mainframe = QFrame()
        mainframe.setFrameShape(QFrame.StyledPanel)
        mainframe.setLineWidth(1)
        mainframe.setLayout(self.layout)
        self.setCentralWidget(mainframe)

    def statusbar(self):
        pass

    def clear_mainframe(self, index=0):
        item = self.layout.takeAt(index)
        if item:
            item.widget().deleteLater()

    def load_table_create_form(self):
        self.clear_mainframe()
        self.frame = forms.TableCreateForm()
        self.layout.addWidget(self.frame.ui)

    def load_data_insert_form(self):
        self.clear_mainframe()
        self.frame = forms.DataInsertForm()
        self.layout.addWidget(self.frame.ui)

    def load_data_view(self):
        self.clear_mainframe()
        self.frame = forms.DataManageUI()
        self.layout.addWidget(self.frame.ui)

    def load_table_update_form(self):
        self.clear_mainframe()
        self.frame = forms.TableUpdateForm()
        self.layout.addWidget(self.frame.ui)
        print("Table update")

    def load_table_delete_form(self):
        self.clear_mainframe()
        self.frame = forms.TableDeleteForm()
        self.layout.addWidget(self.frame.ui)
        print("Table delete")




    @classmethod
    def run(self):
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
