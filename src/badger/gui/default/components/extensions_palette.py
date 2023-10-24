from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, \
    QWidget, QLabel
from badger.gui.default.components.analysis_extensions import AnalysisExtension, \
    ParetoFrontViewer


class ExtensionsPalette(QMainWindow):
    def __init__(self, run_monitor):
        super(ExtensionsPalette, self).__init__()

        self.run_monitor = run_monitor

        self.setWindowTitle('Badger Extensions Palette')
        self.setGeometry(100, 100, 200, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.base_text = "Number of active exensions: "
        self.text_box = QLabel(self.base_text + "0", self)

        self.btn_data_viewer = QPushButton('ParetoFrontViewer')

        layout.addWidget(self.text_box)
        layout.addWidget(self.btn_data_viewer)

        central_widget.setLayout(layout)

        self.btn_data_viewer.clicked.connect(self.add_pf_viewer)

    @property
    def n_active_extensions(self):
        return len(self.run_monitor.active_extensions)

    def update_palette(self):
        self.text_box.setText(
            self.base_text + str(self.n_active_extensions))

    def add_pf_viewer(self):
        self.add_child_window_to_monitor(ParetoFrontViewer())

    def add_child_window_to_monitor(self, child_window: AnalysisExtension):
        child_window.show()
        child_window.window_closed.connect(self.run_monitor.extension_window_closed)
        self.run_monitor.active_extensions.append(child_window)

        if self.run_monitor.routine is not None:
            self.run_monitor.active_extensions[-1].update_window(
                self.run_monitor.routine
            )

        self.update_palette()


