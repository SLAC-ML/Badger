from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtWidgets import QPushButton, QLabel


class BadgerRoutinePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Set up the layout
        vbox = QVBoxLayout(self)

        # Search bar
        panel_search = QWidget()
        hbox_search = QHBoxLayout(panel_search)

        btn_setting = QPushButton('Settings')
        hbox_search.addWidget(btn_setting)

        vbox.addWidget(panel_search)
