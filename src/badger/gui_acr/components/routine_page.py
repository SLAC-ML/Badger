from PyQt5.QtWidgets import QLineEdit, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import QSize
import sqlite3
from coolname import generate_slug
from ...factory import list_algo, list_env, get_algo, get_env
from ...utils import ystring, load_config, config_list_to_dict
from ...core import normalize_routine, instantiate_env, list_scaling_func, get_scaling_default_params
from ...db import save_routine, remove_routine
from .variable_item import variable_item
from .objective_item import objective_item
from .constraint_item import constraint_item
from .state_item import state_item
from .algo_cbox import BadgerAlgoBox
from .env_cbox import BadgerEnvBox
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
        self.scaling_functions = list_scaling_func()

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        # Set up the layout
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(11, 11, 19, 11)

        # Meta group
        group_meta = QGroupBox('Metadata')
        hbox_meta = QHBoxLayout(group_meta)
        label_name = QLabel('Routine Name')
        self.edit_save = edit_save = QLineEdit()
        edit_save.setPlaceholderText(generate_slug(2))
        hbox_meta.addWidget(label_name)
        hbox_meta.addWidget(edit_save, 1)
        # hbox_meta.addStretch(2)
        vbox.addWidget(group_meta)

        # Algo box
        self.algo_box = BadgerAlgoBox(self.algos, self.scaling_functions)
        self.algo_box.expand()  # expand the box initially
        vbox.addWidget(self.algo_box)

        # Env box
        self.env_box = BadgerEnvBox(self.envs)
        self.env_box.expand()  # expand the box initially
        vbox.addWidget(self.env_box)

        vbox.addStretch()

    def config_logic(self):
        self.algo_box.cb.currentIndexChanged.connect(self.select_algo)
        self.algo_box.check_use_script.stateChanged.connect(self.toggle_use_script)
        self.algo_box.btn_edit_script.clicked.connect(self.edit_script)
        self.algo_box.cb_scaling.currentIndexChanged.connect(self.select_scaling_func)
        self.env_box.cb.currentIndexChanged.connect(self.select_env)
        self.env_box.btn_env_play.clicked.connect(self.open_playground)
        self.env_box.btn_all_var.clicked.connect(self.check_all_var)
        self.env_box.btn_un_all_var.clicked.connect(self.uncheck_all_var)
        self.env_box.btn_add_var.clicked.connect(self.add_var)
        self.env_box.btn_all_obj.clicked.connect(self.check_all_obj)
        self.env_box.btn_un_all_obj.clicked.connect(self.uncheck_all_obj)
        self.env_box.check_only_var.stateChanged.connect(self.toggle_check_only_var)
        self.env_box.check_only_obj.stateChanged.connect(self.toggle_check_only_obj)
        self.env_box.btn_add_con.clicked.connect(self.add_constraint)
        self.env_box.btn_add_sta.clicked.connect(self.add_state)

    def refresh_ui(self, routine):
        self.routine = routine  # save routine for future reference

        self.algos = list_algo()
        self.envs = list_env()
        # Clean up the constraints/states list
        self.env_box.list_con.clear()
        self.env_box.list_sta.clear()

        if routine is None:
            # Reset the algo and env configs
            self.algo_box.cb.setCurrentIndex(-1)
            self.env_box.cb.setCurrentIndex(-1)

            # Reset the routine configs check box status
            self.env_box.check_only_var.setChecked(False)
            self.env_box.check_only_obj.setChecked(False)

            # Reset the save settings
            name = generate_slug(2)
            self.edit_save.setText('')
            self.edit_save.setPlaceholderText(name)

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
        try:
            name_scaling = routine['config']['domain_scaling']['func']
            params_scaling = routine['config']['domain_scaling'].copy()
            del params_scaling['func']
        except:
            name_scaling = None
            params_scaling = None
        try:
            idx_scaling = self.scaling_functions.index(name_scaling)
        except ValueError:
            idx_scaling = -1
        self.algo_box.cb_scaling.setCurrentIndex(idx_scaling)
        self.algo_box.edit_scaling.setPlainText(ystring(params_scaling))

        name_env = routine['env']
        idx_env = self.envs.index(name_env)
        self.env_box.cb.setCurrentIndex(idx_env)
        self.env_box.edit.setPlainText(ystring(routine['env_params']))

        # Config the vocs panel
        self.env_box.check_only_var.setChecked(True)
        variables = [next(iter(v)) for v in routine['config']['variables']]
        for i in range(self.env_box.list_var.count()):
            item = self.env_box.list_var.item(i)
            item_widget = self.env_box.list_var.itemWidget(item)
            var_name = item_widget.check_name.text()
            try:
                idx = variables.index(var_name)
                vrange = routine['config']['variables'][idx][var_name]
                item_widget.sb_lower.sb.setValue(vrange[0])
                item_widget.sb_upper.sb.setValue(vrange[1])
                item_widget.check_name.setChecked(True)
            except ValueError:
                item_widget.check_name.setChecked(False)

        self.env_box.check_only_obj.setChecked(True)
        objectives = [next(iter(v)) for v in routine['config']['objectives']]
        for i in range(self.env_box.list_obj.count()):
            item = self.env_box.list_obj.item(i)
            item_widget = self.env_box.list_obj.itemWidget(item)
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

        try:
            config_states = routine['config']['states']
        except KeyError:
            config_states = None
        if config_states is not None:
            for name_sta in config_states:
                self.add_state(name_sta)

        # Config the save settings
        name = routine['name']
        self.edit_save.setPlaceholderText(generate_slug(2))
        self.edit_save.setText(name)

        self.algo_box.check_use_script.setChecked(not not self.script)

    def select_algo(self, i):
        # Reset the script
        self.script = ''
        self.algo_box.check_use_script.setChecked(False)

        if i == -1:
            self.algo_box.edit.setPlainText('')
            self.algo_box.cb_scaling.setCurrentIndex(-1)
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

            env_params = load_config(self.env_box.edit.toPlainText())
            try:
                intf_name = self.configs['interface'][0]
            except KeyError:
                intf_name = None
            configs = {
                'params': env_params,
                'interface': [intf_name]
            }
            env = instantiate_env(self.env, configs)
            # Get vocs
            try:
                vocs = self._compose_vocs()
            except Exception:
                vocs = None
            # Function generate comes from the script
            params_algo = tmp['generate'](env, vocs)
            self.algo_box.edit.setPlainText(ystring(params_algo))
        except Exception as e:
            QMessageBox.warning(self, 'Invalid script!', str(e))

    def select_scaling_func(self, i):
        if i == -1:
            self.algo_box.edit_scaling.setPlainText('')
            return

        try:
            name = self.scaling_functions[i]
            default_params = get_scaling_default_params(name)
            self.algo_box.edit_scaling.setPlainText(ystring(default_params))
        except Exception as e:
            self.algo_box.cb.setCurrentIndex(-1)
            return QMessageBox.critical(self, 'Error!', str(e))

    def select_env(self, i):
        if i == -1:
            self.env_box.edit.setPlainText('')
            self.env_box.list_var.clear()
            self.env_box.dict_var.clear()
            self.env_box.list_obj.clear()
            self.env_box.dict_obj.clear()
            self.configs = None
            self.env = None
            self.env_box.btn_add_con.setDisabled(True)
            self.env_box.btn_add_sta.setDisabled(True)
            self.env_box.btn_add_var.setDisabled(True)
            self.routine = None
            return

        name = self.envs[i]
        try:
            env, configs = get_env(name)
            self.configs = configs
            self.env = env
            self.env_box.btn_add_con.setDisabled(False)
            self.env_box.btn_add_sta.setDisabled(False)
            self.env_box.btn_add_var.setDisabled(False)
            if self.algo_box.check_use_script.isChecked():
                self.refresh_params_algo()
        except Exception as e:
            self.configs = None
            self.env = None
            self.env_box.cb.setCurrentIndex(-1)
            self.env_box.btn_add_con.setDisabled(True)
            self.env_box.btn_add_sta.setDisabled(True)
            self.env_box.btn_add_var.setDisabled(True)
            self.routine = None
            return QMessageBox.critical(self, 'Error!', str(e))

        self.env_box.edit.setPlainText(ystring(configs['params']))

        self.env_box.list_var.clear()
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
            item = QListWidgetItem(self.env_box.list_var)
            var_item = variable_item(name, vrange, self.toggle_var)
            item.setSizeHint(var_item.sizeHint())
            self.env_box.list_var.addItem(item)
            self.env_box.list_var.setItemWidget(item, var_item)
            self.env_box.dict_var[name] = item

        self.env_box.list_obj.clear()
        for obj in configs['observations']:
            item = QListWidgetItem(self.env_box.list_obj)
            obj_item = objective_item(obj, 0, self.toggle_obj)
            item.setSizeHint(obj_item.sizeHint())
            self.env_box.list_obj.addItem(item)
            self.env_box.list_obj.setItemWidget(item, obj_item)
            self.env_box.dict_obj[obj] = item

        self.env_box.list_con.clear()
        self.env_box.list_sta.clear()
        self.env_box.fit_content()
        self.routine = None

    def open_playground(self):
        pass

    def check_all_var(self):
        for i in range(self.env_box.list_var.count()):
            item = self.env_box.list_var.item(i)
            item_widget = self.env_box.list_var.itemWidget(item)
            item_widget.check_name.setChecked(True)

    def uncheck_all_var(self):
        for i in range(self.env_box.list_var.count()):
            item = self.env_box.list_var.item(i)
            item_widget = self.env_box.list_var.itemWidget(item)
            item_widget.check_name.setChecked(False)

    def add_var(self):
        # TODO: Use a cached env
        env_params = load_config(self.env_box.edit.toPlainText())
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
            self.env_box.dict_var[name]
        except:
            ok = True

        if not ok:
            QMessageBox.warning(self, 'Variable already exists!', f'Variable {name} already exists!')
            return 1

        item = QListWidgetItem(self.env_box.list_var)
        var_item = variable_item(name, [min, max], self.toggle_var)
        var_item.check_name.setChecked(True)
        item.setSizeHint(var_item.sizeHint())
        self.env_box.list_var.addItem(item)
        self.env_box.list_var.setItemWidget(item, var_item)
        self.env_box.dict_var[name] = item
        self.env_box.fit_content()

        return 0

    def check_all_obj(self):
        for i in range(self.env_box.list_obj.count()):
            item = self.env_box.list_obj.item(i)
            item_widget = self.env_box.list_obj.itemWidget(item)
            item_widget.check_name.setChecked(True)

    def uncheck_all_obj(self):
        for i in range(self.env_box.list_obj.count()):
            item = self.env_box.list_obj.item(i)
            item_widget = self.env_box.list_obj.itemWidget(item)
            item_widget.check_name.setChecked(False)

    def toggle_check_only_var(self):
        if self.env_box.check_only_var.isChecked():
            for i in range(self.env_box.list_var.count()):
                item = self.env_box.list_var.item(i)
                item_widget = self.env_box.list_var.itemWidget(item)
                if not item_widget.check_name.isChecked():
                    item_widget.hide()
                    item.setSizeHint(QSize(0, 0))
        else:
            for i in range(self.env_box.list_var.count()):
                item = self.env_box.list_var.item(i)
                item_widget = self.env_box.list_var.itemWidget(item)
                item_widget.show()
                item.setSizeHint(item_widget.sizeHint())
        self.env_box.fit_content()

    def toggle_var(self, name):
        if self.env_box.check_only_var.isChecked():
            item = self.env_box.dict_var[name]
            item_widget = self.env_box.list_var.itemWidget(item)
            if item_widget.check_name.isChecked():
                item_widget.show()
                item.setSizeHint(item_widget.sizeHint())
            else:
                item_widget.hide()
                item.setSizeHint(QSize(0, 0))
            self.env_box.fit_content()

    def toggle_check_only_obj(self):
        if self.env_box.check_only_obj.isChecked():
            for i in range(self.env_box.list_obj.count()):
                item = self.env_box.list_obj.item(i)
                item_widget = self.env_box.list_obj.itemWidget(item)
                if not item_widget.check_name.isChecked():
                    item_widget.hide()
                    item.setSizeHint(QSize(0, 0))
        else:
            for i in range(self.env_box.list_obj.count()):
                item = self.env_box.list_obj.item(i)
                item_widget = self.env_box.list_obj.itemWidget(item)
                item_widget.show()
                item.setSizeHint(item_widget.sizeHint())
        self.env_box.fit_content()

    def toggle_obj(self, name):
        if self.env_box.check_only_obj.isChecked():
            item = self.env_box.dict_obj[name]
            item_widget = self.env_box.list_obj.itemWidget(item)
            if item_widget.check_name.isChecked():
                item_widget.show()
                item.setSizeHint(item_widget.sizeHint())
            else:
                item_widget.hide()
                item.setSizeHint(QSize(0, 0))
            self.env_box.fit_content()

    def add_constraint(self, name=None, relation=0, threshold=0, critical=False):
        if self.configs is None:
            return

        options = self.configs['observations']
        item = QListWidgetItem(self.env_box.list_con)
        con_item = constraint_item(options,
                                   lambda: self.env_box.list_con.takeItem(
                                       self.env_box.list_con.row(item)),
                                   name, relation, threshold, critical)
        item.setSizeHint(con_item.sizeHint())
        self.env_box.list_con.addItem(item)
        self.env_box.list_con.setItemWidget(item, con_item)
        # self.env_box.dict_con[''] = item
        self.env_box.fit_content()

    def add_state(self, name=None):
        if self.configs is None:
            return

        var_names = [next(iter(d)) for d in self.configs['variables']]
        options = self.configs['observations'] + var_names
        item = QListWidgetItem(self.env_box.list_sta)
        sta_item = state_item(options,
                              lambda: self.env_box.list_sta.takeItem(
                                  self.env_box.list_sta.row(item)), name)
        item.setSizeHint(sta_item.sizeHint())
        self.env_box.list_sta.addItem(item)
        self.env_box.list_sta.setItemWidget(item, sta_item)
        self.env_box.fit_content()

    def _compose_vocs(self):
        # Compose the VOCS settings
        variables = []
        for i in range(self.env_box.list_var.count()):
            item = self.env_box.list_var.item(i)
            item_widget = self.env_box.list_var.itemWidget(item)
            if item_widget.check_name.isChecked():
                var_name = item_widget.check_name.text()
                lb = item_widget.sb_lower.sb.value()
                ub = item_widget.sb_upper.sb.value()
                _dict = {}
                _dict[var_name] = [lb, ub]
                variables.append(_dict)

        objectives = []
        for i in range(self.env_box.list_obj.count()):
            item = self.env_box.list_obj.item(i)
            item_widget = self.env_box.list_obj.itemWidget(item)
            if item_widget.check_name.isChecked():
                obj_name = item_widget.check_name.text()
                rule = item_widget.cb_rule.currentText()
                _dict = {}
                _dict[obj_name] = rule
                objectives.append(_dict)

        constraints = []
        for i in range(self.env_box.list_con.count()):
            item = self.env_box.list_con.item(i)
            item_widget = self.env_box.list_con.itemWidget(item)
            critical = item_widget.check_crit.isChecked()
            con_name = item_widget.cb_obs.currentText()
            relation = CONS_RELATION_DICT[item_widget.cb_rel.currentText()]
            value = item_widget.sb.value()
            _dict = {}
            _dict[con_name] = [relation, value]
            if critical:
                _dict[con_name].append('CRITICAL')
            constraints.append(_dict)

        states = []
        for i in range(self.env_box.list_sta.count()):
            item = self.env_box.list_sta.item(i)
            item_widget = self.env_box.list_sta.itemWidget(item)
            sta_name = item_widget.cb_sta.currentText()
            states.append(sta_name)

        vocs = {
            'variables': variables,
            'objectives': objectives,
            'constraints': constraints,
            'states': states,
        }

        return vocs

    def _compose_routine(self):
        # Compose the routine
        name = self.edit_save.text() or self.edit_save.placeholderText()
        algo = self.algo_box.cb.currentText()
        assert algo, 'Please specify algorithm'
        env = self.env_box.cb.currentText()
        assert env, 'Please specify environment'
        algo_params = load_config(self.algo_box.edit.toPlainText())
        env_params = load_config(self.env_box.edit.toPlainText())

        variables = []
        for i in range(self.env_box.list_var.count()):
            item = self.env_box.list_var.item(i)
            item_widget = self.env_box.list_var.itemWidget(item)
            if item_widget.check_name.isChecked():
                var_name = item_widget.check_name.text()
                lb = item_widget.sb_lower.sb.value()
                ub = item_widget.sb_upper.sb.value()
                _dict = {}
                _dict[var_name] = [lb, ub]
                variables.append(_dict)

        objectives = []
        for i in range(self.env_box.list_obj.count()):
            item = self.env_box.list_obj.item(i)
            item_widget = self.env_box.list_obj.itemWidget(item)
            if item_widget.check_name.isChecked():
                obj_name = item_widget.check_name.text()
                rule = item_widget.cb_rule.currentText()
                _dict = {}
                _dict[obj_name] = rule
                objectives.append(_dict)

        constraints = []
        for i in range(self.env_box.list_con.count()):
            item = self.env_box.list_con.item(i)
            item_widget = self.env_box.list_con.itemWidget(item)
            critical = item_widget.check_crit.isChecked()
            con_name = item_widget.cb_obs.currentText()
            relation = CONS_RELATION_DICT[item_widget.cb_rel.currentText()]
            value = item_widget.sb.value()
            _dict = {}
            _dict[con_name] = [relation, value]
            if critical:
                _dict[con_name].append('CRITICAL')
            constraints.append(_dict)

        states = []
        for i in range(self.env_box.list_sta.count()):
            item = self.env_box.list_sta.item(i)
            item_widget = self.env_box.list_sta.itemWidget(item)
            sta_name = item_widget.cb_sta.currentText()
            states.append(sta_name)

        try:
            scaling = self.algo_box.cb_scaling.currentText()
            scaling_params = load_config(self.algo_box.edit_scaling.toPlainText())
            domain_scaling = {'func': scaling, **scaling_params}
        except:
            domain_scaling = None

        configs = {
            'variables': variables,
            'objectives': objectives,
            'constraints': constraints,
            'states': states,
            'domain_scaling': domain_scaling,
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

    def save(self):
        try:
            routine = self._compose_routine()
        except Exception as e:
            return QMessageBox.critical(self, 'Error!', str(e))

        try:
            save_routine(routine)
        except sqlite3.IntegrityError:
            return QMessageBox.critical(self, 'Error!',
                f'Routine {routine["name"]} already existed in the database! Please choose another name.')

        return 0

    def delete(self):
        name = self.edit_save.text() or self.edit_save.placeholderText()
        remove_routine(name)

        return 0
