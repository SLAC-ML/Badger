from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
import sys
# import ctypes
from .windows.main_window import BadgerMainWindow

# Fix the scaling issue on multiple monitors w/ different scaling settings
# if sys.platform == 'win32':
#     ctypes.windll.shcore.SetProcessDpiAwareness(1)

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# if hasattr(QtCore.Qt, 'HighDpiScaleFactorRoundingPolicy'):
#     QApplication.setAttribute(
#         QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)


def launch_gui():
    app = QApplication(sys.argv)

    window = BadgerMainWindow()

    window.show()

    # timer = QtCore.QTimer()
    # timer.timeout.connect(lambda: None)
    # timer.start(100)

    sys.exit(app.exec())
