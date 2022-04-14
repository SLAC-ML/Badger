from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QPlainTextEdit
from PyQt5.QtWidgets import QComboBox, QCheckBox, QStyledItemDelegate, QLabel
from .collapsible_box import CollapsibleBox


class BadgerEnvBox(CollapsibleBox):
    def __init__(self, envs=[], parent=None):
        super().__init__(' Environment', parent)

        self.envs = envs

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
        cb.addItems(self.envs)
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
        self.edit = edit = QPlainTextEdit()
        edit.setFixedHeight(128)
        vbox_params_edit.addWidget(edit)
        hbox_params.addWidget(edit_params_col)
        vbox.addWidget(params)

        action_bar = QWidget()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)
        self.btn_env_play = btn_env_play = QPushButton('Open Playground')
        btn_env_play.setFixedSize(128, 24)
        # btn_env_play.hide()  # hide for now to prevent confusions
        hbox_action.addStretch(1)
        hbox_action.addWidget(btn_env_play)
        vbox.addWidget(action_bar)

        self.setContentLayout(vbox)
