from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem
from PyQt5.QtCore import Qt
from .routine_item import BadgerRoutineItem


class BadgerWidgetList(QListWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.model().rowsInserted.connect(
        self.handleRowsInserted, Qt.QueuedConnection)

    def add_routine_item(self, item):
            _item = QListWidgetItem()
            _item.setSizeHint(item.sizeHint())
            _item.setData(Qt.UserRole, (item.name, item.timestamp))
            self.addItem(_item)
            self.setItemWidget(_item, item)

    def get_routine_name(self, item):
        name, _ = item.data(Qt.UserRole)
        return name              

    def has_same_name(self, item_1, item_2):
        return self.get_routine_name(item_1) == self.get_routine_name(item_2)


    def set_drag_and_drop(self, enable):
        if enable:
            self.setDragEnabled(True)
            self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
            self.setDefaultDropAction(Qt.DropAction.MoveAction)
            for i in range(self.count()):
                self.item(i).setCheckState(Qt.CheckState.Unchecked)
        else:
            self.setDragEnabled(False)
            self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
            self.setDefaultDropAction(Qt.DropAction.IgnoreAction)
            # remove checkboxes from items
            for i in range(self.count()):
                self.item(i).setData(Qt.CheckStateRole, None)


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

    def get_sequence(self, checked_only=True):
        if checked_only:
            return [self.item(i) for i in range(self.count()) if self.item(i).checkState() == Qt.CheckState.Checked]
        return [self.item(i) for i in range(self.count())]
