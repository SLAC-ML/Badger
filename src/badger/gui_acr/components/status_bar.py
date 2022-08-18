from pkg_resources import resource_filename
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from ..windows.settings_dialog import BadgerSettingsDialog


class BadgerStatusBar(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.summary = summary = QLabel()
        self.btn_settings = btn_settings = QPushButton()
        icon_path = resource_filename(__name__, '../images/gear.png')
        btn_settings.setFixedSize(24, 24)
        btn_settings.setIcon(QIcon(icon_path))
        # btn_settings.setIconSize(QSize(18, 18))
        summary.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        summary.setAlignment(Qt.AlignCenter)
        hbox.addWidget(summary, 1)
        hbox.addWidget(btn_settings)

    def config_logic(self):
        self.btn_settings.clicked.connect(self.go_settings)

    def set_summary(self, text):
        self.summary.setText(text)

    def go_settings(self):
        dlg = BadgerSettingsDialog(self)
        dlg.exec()
