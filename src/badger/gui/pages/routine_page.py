from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtWidgets import QPushButton, QLabel


class BadgerRoutinePage(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name

        self.init_ui()

    def init_ui(self):
        # Set up the layout
        vbox = QVBoxLayout(self)

        # Action bar
        self.btn_back = btn_back = QPushButton('Back')
        btn_back.setFixedWidth(64)
        vbox.addWidget(btn_back)

        vbox.addStretch()
