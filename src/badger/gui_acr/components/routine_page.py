from PyQt5.QtWidgets import QLineEdit, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QGroupBox, QComboBox, QLineEdit, QPlainTextEdit, QCheckBox
from PyQt5.QtWidgets import QMessageBox, QStyledItemDelegate, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from coolname import generate_slug
from pytest import param
from ...factory import list_algo, list_env, get_algo, get_env
from ...utils import ystring, load_config, config_list_to_dict, normalize_routine, instantiate_env
from .variable_item import variable_item
from .objective_item import objective_item
from .constraint_item import constraint_item
from .algo_cbox import BadgerAlgoBox
from ..windows.review_dialog import BadgerReviewDialog
from ..windows.var_dialog import BadgerVariableDialog
from ..windows.edit_script_dialog import BadgerEditScriptDialog


CONS_RELATION_DICT = {
    '>': 'GREATER_THAN',
    '<': 'LESS_THAN',
    '=': 'EQUAL_TO',
}


class BadgerRoutinePage(QWidget):
    def __init__(self):
        super().__init__()

        self.algos = list_algo()
        self.envs = list_env()
        self.env = None
        self.routine = None
        self.script = ''

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        # Set up the layout
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(11, 11, 19, 11)

        # Algo and env configs
        panel_int = QWidget()
        vbox_int = QVBoxLayout(panel_int)
        vbox_int.setContentsMargins(0, 0, 0, 0)

        self.algo_box = BadgerAlgoBox(self.algos)
        vbox_int.addWidget(self.algo_box)

        group_env = QGroupBox('Environment')
        vbox_env = QVBoxLayout(group_env)
        action_env = QWidget()
        hbox_action_env = QHBoxLayout(action_env)
        hbox_action_env.setContentsMargins(0, 0, 0, 0)
        self.cb_env = cb_env = QComboBox()
        cb_env.setItemDelegate(QStyledItemDelegate())
        cb_env.addItems(self.envs)
        cb_env.setCurrentIndex(-1)
        self.btn_env_play = btn_env_play = QPushButton('Playground')
        btn_env_play.setFixedSize(96, 24)
        btn_env_play.hide()  # hide for now to prevent confusions
        hbox_action_env.addWidget(cb_env, 1)
        hbox_action_env.addWidget(btn_env_play)
        vbox_env.addWidget(action_env)
        self.edit_env = edit_env = QPlainTextEdit()
        edit_env.setFixedHeight(128)
        vbox_env.addWidget(edit_env)
        vbox_int.addWidget(group_env)
        vbox.addWidget(panel_int)

        # Configs group
        group_ext = QGroupBox('Configs')
        vbox_ext = QVBoxLayout(group_ext)

        group_var = QGroupBox('Variables')
        vbox_var = QVBoxLayout(group_var)
        action_var = QWidget()
        hbox_action_var = QHBoxLayout(action_var)
        hbox_action_var.setContentsMargins(0, 0, 0, 0)
        self.btn_all_var = btn_all_var = QPushButton('Check All')
        self.btn_un_all_var = btn_un_all_var = QPushButton('Uncheck All')
        btn_all_var.setFixedSize(96, 24)
        btn_un_all_var.setFixedSize(96, 24)
        self.btn_add_var = btn_add_var = QPushButton('Add')
        btn_add_var.setFixedSize(96, 24)
        btn_add_var.setDisabled(True)
        self.check_only_var = check_only_var = QCheckBox('Checked Only')
        check_only_var.setChecked(False)
        hbox_action_var.addWidget(btn_all_var)
        hbox_action_var.addWidget(btn_un_all_var)
        hbox_action_var.addWidget(btn_add_var)
        hbox_action_var.addStretch()
        hbox_action_var.addWidget(check_only_var)
        vbox_var.addWidget(action_var)
        self.list_var = list_var = QListWidget()
        self.dict_var = {}
        vbox_var.addWidget(list_var)
        vbox_ext.addWidget(group_var)

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
        vbox_ext.addWidget(group_obj)

        group_con = QGroupBox('Constraints')
        vbox_con = QVBoxLayout(group_con)
        action_con = QWidget()
        hbox_action_con = QHBoxLayout(action_con)
        hbox_action_con.setContentsMargins(0, 0, 0, 0)
        self.btn_add_con = btn_add_con = QPushButton('Add')
        btn_add_con.setFixedSize(96, 24)
        btn_add_con.setDisabled(True)
        hbox_action_con.addWidget(btn_add_con)
        hbox_action_con.addStretch()
        vbox_con.addWidget(action_con)
        self.list_con = list_con = QListWidget()
        self.dict_con = {}
        vbox_con.addWidget(list_con)
        vbox_ext.addWidget(group_con)

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

    def config_logic(self):
        self.algo_box.cb.currentIndexChanged.connect(self.select_algo)
        self.algo_box.check_use_script.stateChanged.connect(self.toggle_use_script)
        self.algo_box.btn_edit_script.clicked.connect(self.edit_script)
        self.cb_env.currentIndexChanged.connect(self.select_env)
        self.btn_env_play.clicked.connect(self.open_playground)
        self.btn_all_var.clicked.connect(self.check_all_var)
        self.btn_un_all_var.clicked.connect(self.uncheck_all_var)
        self.btn_add_var.clicked.connect(self.add_var)
        self.btn_all_obj.clicked.connect(self.check_all_obj)
        self.btn_un_all_obj.clicked.connect(self.uncheck_all_obj)
        self.check_only_var.stateChanged.connect(self.toggle_check_only_var)
        self.check_only_obj.stateChanged.connect(self.toggle_check_only_obj)
        self.btn_add_con.clicked.connect(self.add_constraint)
        self.check_save.stateChanged.connect(self.toggle_save)

    def refresh_ui(self, routine):
        self.routine = routine  # save routine for future reference

        self.algos = list_algo()
        self.envs = list_env()
        # Clean up the constraints list
        self.list_con.clear()

        if routine is None:
            # Reset the algo and env configs
            self.algo_box.cb.setCurrentIndex(-1)
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
        self.algo_box.cb.setCurrentIndex(idx_algo)
        self.algo_box.edit.setPlainText(ystring(routine['algo_params']))
        try:
            self.script = routine['config']['script']
        except KeyError:
            self.script = None

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

        if routine['config']['constraints'] is not None:
            for i in range(len(routine['config']['constraints'])):
                name = next(iter(routine['config']['constraints'][i]))
                relation, thres = routine['config']['constraints'][i][name][:2]
                try:
                    routine['config']['constraints'][i][name][2]
                    critical = True
                except:
                    critical = False
                relation = ['GREATER_THAN', 'LESS_THAN',
                            'EQUAL_TO'].index(relation)
                self.add_constraint(name, relation, thres, critical)

        # Config the save settings
        name = routine['name']
        self.edit_save.setPlaceholderText(generate_slug(2))
        self.edit_save.setText(name)
        self.check_save.setChecked(False)

        if self.script:
            self.algo_box.check_use_script.setChecked(True)

    def select_algo(self, i):
        # Reset the script
        self.script = ''
        self.algo_box.check_use_script.setChecked(False)

        if i == -1:
            self.algo_box.edit.setPlainText('')
            return

        name = self.algos[i]
        try:
            _, configs = get_algo(name)
            self.algo_box.edit.setPlainText(ystring(configs['params']))
        except Exception as e:
            self.algo_box.cb.setCurrentIndex(-1)
            return QMessageBox.critical(self, 'Error!', str(e))

    def toggle_use_script(self):
        if self.algo_box.check_use_script.isChecked():
            self.algo_box.btn_edit_script.show()
            self.algo_box.edit.setReadOnly(True)
            self.refresh_params_algo()
        else:
            self.algo_box.btn_edit_script.hide()
            self.algo_box.edit.setReadOnly(False)

    def edit_script(self):
        algo = self.algo_box.cb.currentText()
        dlg = BadgerEditScriptDialog(self, algo, self.script, self.script_updated)
        dlg.exec()

    def script_updated(self, text):
        self.script = text
        self.refresh_params_algo()

    def refresh_params_algo(self):
        if not self.script:
            return

        try:
            tmp = {}
            exec(self.script, tmp)
            try:
                tmp['generate']  # test if generate function is defined
            except Exception as e:
                QMessageBox.warning(self, 'Please define a valid generate function!', str(e))
                return

            env_params = load_config(self.edit_env.toPlainText())
            try:
                intf_name = self.configs['interface'][0]
            except KeyError:
                intf_name = None
            configs = {
                'params': env_params,
                'interface': [intf_name]
            }
            env = instantiate_env(self.env, configs)
            # Function generate comes from the script
            params_algo = tmp['generate'](env, None)
            self.algo_box.edit.setPlainText(ystring(params_algo))
        except Exception as e:
            QMessageBox.warning(self, 'Invalid script!', str(e))

    def select_env(self, i):
        if i == -1:
            self.edit_env.setPlainText('')
            self.list_var.clear()
            self.dict_var.clear()
            self.list_obj.clear()
            self.dict_obj.clear()
            self.configs = None
            self.env = None
            self.btn_add_con.setDisabled(True)
            self.btn_add_var.setDisabled(True)
            self.routine = None
            return

        name = self.envs[i]
        try:
            env, configs = get_env(name)
            self.configs = configs
            self.env = env
            self.btn_add_con.setDisabled(False)
            self.btn_add_var.setDisabled(False)
            if self.algo_box.check_use_script.isChecked():
                self.refresh_params_algo()
        except Exception as e:
            self.configs = None
            self.env = None
            self.cb_env.setCurrentIndex(-1)
            self.btn_add_con.setDisabled(True)
            self.btn_add_var.setDisabled(True)
            self.routine = None
            return QMessageBox.critical(self, 'Error!', str(e))

        self.edit_env.setPlainText(ystring(configs['params']))

        self.list_var.clear()
        vars_env = configs['variables']
        vars_combine = [*vars_env]
        if self.routine:  # check for the temp variables in vocs
            vars_vocs = self.routine['config']['variables']
            var_names_vocs = [next(iter(var)) for var in vars_vocs]
            var_names_env = [next(iter(var)) for var in vars_env]
            env_instance = instantiate_env(env, configs)
            for name in var_names_vocs:
                if name in var_names_env:
                    continue

                _var = {}
                _var[name] = env_instance._get_vrange(name)
                vars_combine.append(_var)
        for var in vars_combine:
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

        self.list_con.clear()
        self.routine = None

    def open_playground(self):
        pass

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

    def add_var(self):
        # TODO: Use a cached env
        env_params = load_config(self.edit_env.toPlainText())
        try:
            intf_name = self.configs['interface'][0]
        except KeyError:
            intf_name = None
        configs = {
            'params': env_params,
            'interface': [intf_name]
        }

        dlg = BadgerVariableDialog(self, self.env, configs, self.add_var_to_list)
        dlg.exec()

    def add_var_to_list(self, name, min, max):
        # Check if already in the list
        ok = False
        try:
            self.dict_var[name]
        except:
            ok = True

        if not ok:
            QMessageBox.warning(self, 'Variable already exists!', f'Variable {name} already exists!')
            return 1

        item = QListWidgetItem(self.list_var)
        var_item = variable_item(name, [min, max], self.toggle_var)
        var_item.check_name.setChecked(True)
        item.setSizeHint(var_item.sizeHint())
        self.list_var.addItem(item)
        self.list_var.setItemWidget(item, var_item)
        self.dict_var[name] = item

        return 0

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

    def add_constraint(self, name=None, relation=0, threshold=0, critical=False):
        if self.configs is None:
            return

        options = self.configs['observations']
        item = QListWidgetItem(self.list_con)
        con_item = constraint_item(options,
                                   lambda: self.list_con.takeItem(
                                       self.list_con.row(item)),
                                   name, relation, threshold, critical)
        item.setSizeHint(con_item.sizeHint())
        self.list_con.addItem(item)
        self.list_con.setItemWidget(item, con_item)
        # self.dict_con[''] = item

    def _compose_routine(self):
        # Compose the routine
        name = self.edit_save.text() or self.edit_save.placeholderText()
        algo = self.algo_box.cb.currentText()
        env = self.cb_env.currentText()
        algo_params = load_config(self.algo_box.edit.toPlainText())
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

        constraints = []
        for i in range(self.list_con.count()):
            item = self.list_con.item(i)
            item_widget = self.list_con.itemWidget(item)
            critical = item_widget.check_crit.isChecked()
            con_name = item_widget.cb_obs.currentText()
            relation = CONS_RELATION_DICT[item_widget.cb_rel.currentText()]
            value = item_widget.sb.value()
            _dict = {}
            _dict[con_name] = [relation, value]
            if critical:
                _dict[con_name].append('CRITICAL')
            constraints.append(_dict)

        configs = {
            'variables': variables,
            'objectives': objectives,
            'constraints': constraints,
        }
        if self.algo_box.check_use_script.isChecked():
            configs['script'] = self.script

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