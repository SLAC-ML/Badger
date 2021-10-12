from PyQt6.QtWidgets import QApplication
import sys
from .windows.main_window import BadgerMainWindow

def launch_gui():
    app = QApplication(sys.argv)

    window = BadgerMainWindow()

    window.show()
    sys.exit(app.exec())
