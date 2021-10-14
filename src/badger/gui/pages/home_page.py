from datetime import datetime
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QCompleter
from PyQt6.QtWidgets import QPushButton, QGroupBox, QListWidgetItem, QListWidget
from PyQt6.QtGui import QIcon
from ..components.search_bar import search_bar
from ...db import list_routines


class BadgerHomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        routines, timestamps = list_routines()

        # Set up the layout
        vbox = QVBoxLayout(self)

        # Search bar
        panel_search = QWidget()
        hbox_search = QHBoxLayout(panel_search)

        self.sbar = sbar = search_bar(routines)
        btn_setting = QPushButton('Settings')
        hbox_search.addWidget(sbar)
        hbox_search.addWidget(btn_setting)

        vbox.addWidget(panel_search)

        # Recent routines
        group_recent = QGroupBox('Recent Routines')
        self.hbox_recent = hbox_recent = QHBoxLayout(group_recent)

        self.btn_new = btn_new = QPushButton('+')
        btn_new.setMinimumHeight(64)
        btn_new.setFixedWidth(64)
        hbox_recent.addWidget(btn_new)

        for routine in routines[:-4:-1]:
            btn = QPushButton(routine)
            btn.setMinimumHeight(64)
            hbox_recent.addWidget(btn)

        vbox.addWidget(group_recent)

        # All routines
        group_all = QGroupBox('All Routines')
        self.routine_list = routine_list = QListWidget()
        vbox_all = QVBoxLayout(group_all)
        vbox_all.addWidget(routine_list)

        for i, routine in enumerate(routines):
            routine_widget = QWidget()
            routine_layout = QHBoxLayout()
            routine_widget.setLayout(routine_layout)
            timestamp = datetime.fromisoformat(timestamps[i])
            time_str = timestamp.strftime('%m/%d/%Y, %H:%M:%S')
            btn = QPushButton(f'{routine}: {time_str}')
            btn.setMinimumHeight(24)
            routine_layout.addWidget(btn)
            item = QListWidgetItem(routine_list)
            item.setSizeHint(routine_widget.sizeHint())
            routine_list.addItem(item)
            routine_list.setItemWidget(item, btn)

        vbox.addWidget(group_all)

        # stylesheet = (
        #     'background-color: red;'
        # )
        # self.setStyleSheet(stylesheet)

    def refresh_ui(self):
        routines, timestamps = list_routines()

        # Update the search bar completer
        completer = QCompleter(routines)
        self.sbar.setCompleter(completer)

        # Update recent routines
        for i in reversed(range(self.hbox_recent.count())):
            if not i:  # keep the "+" button
                break

            _widget = self.hbox_recent.itemAt(i).widget()
            # remove it from the layout list
            self.hbox_recent.removeWidget(_widget)
            # remove it from the gui
            _widget.setParent(None)

        for routine in routines[:-4:-1]:
            btn = QPushButton(routine)
            btn.setMinimumHeight(64)
            self.hbox_recent.addWidget(btn)

        # Update all routines
        self.routine_list.clear()

        for i, routine in enumerate(routines):
            routine_widget = QWidget()
            routine_layout = QHBoxLayout()
            routine_widget.setLayout(routine_layout)
            timestamp = datetime.fromisoformat(timestamps[i])
            time_str = timestamp.strftime('%m/%d/%Y, %H:%M:%S')
            btn = QPushButton(f'{routine}: {time_str}')
            btn.setMinimumHeight(24)
            routine_layout.addWidget(btn)
            item = QListWidgetItem(self.routine_list)
            item.setSizeHint(routine_widget.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, btn)
