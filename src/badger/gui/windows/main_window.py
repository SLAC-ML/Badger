from pkg_resources import get_distribution
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget
from ..pages.home_page import BadgerHomePage
from ..pages.routine_page import BadgerRoutinePage


class BadgerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        version = get_distribution('badger-opt').version
        self.setWindowTitle(f'Badger v{version}')
        # self.setWindowIcon(QIcon('badger.png'))
        self.resize(864, 648)
        self.center()

        # Add pages
        self.home_page = BadgerHomePage(self.show_routine_page)
        self.routine_page = BadgerRoutinePage(self.show_home_page)

        self.stacks = stacks = QStackedWidget()
        stacks.addWidget(self.home_page)
        stacks.addWidget(self.routine_page)

        stacks.setCurrentIndex(0)

        self.setCentralWidget(self.stacks)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def config_logic(self):
        pass

    def show_routine_page(self, routine=None):
        self.routine_page.refresh_ui(routine)
        self.stacks.setCurrentIndex(1)

    def show_home_page(self):
        self.home_page.refresh_ui()
        self.stacks.setCurrentIndex(0)
