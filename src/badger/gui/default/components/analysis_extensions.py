from abc import ABC, abstractmethod

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QWidget

from badger.core import Routine
import pyqtgraph as pg


class AnalysisExtension(QDialog):
    window_closed = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    @abstractmethod
    def update_window(self, routine: Routine):
        pass

    def closeEvent(self, event) -> None:
        self.window_closed.emit(self)
        super().closeEvent(event)


class ScatterPlotViewer(QWidget):
    def __init__(self):
        super(ScatterPlotViewer, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Create a PyQtGraph plot widget
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.scatter_plot = self.plot_widget.plot(pen=None, symbol='o', symbolSize=10)

    def update_plot(self, routine: Routine):
        # Extract x and y data from the DataFrame
        x = routine.data[routine.vocs.objective_names[0]]
        y = routine.data[routine.vocs.objective_names[0]]

        # Update the scatter plot
        self.scatter_plot.setData(x=x, y=y)

        # set labels
        self.plot_widget.setLabel("left", routine.vocs.objective_names[0])
        self.plot_widget.setLabel("bottom", routine.vocs.objective_names[0])


class DataViewer(AnalysisExtension):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Window")

        self.text_box = QLabel("Enter text here", self)

        self.plot_window = ScatterPlotViewer()

        layout = QVBoxLayout()
        layout.addWidget(self.text_box)
        layout.addWidget(self.plot_window)
        self.setLayout(layout)

    def update_window(self, routine: Routine):
        print(len(routine.data))
        self.text_box.setText(str(len(routine.data)))
        self.plot_window.update_plot(routine)
