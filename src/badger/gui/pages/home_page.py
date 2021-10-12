from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtGui import QIcon
from ..components.search_bar import search_bar


class BadgerHomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Set up the layout
        vbox = QVBoxLayout(self)

        # Search bar
        panel_search = QWidget()
        hbox_search = QHBoxLayout(panel_search)

        sbar = search_bar()
        btn_setting = QPushButton('Settings')
        hbox_search.addWidget(sbar)
        hbox_search.addWidget(btn_setting)

        vbox.addWidget(panel_search)

        # Recent routines
        panel_recent = QWidget()
        vbox_recent = QVBoxLayout(panel_recent)

        label_recent = QLabel('Recent Routines')
        vbox_recent.addWidget(label_recent)

        hbox_recent = QHBoxLayout()
        btn1 = QPushButton('+')
        btn1.setMinimumHeight(64)
        btn2 = QPushButton('lcls emittance')
        btn2.setMinimumHeight(64)
        btn3 = QPushButton('spear3 lossrate')
        btn3.setMinimumHeight(64)
        hbox_recent.addWidget(btn1)
        hbox_recent.addWidget(btn2)
        hbox_recent.addWidget(btn3)
        vbox_recent.addLayout(hbox_recent)

        vbox.addWidget(panel_recent)

        # All routines
        panel_all = QWidget()
        vbox_all = QVBoxLayout(panel_all)

        label_all = QLabel('All Routines')
        vbox_all.addWidget(label_all)

        btn1 = QPushButton('lcls emittance')
        btn2 = QPushButton('spear3 lossrate')
        btn3 = QPushButton('test')

        vbox_all.addWidget(btn1)
        vbox_all.addWidget(btn2)
        vbox_all.addWidget(btn3)
        vbox_all.addStretch()

        vbox.addWidget(panel_all)

        # stylesheet = (
        #     'background-color: red;'
        # )
        # self.setStyleSheet(stylesheet)
