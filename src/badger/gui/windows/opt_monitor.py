import numpy as np
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
from PyQt6 import QtCore
import pyqtgraph as pg


class BadgerOptMonitor(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        self.setWindowTitle('Opt Monitor')
        self.resize(2560, 1280)

        vbox = QVBoxLayout(self)

        monitor = pg.GraphicsLayoutWidget()
        # monitor.resize(1000, 600)
        pg.setConfigOptions(antialias=True)

        self.plot_obj = plot_obj = monitor.addPlot(title='Evaluation History (Y)')
        plot_obj.setLabel('left', 'objectives')
        plot_obj.setLabel('bottom', 'iterations')
        plot_obj.showGrid(x=True, y=True)

        self.plot_var = plot_var = monitor.addPlot(title='Evaluation History (X)')
        plot_var.setLabel('left', 'variables')
        plot_var.setLabel('bottom', 'iterations')
        plot_var.showGrid(x=True, y=True)

        self.btn_ok = btn_ok = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)

        vbox.addWidget(monitor)
        vbox.addWidget(btn_ok)

    def config_logic(self):
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'w']
        self.symbols = ['o', 't', 't1', 's', 'p', 'h', 'd']
        self.vars = []
        self.objs = []
        self.curves_var = []
        self.curves_obj = []

        self.btn_ok.accepted.connect(self.accept)

    def update(self, vars, objs):
        self.vars.append(vars)
        self.objs.append(objs)

        if not self.curves_obj:
            for i in range(len(objs)):
                color = self.colors[i % 7]
                symbol = self.symbols[i % 7]
                _curve = self.plot_obj.plot(pen=color, symbol=symbol)
                self.curves_obj.append(_curve)

        if not self.curves_var:
            for i in range(len(vars)):
                color = self.colors[i % 7]
                symbol = self.symbols[i % 7]
                _curve = self.plot_var.plot(pen=color, symbol=symbol)
                self.curves_var.append(_curve)

        for i in range(len(objs)):
            self.curves_obj[i].setData(np.array(self.objs)[:, i])

        for i in range(len(vars)):
            self.curves_var[i].setData(np.array(self.vars)[:, i])
