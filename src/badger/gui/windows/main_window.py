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
        self.resize(640, 480)
        self.center()

        # Add pages
        self.home_page = BadgerHomePage()
        self.routine_page = BadgerRoutinePage(None)

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
        self.home_page.btn_new.clicked.connect(self.show_routine_page)
        self.routine_page.btn_back.clicked.connect(self.show_home_page)

    def show_routine_page(self):
        self.stacks.setCurrentIndex(1)

    def show_home_page(self):
        self.stacks.setCurrentIndex(0)
