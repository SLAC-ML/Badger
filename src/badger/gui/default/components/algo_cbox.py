from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QPlainTextEdit
from PyQt5.QtWidgets import QComboBox, QCheckBox, QStyledItemDelegate, QLabel
from .collapsible_box import CollapsibleBox


class BadgerAlgoBox(CollapsibleBox):
    def __init__(self, algos=[], scaling_functions=[], parent=None):
        super().__init__(' Algorithm', parent)

        self.algos = algos
        self.scaling_functions = scaling_functions

        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        # Algo selector
        name = QWidget()
        hbox_name = QHBoxLayout(name)
        hbox_name.setContentsMargins(0, 0, 0, 0)
        lbl = QLabel('Name')
        lbl.setFixedWidth(64)
        self.cb = cb = QComboBox()
        cb.setItemDelegate(QStyledItemDelegate())
        cb.addItems(self.algos)
        cb.setCurrentIndex(-1)
        hbox_name.addWidget(lbl)
        hbox_name.addWidget(cb, 1)
        vbox.addWidget(name)

        # Algo params
        params = QWidget()
        hbox_params = QHBoxLayout(params)
        hbox_params.setContentsMargins(0, 0, 0, 0)
        lbl_params_col = QWidget()
        vbox_lbl_params = QVBoxLayout(lbl_params_col)
        vbox_lbl_params.setContentsMargins(0, 0, 0, 0)
        lbl_params = QLabel('Params')
        lbl_params.setFixedWidth(64)
        vbox_lbl_params.addWidget(lbl_params)
        vbox_lbl_params.addStretch(1)
        hbox_params.addWidget(lbl_params_col)

        edit_params_col = QWidget()
        vbox_params_edit = QVBoxLayout(edit_params_col)
        vbox_params_edit.setContentsMargins(0, 0, 0, 8)
        script_bar = QWidget()
        hbox_script = QHBoxLayout(script_bar)
        hbox_script.setContentsMargins(0, 0, 0, 0)
        vbox_params_edit.addWidget(script_bar)
        self.check_use_script = check_use_script = QCheckBox('Generate from Script')
        check_use_script.setChecked(False)
        self.btn_edit_script = btn_edit_script = QPushButton('Edit Script')
        btn_edit_script.setFixedSize(96, 24)
        btn_edit_script.hide()
        hbox_script.addWidget(check_use_script)
        hbox_script.addWidget(btn_edit_script)
        self.edit = edit = QPlainTextEdit()
        edit.setFixedHeight(128)
        vbox_params_edit.addWidget(edit)
        hbox_params.addWidget(edit_params_col)
        vbox.addWidget(params)

        # Domain scaling
        scaling = QWidget()
        hbox_scaling = QHBoxLayout(scaling)
        hbox_scaling.setContentsMargins(0, 0, 0, 0)
        lbl_scaling_col = QWidget()
        vbox_lbl_scaling = QVBoxLayout(lbl_scaling_col)
        vbox_lbl_scaling.setContentsMargins(0, 0, 0, 0)
        lbl_scaling = QLabel('Scaling')
        lbl_scaling.setFixedWidth(64)
        vbox_lbl_scaling.addWidget(lbl_scaling)
        vbox_lbl_scaling.addStretch(1)
        hbox_scaling.addWidget(lbl_scaling_col)

        edit_scaling_col = QWidget()
        vbox_scaling_edit = QVBoxLayout(edit_scaling_col)
        vbox_scaling_edit.setContentsMargins(0, 0, 0, 0)
        self.cb_scaling = cb_scaling = QComboBox()
        cb_scaling.setItemDelegate(QStyledItemDelegate())
        cb_scaling.addItems(self.scaling_functions)
        cb_scaling.setCurrentIndex(-1)
        vbox_scaling_edit.addWidget(cb_scaling)
        self.edit_scaling = edit_scaling = QPlainTextEdit()
        edit_scaling.setFixedHeight(128)
        vbox_scaling_edit.addWidget(edit_scaling)
        hbox_scaling.addWidget(edit_scaling_col)
        vbox.addWidget(scaling)

        self.setContentLayout(vbox)
