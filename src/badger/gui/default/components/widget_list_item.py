from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt


class BadgerWidgetListItem(QListWidgetItem):
    def __init__(self, parent, routine, timestamp):
        super().__init__(parent)
        self.setData(Qt.UserRole, (routine, timestamp))
    
    def get_routine_name(self):
        routine, _ = self.data(Qt.UserRole)
        return routine

    def has_same_routine_name(self, name):
        routine, _ = self.data(Qt.UserRole)
        return routine == name