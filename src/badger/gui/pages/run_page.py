import os
import numpy as np
from PyQt5.QtWidgets import QHBoxLayout, QTabWidget, QVBoxLayout, QMessageBox, QTextEdit
from PyQt5.QtWidgets import QWidget, QSplitter, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from ..windows.opt_monitor import BadgerOptMonitor
from ...archive import list_run, load_run, delete_run
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
                        name = os.path.splitext(file)[0]
                        item_file = QTreeWidgetItem([name])
                        if not self.recent_item:
                            self.recent_item = item_file
                        item_day.addChild(item_file)
                    item_month.addChild(item_day)
                item_year.addChild(item_month)
            items.append(item_year)
        run_tree.insertTopLevelItems(0, items)

        splitter = QSplitter(Qt.Horizontal)

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
        run_tab.addTab(run_view, 'Visualization')
        run_tab.addTab(run_edit, 'Raw Data')
        splitter.addWidget(run_tree)
        splitter.addWidget(run_tab)
        # splitter.setSizes([100, 200])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        vbox.addWidget(splitter, 1)

        # Action bar
        action_bar = QWidget()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)

        cool_font = QFont()
        cool_font.setWeight(QFont.DemiBold)
        # cool_font.setPixelSize(16)

        self.btn_back = btn_back = QPushButton('Back')
        btn_back.setFixedSize(64, 64)
        btn_back.setFont(cool_font)
        self.btn_del = btn_del = QPushButton('Delete')
        btn_del.setFixedSize(64, 64)
        btn_del.setFont(cool_font)
        self.btn_run = btn_run = QPushButton('Rerun')
        btn_run.setFixedSize(64, 64)
        btn_run.setFont(cool_font)
        self.btn_load = btn_load = QPushButton('Load Routine')
        btn_load.setFixedSize(128, 64)
        btn_load.setFont(cool_font)
        hbox_action.addWidget(btn_back)
        hbox_action.addStretch(1)
        hbox_action.addWidget(btn_del)
        hbox_action.addWidget(btn_run)
        hbox_action.addWidget(btn_load)

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
        self.colors = ['c', 'g', 'm', 'y', 'b', 'r', 'w']
        self.symbols = ['o', 't', 't1', 's', 'p', 'h', 'd']

        self.run_tree.currentItemChanged.connect(self.load_run)
        self.run_tree.setCurrentItem(self.recent_item)

        self.btn_back.clicked.connect(self.go_home)
        self.btn_del.clicked.connect(self.delete_run)
        self.btn_run.clicked.connect(self.rerun_routine)
        self.btn_load.clicked.connect(self.load_routine)

    def reconfig_logic(self):
        self.run_tree.setCurrentItem(self.recent_item)

    def load_run(self, current, previous):
        # self.current_item = current
        self.previous_item = previous

        try:
            self.run_name = run_name = current.text(0)
            self.run = run = load_run(run_name + '.yaml')
            self.run_edit.setText(ystring(run))
            self.plot_run()
        except:
            self.run_name = None
            self.run = None
            self.run_edit.setText('')
            self.plot_run()

    def plot_run(self):
        run = self.run
        self.plot_obj.clear()
        try:
            self.plot_con.clear()
        except:
            pass
        self.plot_var.clear()

        if not run:
            self.btn_del.setDisabled(True)
            self.btn_run.setDisabled(True)
            self.btn_load.setDisabled(True)

            try:
                self.run_view.removeItem(self.plot_con)
                del self.plot_con
            except:
                pass

            return

        self.btn_del.setDisabled(False)
        self.btn_run.setDisabled(False)
        self.btn_load.setDisabled(False)

        var_names = [next(iter(d))
                     for d in run['routine']['config']['variables']]
        obj_names = [next(iter(d))
                     for d in run['routine']['config']['objectives']]
        try:
            con_names = [next(iter(d))
                         for d in run['routine']['config']['constraints']]
        except:
            con_names = []
        data = run['data']

        for i, obj_name in enumerate(obj_names):
            color = self.colors[i % len(self.colors)]
            symbol = self.symbols[i % len(self.colors)]
            self.plot_obj.plot(np.array(data[obj_name]), pen=pg.mkPen(color, width=3),
                               # symbol=symbol,
                               name=obj_name)

        if con_names:
            try:
                self.plot_con
            except:
                self.plot_con = plot_con = self.run_view.addPlot(
                    row=1, col=0, title='Evaluation History (C)')
                plot_con.setLabel('left', 'constraints')
                plot_con.setLabel('bottom', 'iterations')
                plot_con.showGrid(x=True, y=True)
                leg_con = plot_con.addLegend()
                leg_con.setBrush((50, 50, 100, 200))

                plot_con.setXLink(self.plot_obj)

            for i, con_name in enumerate(con_names):
                color = self.colors[i % len(self.colors)]
                symbol = self.symbols[i % len(self.colors)]
                try:
                    self.plot_con.plot(np.array(data[con_name]), pen=pg.mkPen(color, width=3),
                                       # symbol=symbol,
                                       name=con_name)
                except:  # Mal-format data
                    pass
        else:
            try:
                self.run_view.removeItem(self.plot_con)
                del self.plot_con
            except:
                pass

        for i, var_name in enumerate(var_names):
            color = self.colors[i % len(self.colors)]
            symbol = self.symbols[i % len(self.colors)]
            self.plot_var.plot(np.array(data[var_name]), pen=pg.mkPen(color, width=3),
                               # symbol=symbol,
                               name=var_name)

    def delete_run(self):
        reply = QMessageBox.question(self,
                                     'Delete Run',
                                     f'Are you sure you want to delete this run data?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        if self.run_name is None:
            return

        delete_run(self.run_name + '.yaml')
        self.run_tree.setCurrentItem(self.previous_item)
        root = self.run_tree.invisibleRootItem()
        (self.previous_item.parent() or root).removeChild(self.previous_item)

    def load_routine(self):
        routine = self.run['routine']

        self.go_routine(routine)

    def rerun_routine(self):
        routine = self.run['routine']
        try:
            self.monitor = BadgerOptMonitor(self, routine, False)
            self.monitor.show()
            self.monitor.start()
        except Exception as e:
            # raise e
            QMessageBox.critical(self, 'Error!', str(e))
