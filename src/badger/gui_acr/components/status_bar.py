from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QTextEdit, QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class BadgerStatusBar(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.summary = summary = QLabel()
        summary.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        summary.setAlignment(Qt.AlignCenter)
        vbox.addWidget(summary)

    def config_logic(self):
        pass

    def set_summary(self, text):
        self.summary.setText(text)
