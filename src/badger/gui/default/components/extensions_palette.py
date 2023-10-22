from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, \
    QWidget, QLabel
from badger.gui.default.components.analysis_extensions import DataViewer, \
    AnalysisExtension


class ExtensionsPalette(QMainWindow):
    def __init__(self, run_monitor):
        super(ExtensionsPalette, self).__init__()

        self.run_monitor = run_monitor

        self.setWindowTitle('PyQt Button Window')
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.text_box = QLabel("0", self)
        self.btn_data_viewer = QPushButton('Data Viewer')

        layout.addWidget(self.text_box)
        layout.addWidget(self.btn_data_viewer)

        central_widget.setLayout(layout)

        self.btn_data_viewer.clicked.connect(self.add_data_viewer)

    def update_palette(self):
        self.text_box.setText(str(len(self.run_monitor.active_extensions)))

    def add_child_window_to_monitor(self, child_window: AnalysisExtension):
        child_window.show()
        child_window.window_closed.connect(self.run_monitor.extension_window_closed)
        self.run_monitor.active_extensions.append(child_window)

        self.update_palette()

    def add_data_viewer(self):
        self.add_child_window_to_monitor(DataViewer())


