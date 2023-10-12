from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel

from badger.core import Routine


class AnalysisExtension(QDialog):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def update_window(self, routine: Routine):
        pass


class DataViewer(AnalysisExtension):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Window")

        self.text_box = QLabel("Enter text here", self)

        layout = QVBoxLayout()
        layout.addWidget(self.text_box)
        self.setLayout(layout)

    @abstractmethod
    def update_window(self, routine: Routine):
        print(routine)
        self.text_box.setText(routine)
