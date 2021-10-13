from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QPushButton, QGroupBox, QComboBox, QPlainTextEdit, QCheckBox
from PyQt6.QtCore import QSize
from ...factory import list_algo, list_env, get_algo, get_env
from ...utils import ystring
from ..components.variable_item import variable_item
from ..components.objective_item import objective_item


class BadgerRoutinePage(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        if self.name is None:
            pass

        self.algos = algos = list_algo()
        self.envs = envs = list_env()

        # Set up the layout
        vbox = QVBoxLayout(self)

        # Action bar
        self.btn_back = btn_back = QPushButton('Back')
        btn_back.setFixedWidth(64)
        vbox.addWidget(btn_back)

        # Algo and env configs
        panel_int = QWidget()
        hbox_int = QHBoxLayout(panel_int)
        hbox_int.setContentsMargins(0, 0, 0, 0)

        group_algo = QGroupBox('Algorithm')
        vbox_algo = QVBoxLayout(group_algo)
        self.cb_algo = cb_algo = QComboBox()
        cb_algo.addItems(algos)
        cb_algo.setCurrentIndex(-1)
        vbox_algo.addWidget(cb_algo)
        self.edit_algo = edit_algo = QPlainTextEdit()
        edit_algo.setFixedHeight(128)
        vbox_algo.addWidget(edit_algo)
        hbox_int.addWidget(group_algo)

        group_env = QGroupBox('Environment')
        vbox_env = QVBoxLayout(group_env)
        self.cb_env = cb_env = QComboBox()
        cb_env.addItems(envs)
        cb_env.setCurrentIndex(-1)
        vbox_env.addWidget(cb_env)
        self.edit_env = edit_env = QPlainTextEdit()
        edit_env.setFixedHeight(128)
        vbox_env.addWidget(edit_env)
        hbox_int.addWidget(group_env)
        vbox.addWidget(panel_int)

        # Configs group
        group_ext = QGroupBox('Configs')
        hbox_ext = QHBoxLayout(group_ext)

        group_var = QGroupBox('Variables')
        vbox_var = QVBoxLayout(group_var)
        action_var = QWidget()
        hbox_action_var = QHBoxLayout(action_var)
        hbox_action_var.setContentsMargins(0, 0, 0, 0)
        self.btn_all_var = btn_all_var = QPushButton('Check All')
        self.btn_un_all_var = btn_un_all_var = QPushButton('Uncheck All')
        self.check_only_var = check_only_var = QCheckBox('Checked Only')
        check_only_var.setChecked(False)
        hbox_action_var.addWidget(btn_all_var)
        hbox_action_var.addWidget(btn_un_all_var)
        hbox_action_var.addStretch()
        hbox_action_var.addWidget(check_only_var)
        vbox_var.addWidget(action_var)
        self.list_var = list_var = QListWidget()
        self.dict_var = {}
        vbox_var.addWidget(list_var)
        hbox_ext.addWidget(group_var)

        group_obj = QGroupBox('Objectives')
        vbox_obj = QVBoxLayout(group_obj)
        action_obj = QWidget()
        hbox_action_obj = QHBoxLayout(action_obj)
        hbox_action_obj.setContentsMargins(0, 0, 0, 0)
        self.btn_all_obj = btn_all_obj = QPushButton('Check All')
        self.btn_un_all_obj = btn_un_all_obj = QPushButton('Uncheck All')
        self.check_only_obj = check_only_obj = QCheckBox('Checked Only')
        check_only_obj.setChecked(False)
        hbox_action_obj.addWidget(btn_all_obj)
        hbox_action_obj.addWidget(btn_un_all_obj)
        hbox_action_obj.addStretch()
        hbox_action_obj.addWidget(check_only_obj)
        vbox_obj.addWidget(action_obj)
        self.list_obj = list_obj = QListWidget()
        self.dict_obj = {}
        vbox_obj.addWidget(list_obj)
        hbox_ext.addWidget(group_obj)

        group_con = QGroupBox('Constraints')
        vbox_con = QVBoxLayout(group_con)
        self.list_con = list_con = QListWidget()
        self.dict_con = {}
        vbox_con.addWidget(list_con)
        hbox_ext.addWidget(group_con)

        vbox.addWidget(group_ext, 1)

    def config_logic(self):
        self.cb_algo.currentIndexChanged.connect(self.select_algo)
        self.cb_env.currentIndexChanged.connect(self.select_env)
        self.btn_all_var.clicked.connect(self.check_all_var)
        self.btn_un_all_var.clicked.connect(self.uncheck_all_var)
        self.btn_all_obj.clicked.connect(self.check_all_obj)
        self.btn_un_all_obj.clicked.connect(self.uncheck_all_obj)
        self.check_only_var.stateChanged.connect(self.toggle_check_only_var)
        self.check_only_obj.stateChanged.connect(self.toggle_check_only_obj)

    def select_algo(self, i):
        if i == -1:
            self.edit_algo.setPlainText('')
            return

        name = self.algos[i]
        _, configs = get_algo(name)
        self.edit_algo.setPlainText(ystring(configs['params']))

    def select_env(self, i):
        if i == -1:
            self.edit_env.setPlainText('')
            self.list_var.clear()
            self.dict_var.clear()
            self.list_obj.clear()
            self.dict_obj.clear()
            self.list_con.clear()
            self.dict_con.clear()
            return

        name = self.envs[i]
        _, configs = get_env(name)
        self.edit_env.setPlainText(ystring(configs['params']))

        self.list_var.clear()
        for var in configs['variables']:
            name = next(iter(var))
            vrange = var[name]
            item = QListWidgetItem(self.list_var)
            var_item = variable_item(name, vrange, self.toggle_var)
            item.setSizeHint(var_item.sizeHint())
            self.list_var.addItem(item)
            self.list_var.setItemWidget(item, var_item)
            self.dict_var[name] = item

        self.list_obj.clear()
        for obj in configs['observations']:
            item = QListWidgetItem(self.list_obj)
            obj_item = objective_item(obj, 0, self.toggle_obj)
            item.setSizeHint(obj_item.sizeHint())
            self.list_obj.addItem(item)
            self.list_obj.setItemWidget(item, obj_item)
            self.dict_obj[obj] = item

    def check_all_var(self):
        for i in range(self.list_var.count()):
            item = self.list_var.item(i)
            item_widget = self.list_var.itemWidget(item)
            item_widget.check_name.setChecked(True)

    def uncheck_all_var(self):
        for i in range(self.list_var.count()):
            item = self.list_var.item(i)
            item_widget = self.list_var.itemWidget(item)
            item_widget.check_name.setChecked(False)

    def check_all_obj(self):
        for i in range(self.list_obj.count()):
            item = self.list_obj.item(i)
            item_widget = self.list_obj.itemWidget(item)
            item_widget.check_name.setChecked(True)

    def uncheck_all_obj(self):
        for i in range(self.list_obj.count()):
            item = self.list_obj.item(i)
            item_widget = self.list_obj.itemWidget(item)
            item_widget.check_name.setChecked(False)

    def toggle_check_only_var(self):
        if self.check_only_var.isChecked():
            for i in range(self.list_var.count()):
                item = self.list_var.item(i)
                item_widget = self.list_var.itemWidget(item)
                if not item_widget.check_name.isChecked():
                    item_widget.hide()
                    item.setSizeHint(QSize(0, 0))
        else:
            for i in range(self.list_var.count()):
                item = self.list_var.item(i)
                item_widget = self.list_var.itemWidget(item)
                item_widget.show()
                item.setSizeHint(item_widget.sizeHint())

    def toggle_var(self, name):
        if self.check_only_var.isChecked():
            item = self.dict_var[name]
            item_widget = self.list_var.itemWidget(item)
            if item_widget.check_name.isChecked():
                item_widget.show()
                item.setSizeHint(item_widget.sizeHint())
            else:
                item_widget.hide()
                item.setSizeHint(QSize(0, 0))

    def toggle_check_only_obj(self):
        if self.check_only_obj.isChecked():
            for i in range(self.list_obj.count()):
                item = self.list_obj.item(i)
                item_widget = self.list_obj.itemWidget(item)
                if not item_widget.check_name.isChecked():
                    item_widget.hide()
                    item.setSizeHint(QSize(0, 0))
        else:
            for i in range(self.list_obj.count()):
                item = self.list_obj.item(i)
                item_widget = self.list_obj.itemWidget(item)
                item_widget.show()
                item.setSizeHint(item_widget.sizeHint())

    def toggle_obj(self, name):
        if self.check_only_obj.isChecked():
            item = self.dict_obj[name]
            item_widget = self.list_obj.itemWidget(item)
            if item_widget.check_name.isChecked():
                item_widget.show()
                item.setSizeHint(item_widget.sizeHint())
            else:
                item_widget.hide()
                item.setSizeHint(QSize(0, 0))
