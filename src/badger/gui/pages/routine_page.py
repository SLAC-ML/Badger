from PyQt5.QtWidgets import QLineEdit, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QGroupBox, QComboBox, QLineEdit, QPlainTextEdit, QCheckBox
from PyQt5.QtWidgets import QMessageBox, QStyledItemDelegate
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from coolname import generate_slug
from ...factory import list_algo, list_env, get_algo, get_env
from ...utils import ystring, load_config, config_list_to_dict, normalize_routine
from ..components.variable_item import variable_item
from ..components.objective_item import objective_item
from ..windows.review_dialog import BadgerReviewDialog
from ..windows.opt_monitor import BadgerOptMonitor


class BadgerRoutinePage(QWidget):
    def __init__(self, go_home=None):
        super().__init__()

        self.go_home = go_home

        self.algos = list_algo()
        self.envs = list_env()

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        # Set up the layout
        vbox = QVBoxLayout(self)

        # Algo and env configs
        panel_int = QWidget()
        hbox_int = QHBoxLayout(panel_int)
        hbox_int.setContentsMargins(0, 0, 0, 0)

        group_algo = QGroupBox('Algorithm')
        vbox_algo = QVBoxLayout(group_algo)
        self.cb_algo = cb_algo = QComboBox()
        cb_algo.setItemDelegate(QStyledItemDelegate())
        cb_algo.addItems(self.algos)
        cb_algo.setCurrentIndex(-1)
        vbox_algo.addWidget(cb_algo)
        self.edit_algo = edit_algo = QPlainTextEdit()
        edit_algo.setFixedHeight(128)
        vbox_algo.addWidget(edit_algo)
        hbox_int.addWidget(group_algo)

        group_env = QGroupBox('Environment')
        vbox_env = QVBoxLayout(group_env)
        self.cb_env = cb_env = QComboBox()
        cb_env.setItemDelegate(QStyledItemDelegate())
        cb_env.addItems(self.envs)
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
        btn_all_var.setFixedSize(96, 24)
        btn_un_all_var.setFixedSize(96, 24)
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
        btn_all_obj.setFixedSize(96, 24)
        btn_un_all_obj.setFixedSize(96, 24)
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

        # Misc group
        group_misc = QGroupBox('Misc')
        hbox_misc = QHBoxLayout(group_misc)
        self.check_save = check_save = QCheckBox('Save as')
        check_save.setChecked(False)
        self.edit_save = edit_save = QLineEdit()
        edit_save.setPlaceholderText(generate_slug(2))
        edit_save.setDisabled(True)
        hbox_misc.addWidget(check_save)
        hbox_misc.addWidget(edit_save, 1)
        hbox_misc.addStretch(2)

        vbox.addWidget(group_misc)

        # Action bar
        action_bar = QWidget()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)
        self.btn_back = btn_back = QPushButton('Back')
        self.btn_review = btn_review = QPushButton('Review')
        self.btn_run = btn_run = QPushButton('Run Routine')

        cool_font = QFont()
        cool_font.setWeight(QFont.DemiBold)
        # cool_font.setPixelSize(16)

        btn_back.setFixedSize(64, 64)
        btn_back.setFont(cool_font)
        btn_review.setFixedSize(64, 64)
        btn_review.setFont(cool_font)
        btn_run.setFixedSize(256, 64)
        btn_run.setFont(cool_font)
        hbox_action.addWidget(btn_back)
        hbox_action.addWidget(btn_review)
        hbox_action.addStretch(1)
        hbox_action.addWidget(btn_run)

        # vbox.addSpacing(16)
        vbox.addWidget(action_bar)

    def config_logic(self):
        self.btn_back.clicked.connect(self.go_home)
        self.cb_algo.currentIndexChanged.connect(self.select_algo)
        self.cb_env.currentIndexChanged.connect(self.select_env)
        self.btn_all_var.clicked.connect(self.check_all_var)
        self.btn_un_all_var.clicked.connect(self.uncheck_all_var)
        self.btn_all_obj.clicked.connect(self.check_all_obj)
        self.btn_un_all_obj.clicked.connect(self.uncheck_all_obj)
        self.check_only_var.stateChanged.connect(self.toggle_check_only_var)
        self.check_only_obj.stateChanged.connect(self.toggle_check_only_obj)
        self.check_save.stateChanged.connect(self.toggle_save)
        self.btn_review.clicked.connect(self.review)
        self.btn_run.clicked.connect(self.run)

    def refresh_ui(self, routine):
        self.algos = list_algo()
        self.envs = list_env()

        if routine is None:
            # Reset the algo and env configs
            self.cb_algo.setCurrentIndex(-1)
            self.cb_env.setCurrentIndex(-1)

            # Reset the routine configs check box status
            self.check_only_var.setChecked(False)
            self.check_only_obj.setChecked(False)

            # Reset the save settings
            name = generate_slug(2)
            self.edit_save.setText('')
            self.edit_save.setPlaceholderText(name)
            self.check_save.setChecked(False)

            return

        # Fill in the algo and env configs
        name_algo = routine['algo']
        idx_algo = self.algos.index(name_algo)
        self.cb_algo.setCurrentIndex(idx_algo)
        self.edit_algo.setPlainText(ystring(routine['algo_params']))

        name_env = routine['env']
        idx_env = self.envs.index(name_env)
        self.cb_env.setCurrentIndex(idx_env)
        self.edit_env.setPlainText(ystring(routine['env_params']))

        # Config the vocs panel
        self.check_only_var.setChecked(True)
        variables = [next(iter(v)) for v in routine['config']['variables']]
        for i in range(self.list_var.count()):
            item = self.list_var.item(i)
            item_widget = self.list_var.itemWidget(item)
            var_name = item_widget.check_name.text()
            try:
                idx = variables.index(var_name)
                vrange = routine['config']['variables'][idx][var_name]
                item_widget.sb_lower.sb.setValue(vrange[0])
                item_widget.sb_upper.sb.setValue(vrange[1])
                item_widget.check_name.setChecked(True)
            except ValueError:
                item_widget.check_name.setChecked(False)

        self.check_only_obj.setChecked(True)
        objectives = [next(iter(v)) for v in routine['config']['objectives']]
        for i in range(self.list_obj.count()):
            item = self.list_obj.item(i)
            item_widget = self.list_obj.itemWidget(item)
            obj_name = item_widget.check_name.text()
            try:
                idx = objectives.index(obj_name)
                rule = routine['config']['objectives'][idx][obj_name]
                idx_rule = 0 if rule == 'MINIMIZE' else 1
                item_widget.cb_rule.setCurrentIndex(idx_rule)
                item_widget.check_name.setChecked(True)
            except ValueError:
                item_widget.check_name.setChecked(False)

        # Config the save settings
        name = routine['name']
        self.edit_save.setPlaceholderText(generate_slug(2))
        self.edit_save.setText(name)
        self.check_save.setChecked(False)

    def select_algo(self, i):
        if i == -1:
            self.edit_algo.setPlainText('')
            return

        name = self.algos[i]
        try:
            _, configs = get_algo(name)
            self.edit_algo.setPlainText(ystring(configs['params']))
        except Exception as e:
            self.cb_algo.setCurrentIndex(-1)
            return QMessageBox.critical(self, 'Error!', str(e))

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
        try:
            _, configs = get_env(name)
        except Exception as e:
            self.cb_env.setCurrentIndex(-1)
            return QMessageBox.critical(self, 'Error!', str(e))

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

    def toggle_save(self):
        if self.check_save.isChecked():
            self.edit_save.setDisabled(False)
        else:
            self.edit_save.setDisabled(True)

    def _compose_routine(self):
        # Compose the routine
        name = self.edit_save.text() or self.edit_save.placeholderText()
        algo = self.cb_algo.currentText()
        env = self.cb_env.currentText()
        algo_params = load_config(self.edit_algo.toPlainText())
        env_params = load_config(self.edit_env.toPlainText())

        variables = []
        for i in range(self.list_var.count()):
            item = self.list_var.item(i)
            item_widget = self.list_var.itemWidget(item)
            if item_widget.check_name.isChecked():
                var_name = item_widget.check_name.text()
                lb = item_widget.sb_lower.sb.value()
                ub = item_widget.sb_upper.sb.value()
                _dict = {}
                _dict[var_name] = [lb, ub]
                variables.append(_dict)

        objectives = []
        for i in range(self.list_obj.count()):
            item = self.list_obj.item(i)
            item_widget = self.list_obj.itemWidget(item)
            if item_widget.check_name.isChecked():
                obj_name = item_widget.check_name.text()
                rule = item_widget.cb_rule.currentText()
                _dict = {}
                _dict[obj_name] = rule
                objectives.append(_dict)

        configs = {
            'variables': variables,
            'objectives': objectives,
            'constraints': None,
        }

        routine = {
            'name': name,
            'algo': algo,
            'env': env,
            'algo_params': algo_params,
            'env_params': env_params,
            'env_vranges': config_list_to_dict(variables),
            'config': configs,
        }

        # Sanity check and config normalization
        try:
            routine = normalize_routine(routine)
        except Exception as e:
            raise e

        return routine

    def review(self):
        try:
            routine = self._compose_routine()
        except Exception as e:
            return QMessageBox.critical(self, 'Error!', str(e))

        dlg = BadgerReviewDialog(self, routine)
        dlg.exec()

    def run_routine(self, routine, save):
        self.monitor = BadgerOptMonitor(self, routine, save)
        self.monitor.show()
        self.monitor.start()

    def run(self):
        try:
            routine = self._compose_routine()
        except Exception as e:
            return QMessageBox.critical(self, 'Error!', str(e))

        save = self.check_save.isChecked()

        try:
            self.run_routine(routine, save)
        except Exception as e:
            # raise e
            QMessageBox.critical(self, 'Error!', str(e))
