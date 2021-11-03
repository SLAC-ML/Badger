import os
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QTextEdit
from PyQt5.QtWidgets import QWidget, QSplitter, QPushButton, QTreeWidget, QTreeWidgetItem
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

        # Set up the layout
        vbox = QVBoxLayout(self)

        # History run list
        self.run_tree = run_tree = QTreeWidget()
        self.recent_item = None
        run_tree.setColumnCount(1)
        run_tree.setHeaderLabels(['History Run'])
        # run_list.setSpacing(1)
        items = []
        for year, dict_year in runs.items():
            item_year = QTreeWidgetItem([year])
            for month, dict_month in dict_year.items():
                item_month = QTreeWidgetItem([month])
                for day, list_day in dict_month.items():
                    item_day = QTreeWidgetItem([day])
                    for i, file in enumerate(list_day):
                        item_file = QTreeWidgetItem([file])
                        if not self.recent_item:
                            self.recent_item = item_file
                        item_day.addChild(item_file)
                    item_month.addChild(item_day)
                item_year.addChild(item_month)
            items.append(item_year)
        run_tree.insertTopLevelItems(0, items)

        splitter = QSplitter(Qt.Horizontal)
        self.run_view = run_view = QTextEdit()
        splitter.addWidget(run_tree)
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

    def refresh_ui(self):
        self.runs = runs = list_run()

        self.run_tree.clear()
        self.recent_item = None

        items = []
        for year, dict_year in runs.items():
            item_year = QTreeWidgetItem([year])
            for month, dict_month in dict_year.items():
                item_month = QTreeWidgetItem([month])
                for day, list_day in dict_month.items():
                    item_day = QTreeWidgetItem([day])
                    for file in list_day:
                        name = os.path.splitext(file)[0]
                        item_file = QTreeWidgetItem([name])
                        if not self.recent_item:
                            self.recent_item = item_file
                        item_day.addChild(item_file)
                    item_month.addChild(item_day)
                item_year.addChild(item_month)
            items.append(item_year)
        self.run_tree.insertTopLevelItems(0, items)

    def config_logic(self):
        self.run_tree.currentItemChanged.connect(self.load_run)
        self.run_tree.setCurrentItem(self.recent_item)

        self.btn_back.clicked.connect(self.go_home)

    def reconfig_logic(self):
        self.run_tree.setCurrentItem(self.recent_item)

    def load_run(self, current, previous):
        try:
            run_name = current.text(0)
            run = load_run(run_name + '.yaml')
            self.run_view.setText(ystring(run))
        except Exception as e:
            self.run_view.setText('')
