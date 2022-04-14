from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QPlainTextEdit
from PyQt5.QtWidgets import QComboBox, QCheckBox, QStyledItemDelegate, QLabel
from .collapsible_box import CollapsibleBox


class BadgerAlgoBox(CollapsibleBox):
    def __init__(self, algos=[], parent=None):
        super().__init__(' Algorithm', parent)

        self.algos = algos

        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

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

        self.setContentLayout(vbox)
