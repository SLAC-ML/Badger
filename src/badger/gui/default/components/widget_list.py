from PyQt5.QtWidgets import QListWidget, QAbstractItemView
from PyQt5.QtCore import Qt
from .routine_item import BadgerRoutineItem


class BadgerWidgetList(QListWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.model().rowsInserted.connect(
        self.handleRowsInserted, Qt.QueuedConnection)

    def set_drag_and_drop(self, enable):
        if enable:
            self.setDragEnabled(True)
            self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
            self.setDefaultDropAction(Qt.DropAction.MoveAction)
            self.uncheck_all()
        else:
            self.setDragEnabled(False)
            self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
            self.setDefaultDropAction(Qt.DropAction.IgnoreAction)

    def uncheck_all(self):
        for i in range(self.count()):
            self.item(i).setCheckState(Qt.CheckState.Unchecked)

    def handleRowsInserted(self, parent, first, last):
        # restore item widget after serialiation during drag and drop
        for index in range(self.count()):
            item = self.item(index)
            if item is not None and self.itemWidget(item) is None:
                routine, timestamp = item.data(Qt.UserRole)
                print(routine)
                widget = BadgerRoutineItem(routine, timestamp)
                item.setSizeHint(widget.sizeHint())
                self.setItemWidget(item, widget)

    def get_sequence():
        pass
