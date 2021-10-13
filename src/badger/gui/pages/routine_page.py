from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QPushButton, QGroupBox, QComboBox, QPlainTextEdit
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
        self.list_var = list_var = QListWidget()
        vbox_var.addWidget(list_var)
        hbox_ext.addWidget(group_var)

        group_obj = QGroupBox('Objectives')
        vbox_obj = QVBoxLayout(group_obj)
        self.list_obj = list_obj = QListWidget()
        vbox_obj.addWidget(list_obj)
        hbox_ext.addWidget(group_obj)

        group_con = QGroupBox('Constraints')
        vbox_con = QVBoxLayout(group_con)
        self.list_con = list_con = QListWidget()
        vbox_con.addWidget(list_con)
        hbox_ext.addWidget(group_con)

        vbox.addWidget(group_ext)

        vbox.addStretch()

    def config_logic(self):
        self.cb_algo.currentIndexChanged.connect(self.select_algo)
        self.cb_env.currentIndexChanged.connect(self.select_env)

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
            self.list_obj.clear()
            self.list_con.clear()
            return

        name = self.envs[i]
        _, configs = get_env(name)
        self.edit_env.setPlainText(ystring(configs['params']))

        self.list_var.clear()
        for var in configs['variables']:
            name = next(iter(var))
            vrange = var[name]
            item = QListWidgetItem(self.list_var)
            var_item = variable_item(name, vrange)
            item.setSizeHint(var_item.sizeHint())
            self.list_var.addItem(item)
            self.list_var.setItemWidget(item, var_item)

        self.list_obj.clear()
        for obj in configs['observations']:
            item = QListWidgetItem(self.list_obj)
            obj_item = objective_item(obj, 0)
            item.setSizeHint(obj_item.sizeHint())
            self.list_obj.addItem(item)
            self.list_obj.setItemWidget(item, obj_item)
