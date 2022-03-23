import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QSplitter, QTextEdit, QTabWidget, QShortcut
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QComboBox, QStyledItemDelegate, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont
from ..components.search_bar import search_bar
from ..components.data_table import data_table, update_table
from ..components.routine_item import routine_item, stylesheet_normal, stylesheet_selected
from ..components.run_monitor import BadgerOptMonitor
from ...db import list_routine, load_routine, get_runs_by_routine, get_runs
from ...archive import load_run
from ...utils import ystring


stylesheet = '''
QPushButton:hover:pressed
{
    background-color: #C7737B;
}
QPushButton:hover
{
    background-color: #BF616A;
}
QPushButton
{
    background-color: #A9444E;
}
'''

class BadgerHomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.config_logic()

        self.load_all_runs()

    def init_ui(self):
        # Set up the layout
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        # splitter.setSizes([100, 200])
        vbox.addWidget(splitter, 1)

        # Routine panel
        panel_routine = QWidget()
        vbox_routine = QVBoxLayout(panel_routine)

        # Search bar
        panel_search = QWidget()
        hbox_search = QHBoxLayout(panel_search)
        hbox_search.setContentsMargins(0, 0, 0, 0)

        self.sbar = sbar = search_bar()
        sbar.setFixedHeight(36)
        f = sbar.font()
        f.setPixelSize(16)
        sbar.setFont(f)
        self.btn_new = btn_new = QPushButton('+')
        btn_new.setFixedSize(36, 36)
        btn_new.setFont(f)
        hbox_search.addWidget(sbar)
        hbox_search.addWidget(btn_new)
        vbox_routine.addWidget(panel_search)

        # Routine list
        self.routine_list = routine_list = QListWidget()
        routine_list.setAlternatingRowColors(True)
        routine_list.setSpacing(1)
        self.build_routine_list()
        self.prev_routine = None  # last selected routine
        vbox_routine.addWidget(routine_list)

        # Info panel
        panel_info = QWidget()
        vbox_info = QVBoxLayout(panel_info)

        panel_view = QWidget()
        vbox_view = QVBoxLayout(panel_view)
        vbox_view.setContentsMargins(0, 0, 0, 0)
        vbox_info.addWidget(panel_view)

        # History run nav
        history_nav_bar = QWidget()
        hbox_nav = QHBoxLayout(history_nav_bar)
        hbox_nav.setContentsMargins(0, 0, 0, 0)
        vbox_view.addWidget(history_nav_bar)

        label_nav = QLabel('History Run')
        self.cb_history = cb_history = QComboBox()
        cb_history.setItemDelegate(QStyledItemDelegate())
        self.btn_prev = btn_prev = QPushButton('<')
        self.btn_next = btn_next = QPushButton('>')
        btn_prev.setFixedWidth(32)
        btn_next.setFixedWidth(32)
        btn_prev.setDisabled(True)
        btn_next.setDisabled(True)
        hbox_nav.addWidget(label_nav)
        hbox_nav.addWidget(cb_history, 1)
        hbox_nav.addWidget(btn_prev)
        hbox_nav.addWidget(btn_next)

        # Routine edit + run monitor + data table
        self.splitter_run = splitter_run = QSplitter(Qt.Vertical)
        splitter_run.setStretchFactor(0, 0)
        splitter_run.setStretchFactor(1, 1)
        splitter_run.setStretchFactor(2, 0)
        vbox_view.addWidget(splitter_run)

        # Run monitor
        self.run_view = run_view = QWidget()  # for consistent bg
        vbox_run_view = QVBoxLayout(run_view)
        vbox_run_view.setContentsMargins(0, 10, 0, 0)
        self.run_monitor = run_monitor = BadgerOptMonitor(None, False, self.inspect_solution)
        vbox_run_view.addWidget(run_monitor)

        # Data table
        self.run_table = run_table = data_table()

        # Routine edit
        self.run_edit = run_edit = QTextEdit()

        splitter_run.addWidget(run_edit)
        splitter_run.addWidget(run_view)
        splitter_run.addWidget(run_table)
        splitter_run.setSizes([0, 1, 0])  # collapse routine/table by default

        # Action bar
        action_bar = QWidget()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)

        cool_font = QFont()
        cool_font.setWeight(QFont.DemiBold)
        # cool_font.setPixelSize(16)

        self.btn_del = btn_del = QPushButton('Delete')
        btn_del.setFixedSize(64, 64)
        btn_del.setFont(cool_font)
        btn_del.setStyleSheet(stylesheet)
        self.btn_edit = btn_edit = QPushButton('Edit')
        btn_edit.setFixedSize(64, 64)
        btn_edit.setFont(cool_font)
        self.btn_run = btn_run = QPushButton('Run')
        btn_run.setFixedSize(128, 64)
        btn_run.setFont(cool_font)
        hbox_action.addWidget(btn_del)
        hbox_action.addStretch(1)
        hbox_action.addWidget(btn_edit)
        hbox_action.addWidget(btn_run)
        vbox_info.addWidget(action_bar)

        # Add panels to splitter
        splitter.addWidget(panel_routine)
        splitter.addWidget(panel_info)

    def config_logic(self):
        self.colors = ['c', 'g', 'm', 'y', 'b', 'r', 'w']
        self.symbols = ['o', 't', 't1', 's', 'p', 'h', 'd']

        self.sbar.textChanged.connect(self.build_routine_list)
        self.routine_list.itemClicked.connect(self.select_routine)
        self.run_table.cellClicked.connect(self.solution_selected)
        self.run_table.itemSelectionChanged.connect(self.table_selection_changed)

        self.cb_history.currentIndexChanged.connect(self.go_run)
        self.btn_prev.clicked.connect(self.go_prev_run)
        self.btn_next.clicked.connect(self.go_next_run)

        self.btn_run.clicked.connect(self.run_optimization)

        # Assign shortcuts
        self.shortcut_go_search = QShortcut(QKeySequence('Ctrl+L'), self)
        self.shortcut_go_search.activated.connect(self.go_search)

    def go_search(self):
        self.sbar.setFocus()

    def load_all_runs(self):
        runs = get_runs()
        self.cb_history.clear()
        self.cb_history.addItems(runs)

    def select_routine(self, item):
        if self.prev_routine:
            try:
                self.routine_list.itemWidget(self.prev_routine).setStyleSheet(stylesheet_normal)
            except:
                pass

            if self.prev_routine.routine == item.routine:  # click a routine again to deselect
                self.prev_routine = None
                return self.load_all_runs()

        self.prev_routine = item

        routine, timestamp = load_routine(item.routine)
        self.run_monitor.set_routine(routine)
        self.run_edit.setText(ystring(routine))
        runs = get_runs_by_routine(routine['name'])

        self.cb_history.clear()
        if runs:
            self.cb_history.addItems(runs)
        else:
            self.run_monitor.plot_run(None)

        self.routine_list.itemWidget(item).setStyleSheet(stylesheet_selected)

    def build_routine_list(self, keyword=''):
        routines, timestamps = list_routine(keyword)

        try:
            selected_routine = self.prev_routine.routine
        except:
            selected_routine = None
        self.routine_list.clear()
        for i, routine in enumerate(routines):
            _item = routine_item(routine, timestamps[i])
            item = QListWidgetItem(self.routine_list)
            item.routine = routine  # dirty trick
            item.setSizeHint(_item.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, _item)
            if routine == selected_routine:
                _item.setStyleSheet(stylesheet_selected)
                self.prev_routine = item

    def go_run(self, i):
        if i == -1:
            update_table(self.run_table)
            self.run_monitor.plot_run(None)
            return

        run_filename = self.cb_history.currentText()
        run = load_run(run_filename)
        update_table(self.run_table, run['data'])
        self.run_monitor.plot_run(run)

        idx = self.cb_history.currentIndex()
        if idx == 0:
            self.btn_prev.setDisabled(True)
        else:
            self.btn_prev.setDisabled(False)
        n = self.cb_history.count()
        if idx == n - 1:
            self.btn_next.setDisabled(True)
        else:
            self.btn_next.setDisabled(False)

        self.run_edit.setText(ystring(run['routine']))

    def go_prev_run(self):
        idx = self.cb_history.currentIndex()
        self.cb_history.setCurrentIndex(idx - 1)

    def go_next_run(self):
        idx = self.cb_history.currentIndex()
        self.cb_history.setCurrentIndex(idx + 1)

    def inspect_solution(self, idx):
        self.run_table.selectRow(idx)

    def solution_selected(self, r, c):
        self.run_monitor.jump_to_solution(r)

    def table_selection_changed(self):
        indices = self.run_table.selectedIndexes()
        if len(indices) == 1:  # let other method handles it
            return

        row = -1
        for index in indices:
            _row = index.row()
            if _row == row:
                continue

            if row == -1:
                row = _row
                continue

            return

        self.run_monitor.jump_to_solution(row)

    def run_optimization(self):
        self.run_monitor.start()
