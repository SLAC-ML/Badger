from pkg_resources import get_distribution
from PyQt6.QtWidgets import QMainWindow
from ..pages.home_page import BadgerHomePage


class BadgerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        version = get_distribution('badger-opt').version
        self.setWindowTitle(f'Badger v{version}')
        # self.setWindowIcon(QIcon('qt.png'))
        self.resize(640, 480)
        self.center()

        # Add home page
        home = BadgerHomePage()
        self.setCentralWidget(home)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())
