from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt


def update_tree_view(tree_view, runs=None):
    tree_view.clear()

    if runs is None:
        return tree_view

    items = []
    flag_first_item = True
    first_items = []
    for year, dict_year in runs.items():
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
    tree_view.insertTopLevelItems(0, items)
    for item in first_items:
        item.setExpanded(True)

    return tree_view


def tree_view(runs=None):
    # History run list
    run_tree = QTreeWidget()
    run_tree.setColumnCount(1)
    run_tree.setHeaderHidden(True)
    # run_tree.setHeaderLabels(['Tree View'])
    # run_list.setSpacing(1)
    update_tree_view(run_tree, runs)
    run_tree.setFixedHeight(256)
    return run_tree
