from PyQt6.QtWidgets import QApplication, QWidget
import sys

def launch_gui():
    app = QApplication(sys.argv)

    window = QWidget()
    window.show()
    sys.exit(app.exec())
