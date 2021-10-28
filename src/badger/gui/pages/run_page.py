import os
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QTextEdit
from PyQt5.QtWidgets import QWidget, QFrame, QSplitter, QPushButton, QListWidgetItem, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ...archive import list_run, load_run
from ...utils import ystring


class BadgerRunPage(QWidget):
    def __init__(self, go_routine=None, go_home=None):
        super().__init__()

        # go_xxx is a function that jumps to the corresponding page once called
        self.go_routine = go_routine
        self.go_home = go_home

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        self.runs = runs = list_run()
        self.all_runs = []

        # Set up the layout
        vbox = QVBoxLayout(self)

        # History run list
        self.run_list = run_list = QListWidget()
        run_list.setAlternatingRowColors(True)
        # run_list.setSpacing(1)
        for i, run in enumerate(runs):
            item = QListWidgetItem(os.path.splitext(run)[0])
            run_list.addItem(item)

        splitter = QSplitter(Qt.Horizontal)
        self.run_view = run_view = QTextEdit()
        splitter.addWidget(run_list)
        splitter.addWidget(run_view)
        # splitter.setSizes([100, 200])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        vbox.addWidget(splitter, 1)

        # Action bar
        action_bar = QWidget()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)
        self.btn_back = btn_back = QPushButton('Back')

        cool_font = QFont()
        cool_font.setWeight(QFont.DemiBold)
        # cool_font.setPixelSize(16)

        btn_back.setFixedSize(64, 64)
        btn_back.setFont(cool_font)
        hbox_action.addWidget(btn_back)
        hbox_action.addStretch(1)

        vbox.addWidget(action_bar)

    def config_logic(self):
        self.run_list.currentItemChanged.connect(self.load_run)
        self.run_list.setCurrentRow(0)

        self.btn_back.clicked.connect(self.go_home)

    def load_run(self):
        run_name = self.run_list.currentItem().text()
        run = load_run(run_name + '.yaml')
        self.run_view.setText(ystring(run))
