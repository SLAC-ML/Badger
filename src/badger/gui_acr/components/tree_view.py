import os
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


def update_tree_view(tree_view, runs=None):
    tree_view.clear()

    if runs is None:
        return tree_view

    items = []
    for year, dict_year in runs.items():
        item_year = QTreeWidgetItem([year])
        for month, dict_month in dict_year.items():
            item_month = QTreeWidgetItem([month])
            for day, list_day in dict_month.items():
                item_day = QTreeWidgetItem([day])
                for i, file in enumerate(list_day):
                    item_file = QTreeWidgetItem([file])
                    item_day.addChild(item_file)
                item_month.addChild(item_day)
            item_year.addChild(item_month)
        items.append(item_year)
    tree_view.insertTopLevelItems(0, items)

    return tree_view


def tree_view(runs=None):
    # History run list
    run_tree = QTreeWidget()
    run_tree.setColumnCount(1)
    run_tree.setHeaderHidden(True)
    # run_tree.setHeaderLabels(['Tree View'])
    # run_list.setSpacing(1)
    return update_tree_view(run_tree, runs)
