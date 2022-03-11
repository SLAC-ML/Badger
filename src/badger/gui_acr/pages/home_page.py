from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QSplitter, QTextEdit, QTabWidget, QShortcut
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont
import pyqtgraph as pg
from ..components.search_bar import search_bar
from ..components.routine_item import routine_item
from ...db import list_routine, load_routine
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
        vbox_routine.addWidget(routine_list)

        # Info panel
        panel_info = QWidget()
        vbox_info = QVBoxLayout(panel_info)

        # Run tab
        self.run_tab = run_tab = QTabWidget()
        # Config the plot
        self.run_view = run_view = pg.GraphicsLayoutWidget()
        pg.setConfigOptions(antialias=True)
        self.plot_obj = plot_obj = run_view.addPlot(
            title='Evaluation History (Y)')
        plot_obj.setLabel('left', 'objectives')
        plot_obj.setLabel('bottom', 'iterations')
        plot_obj.showGrid(x=True, y=True)
        leg_obj = plot_obj.addLegend()
        leg_obj.setBrush((50, 50, 100, 200))

        run_view.nextRow()
        run_view.nextRow()

        self.plot_var = plot_var = run_view.addPlot(
            title='Evaluation History (X)')
        plot_var.setLabel('left', 'variables')
        plot_var.setLabel('bottom', 'iterations')
        plot_var.showGrid(x=True, y=True)
        leg_var = plot_var.addLegend()
        leg_var.setBrush((50, 50, 100, 200))

        plot_var.setXLink(plot_obj)

        # Config the raw data viewer
        self.run_edit = run_edit = QTextEdit()
        run_tab.addTab(run_view, 'History')
        run_tab.addTab(run_edit, 'Routine')
        vbox_info.addWidget(run_tab)

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
        self.sbar.textChanged.connect(self.build_routine_list)
        self.routine_list.itemClicked.connect(self.select_routine)

        # Assign shortcuts
        self.shortcut_go_search = QShortcut(QKeySequence('Ctrl+L'), self)
        self.shortcut_go_search.activated.connect(self.go_search)

    def go_search(self):
        self.sbar.setFocus()

    def select_routine(self, item):
        routine, timestamp = load_routine(item.routine)
        self.run_edit.setText(ystring(routine))
        # print(routine)
        # self.run_edit.setText(routine)

    def build_routine_list(self, keyword=''):
        routines, timestamps = list_routine(keyword)

        self.routine_list.clear()
        for i, routine in enumerate(routines):
            _item = routine_item(routine, timestamps[i])
            item = QListWidgetItem(self.routine_list)
            item.routine = routine  # dirty trick
            item.setSizeHint(_item.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, _item)
