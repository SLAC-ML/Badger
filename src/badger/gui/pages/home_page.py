from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QCompleter
from PyQt5.QtWidgets import QPushButton, QGroupBox, QListWidgetItem, QListWidget, QShortcut
from PyQt5.QtGui import QIcon, QKeySequence, QFont
from ..components.search_bar import search_bar
from ..windows.settings_dialog import BadgerSettingsDialog
from ...db import list_routine, load_routine


class BadgerHomePage(QWidget):
    def __init__(self, go_routine=None, go_run=None):
        super().__init__()

        # go_xxx is a function that jumps to the corresponding page once called
        self.go_routine = go_routine
        self.go_run = go_run

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        routines, timestamps = list_routine()
        self.routines = routines

        self.recent_routines = []
        self.all_routines = []

        # Set up the layout
        vbox = QVBoxLayout(self)

        # Search bar
        panel_search = QWidget()
        hbox_search = QHBoxLayout(panel_search)
        hbox_search.setContentsMargins(0, 0, 0, 0)

        self.sbar = sbar = search_bar(routines)
        self.btn_setting = btn_setting = QPushButton('Settings')
        btn_setting.setFixedSize(96, 24)
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
            self.recent_routines.append([routine, btn])

        vbox.addWidget(group_recent)

        # All routines
        group_all = QGroupBox('All Routines')
        self.routine_list = routine_list = QListWidget()
        routine_list.setAlternatingRowColors(True)
        routine_list.setSpacing(1)
        vbox_all = QVBoxLayout(group_all)
        vbox_all.addWidget(routine_list)

        for i, routine in enumerate(routines):
            # timestamp = datetime.fromisoformat(timestamps[i])
            # time_str = timestamp.strftime('%m/%d/%Y, %H:%M:%S')
            # item = QListWidgetItem(f'{routine}: {time_str}')
            # routine_list.addItem(item)
            # self.all_routines.append([routine, item])
            routine_widget = QWidget()
            routine_layout = QHBoxLayout()
            routine_widget.setLayout(routine_layout)
            timestamp = datetime.fromisoformat(timestamps[i])
            time_str = timestamp.strftime('%m/%d/%Y, %H:%M:%S')
            btn = QPushButton(f'{routine}: {time_str}')
            # btn.setMinimumHeight(24)
            routine_layout.addWidget(btn)
            item = QListWidgetItem(routine_list)
            item.setSizeHint(routine_widget.sizeHint())
            routine_list.addItem(item)
            routine_list.setItemWidget(item, btn)
            self.all_routines.append([routine, btn])

        vbox.addWidget(group_all)

        # Action bar
        action_bar = QWidget()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)
        self.btn_run = btn_run = QPushButton('History Runs')

        cool_font = QFont()
        cool_font.setWeight(QFont.DemiBold)
        # cool_font.setPixelSize(16)

        btn_run.setFixedSize(256, 64)
        btn_run.setFont(cool_font)
        hbox_action.addStretch(1)
        hbox_action.addWidget(btn_run)

        vbox.addWidget(action_bar)

        # stylesheet = (
        #     'background-color: red;'
        # )
        # self.setStyleSheet(stylesheet)

    def config_logic(self):
        self.btn_new.clicked.connect(lambda: self._go_routine(None))
        for item in self.recent_routines + self.all_routines:
            routine, btn = item
            btn.clicked.connect(lambda x, routine=routine: self._go_routine(routine))

        self.sbar.returnPressed.connect(self.check_n_go_routine)
        self.btn_setting.clicked.connect(self.go_settings)
        self.btn_run.clicked.connect(self.go_run)

        # Assign shortcuts
        self.shortcut_go_search = QShortcut(QKeySequence('Ctrl+L'), self)
        self.shortcut_go_search.activated.connect(self.go_search)

    def refresh_ui(self):
        routines, timestamps = list_routine()
        self.routines = routines

        self.recent_routines = []
        self.all_routines = []

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
            self.recent_routines.append([routine, btn])

        # Update all routines
        self.routine_list.clear()

        for i, routine in enumerate(routines):
            routine_widget = QWidget()
            routine_layout = QHBoxLayout()
            routine_widget.setLayout(routine_layout)
            timestamp = datetime.fromisoformat(timestamps[i])
            time_str = timestamp.strftime('%m/%d/%Y, %H:%M:%S')
            btn = QPushButton(f'{routine}: {time_str}')
            # btn.setMinimumHeight(24)
            routine_layout.addWidget(btn)
            item = QListWidgetItem(self.routine_list)
            item.setSizeHint(routine_widget.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, btn)
            self.all_routines.append([routine, btn])

    def reconfig_logic(self):
        for item in self.recent_routines + self.all_routines:
            routine, btn = item
            btn.clicked.connect(
                lambda x, routine=routine: self._go_routine(routine))

    def check_n_go_routine(self):
        if self.go_routine is None:
            return

        routine_name = self.sbar.text()

        if not routine_name:
            self.go_routine(None)
            return

        if routine_name in self.routines:
            routine, _ = load_routine(routine_name)
            self.go_routine(routine)
            return

        QMessageBox.warning(
            self, 'Warning!', f'Routine {routine_name} not found in the database!')

    def go_search(self):
        self.sbar.setFocus()

    def _go_routine(self, routine_name):
        if self.go_routine is None:
            return

        if routine_name is None:
            self.go_routine(None)
            return

        routine, _ = load_routine(routine_name)
        self.go_routine(routine)

    def go_settings(self):
        dlg = BadgerSettingsDialog(self)
        dlg.exec()
