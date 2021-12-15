from pkg_resources import get_distribution
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QStackedWidget, QDesktopWidget
# from PyQt5.QtWidgets import QMenuBar, QMenu
from ..pages.home_page import BadgerHomePage
from ..pages.routine_page import BadgerRoutinePage
from ..pages.run_page import BadgerRunPage


class BadgerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        version = get_distribution('badger-opt').version
        self.setWindowTitle(f'Badger v{version}')
        self.resize(960, 720)
        self.center()

        # Add menu bar
        # menu_bar = self.menuBar()
        # edit_menu = menu_bar.addMenu('Edit')
        # edit_menu.addAction('New')

        # Add pages
        self.home_page = BadgerHomePage(self.show_routine_page, self.show_run_page)
        self.routine_page = BadgerRoutinePage(self.show_home_page)
        self.run_page = BadgerRunPage(self.show_routine_page, self.show_home_page)

        self.stacks = stacks = QStackedWidget()
        stacks.addWidget(self.home_page)
        stacks.addWidget(self.routine_page)
        stacks.addWidget(self.run_page)

        stacks.setCurrentIndex(0)

        self.setCentralWidget(self.stacks)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def config_logic(self):
        pass

    def show_routine_page(self, routine=None):
        try:
            self.routine_page.refresh_ui(routine)
        except Exception as e:
            return QMessageBox.critical(self, 'Error!', str(e))

        self.stacks.setCurrentIndex(1)

    def show_home_page(self):
        self.routine_page.refresh_ui(None)  # clean up to prevent bugs
        self.home_page.refresh_ui()
        self.home_page.reconfig_logic()
        self.stacks.setCurrentIndex(0)

    def show_run_page(self):
        try:
            self.run_page.refresh_ui()
            self.run_page.reconfig_logic()
        except Exception as e:
            return QMessageBox.critical(self, 'Error!', str(e))

        self.stacks.setCurrentIndex(2)
