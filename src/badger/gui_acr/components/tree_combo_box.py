from PyQt5.QtWidgets import QComboBox, QTreeView, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import QModelIndex, Qt
from ...utils import run_names_to_dict


# Modified based on the following solution
# https://stackoverflow.com/a/9672359/4263605
class TreeComboBox(QComboBox):
    def __init__(self):
        super(TreeComboBox, self).__init__()
        # self.tree = QTreeWidget()
        # self.setView(QTreeWidget())
        # self.setModel(self.tree.model())

        # self.view().setHeaderHidden(True)
        # self.view().setItemsExpandable(False)
        # self.view().setRootIsDecorated(False)
        # self.view().setFixedHeight(256)

    def setModel(self, model):
        super(TreeComboBox, self).setModel(model)
        parent, row = self._firstSelectableItem()
        if row is not None:
            self.setRootModelIndex(parent)
            self.setCurrentIndex(row)

    def showPopup(self):
        self.setRootModelIndex(QModelIndex())
        # self.view().expandAll()
        QComboBox.showPopup(self)

    def _firstSelectableItem(self, parent=QModelIndex()):
        """
        Internal recursive function for finding the first selectable item.
        """
        for i in range(self.model().rowCount(parent)):
            itemIndex = self.model().index(i, 0, parent)
            if self.model().itemFromIndex(itemIndex).isSelectable():
                return parent, i
            else:
                itemIndex, row = self._firstSelectableItem(itemIndex)
                if row is not None:
                    return itemIndex, row
        return parent, None

    def updateItems(self, runs=None):
        self.tree.clear()

        if runs is None:
            return

        items = []
        flag_first_item = True
        first_items = []
        runs_dict = run_names_to_dict(runs)
        for year, dict_year in runs_dict.items():
            item_year = QTreeWidgetItem([year])
            item_year.setFlags(item_year.flags() & ~Qt.ItemIsSelectable)

            if flag_first_item:
                first_items.append(item_year)

            for month, dict_month in dict_year.items():
                item_month = QTreeWidgetItem([month])
                item_month.setFlags(item_month.flags() & ~Qt.ItemIsSelectable)

                if flag_first_item:
                    first_items.append(item_month)

                for day, list_day in dict_month.items():
                    item_day = QTreeWidgetItem([day])
                    item_day.setFlags(item_day.flags() & ~Qt.ItemIsSelectable)

                    if flag_first_item:
                        first_items.append(item_day)
                        flag_first_item = False

                    for i, file in enumerate(list_day):
                        item_file = QTreeWidgetItem([file])
                        item_day.addChild(item_file)
                    item_month.addChild(item_day)
                item_year.addChild(item_month)
            items.append(item_year)
        self.tree.insertTopLevelItems(0, items)
        for item in first_items:
            item.setExpanded(True)
