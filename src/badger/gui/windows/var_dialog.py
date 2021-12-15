from PyQt5.QtWidgets import QDialog, QWidget, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QGroupBox, QMessageBox
from ..components.labeled_lineedit import labeled_lineedit
from ...factory import get_intf


class BadgerVariableDialog(QDialog):
    def __init__(self, parent, env_class, env_params, intf_name):
        super().__init__(parent)

        if intf_name is not None:
            Interface, _ = get_intf(intf_name)
            intf = Interface()
        else:
            intf = None

        env = env_class(intf, env_params)
        self.env = env

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        self.setWindowTitle(f'Add variable')
        self.setMinimumWidth(360)

        vbox = QVBoxLayout(self)

        # Action bar
        action_bar = QWidget()
        hbox = QHBoxLayout(action_bar)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.edit_name = edit_name = QLineEdit()
        edit_name.setPlaceholderText('Variable name')
        self.btn_check = btn_check = QPushButton('Check')
        btn_check.setDisabled(True)
        btn_check.setFixedSize(96, 24)
        hbox.addWidget(edit_name, 1)
        hbox.addWidget(btn_check)

        # Info group
        group_info = QGroupBox('Variable Info')
        vbox_info = QVBoxLayout(group_info)

        self.edit_value = labeled_lineedit('value', '', 48)
        self.edit_min = labeled_lineedit('min', '', 48)
        self.edit_max = labeled_lineedit('max', '', 48)
        vbox_info.addWidget(self.edit_value)
        vbox_info.addWidget(self.edit_min)
        vbox_info.addWidget(self.edit_max)

        # Button set
        button_set = QWidget()
        hbox_set = QHBoxLayout(button_set)
        hbox_set.setContentsMargins(0, 0, 0, 0)
        self.btn_cancel = btn_cancel = QPushButton('Cancel')
        self.btn_add = btn_add = QPushButton('Add')
        btn_add.setDisabled(True)
        btn_cancel.setFixedSize(96, 24)
        btn_add.setFixedSize(96, 24)
        hbox_set.addStretch()
        hbox_set.addWidget(btn_cancel)
        hbox_set.addWidget(btn_add)

        vbox.addWidget(action_bar)
        vbox.addWidget(group_info)
        vbox.addStretch()
        vbox.addWidget(button_set)

    def config_logic(self):
        self.edit_name.textChanged.connect(self.var_changed)
        self.btn_cancel.clicked.connect(self.close)
        self.btn_check.clicked.connect(self.check_var)

    def var_changed(self, text):
        self.btn_add.setDisabled(True)

        if text:
            self.btn_check.setDisabled(False)
        else:
            self.btn_check.setDisabled(True)

    def check_var(self):
        name = self.edit_name.text()
        try:
            value = self.env._get_var(name)
            min, max = self.env._get_vrange(name)

            self.edit_value.edit.setText(str(value))
            self.edit_min.edit.setText(str(min))
            self.edit_max.edit.setText(str(max))

            self.btn_add.setDisabled(False)
        except Exception as e:
            self.edit_value.edit.setText('')
            self.edit_min.edit.setText('')
            self.edit_max.edit.setText('')
            QMessageBox.critical(self, 'Error!', f'Variable {name} cannot be found!')

            self.btn_add.setDisabled(True)
