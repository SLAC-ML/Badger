from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtWidgets import QComboBox, QCheckBox, QListWidget, QLabel
from .collapsible_box import CollapsibleBox


class BadgerConfigBox(CollapsibleBox):
    def __init__(self, parent=None):
        super().__init__(' Configs', parent)

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        self.vbox = vbox = QVBoxLayout()

        # Variables config
        var_panel = QWidget()
        vbox.addWidget(var_panel, 2)
        hbox_var = QHBoxLayout(var_panel)
        hbox_var.setContentsMargins(0, 0, 0, 0)
        lbl_var_col = QWidget()
        vbox_lbl_var = QVBoxLayout(lbl_var_col)
        vbox_lbl_var.setContentsMargins(0, 0, 0, 0)
        lbl_var = QLabel('Vars')
        lbl_var.setFixedWidth(64)
        vbox_lbl_var.addWidget(lbl_var)
        vbox_lbl_var.addStretch(1)
        hbox_var.addWidget(lbl_var_col)

        edit_var_col = QWidget()
        vbox_var_edit = QVBoxLayout(edit_var_col)
        vbox_var_edit.setContentsMargins(0, 0, 0, 0)
        action_var = QWidget()
        hbox_action_var = QHBoxLayout(action_var)
        hbox_action_var.setContentsMargins(0, 0, 0, 0)
        vbox_var_edit.addWidget(action_var)
        self.btn_all_var = btn_all_var = QPushButton('Check All')
        self.btn_un_all_var = btn_un_all_var = QPushButton('Uncheck All')
        btn_all_var.setFixedSize(96, 24)
        btn_un_all_var.setFixedSize(96, 24)
        self.btn_add_var = btn_add_var = QPushButton('Add')
        btn_add_var.setFixedSize(96, 24)
        btn_add_var.setDisabled(True)
        self.check_only_var = check_only_var = QCheckBox('Show Checked Only')
        check_only_var.setChecked(False)
        hbox_action_var.addWidget(btn_all_var)
        hbox_action_var.addWidget(btn_un_all_var)
        hbox_action_var.addWidget(btn_add_var)
        hbox_action_var.addStretch()
        hbox_action_var.addWidget(check_only_var)
        self.list_var = QListWidget()
        self.list_var.setViewportMargins(2, 2, 17, 2)
        # self.list_var.setFixedHeight(128)
        vbox_var_edit.addWidget(self.list_var)
        # vbox_var_edit.addStretch()
        hbox_var.addWidget(edit_var_col)

        # Objectives config
        obj_panel = QWidget()
        vbox.addWidget(obj_panel, 1)
        hbox_obj = QHBoxLayout(obj_panel)
        hbox_obj.setContentsMargins(0, 0, 0, 0)
        lbl_obj_col = QWidget()
        vbox_lbl_obj = QVBoxLayout(lbl_obj_col)
        vbox_lbl_obj.setContentsMargins(0, 0, 0, 0)
        lbl_obj = QLabel('Objs')
        lbl_obj.setFixedWidth(64)
        vbox_lbl_obj.addWidget(lbl_obj)
        vbox_lbl_obj.addStretch(1)
        hbox_obj.addWidget(lbl_obj_col)

        edit_obj_col = QWidget()
        vbox_obj_edit = QVBoxLayout(edit_obj_col)
        vbox_obj_edit.setContentsMargins(0, 0, 0, 0)
        action_obj = QWidget()
        hbox_action_obj = QHBoxLayout(action_obj)
        hbox_action_obj.setContentsMargins(0, 0, 0, 0)
        vbox_obj_edit.addWidget(action_obj)
        self.btn_all_obj = btn_all_obj = QPushButton('Check All')
        self.btn_un_all_obj = btn_un_all_obj = QPushButton('Uncheck All')
        btn_all_obj.setFixedSize(96, 24)
        btn_un_all_obj.setFixedSize(96, 24)
        self.check_only_obj = check_only_obj = QCheckBox('Show Checked Only')
        check_only_obj.setChecked(False)
        hbox_action_obj.addWidget(btn_all_obj)
        hbox_action_obj.addWidget(btn_un_all_obj)
        hbox_action_obj.addStretch()
        hbox_action_obj.addWidget(check_only_obj)
        self.list_obj = QListWidget()
        # self.list_obj.setFixedHeight(64)
        self.list_obj.setViewportMargins(2, 2, 17, 2)
        vbox_obj_edit.addWidget(self.list_obj)
        # vbox_obj_edit.addStretch()
        hbox_obj.addWidget(edit_obj_col)

        # Constraints config
        con_panel = QWidget()
        vbox.addWidget(con_panel, 1)
        hbox_con = QHBoxLayout(con_panel)
        hbox_con.setContentsMargins(0, 0, 0, 0)
        lbl_con_col = QWidget()
        vbox_lbl_con = QVBoxLayout(lbl_con_col)
        vbox_lbl_con.setContentsMargins(0, 0, 0, 0)
        lbl_con = QLabel('Cons')
        lbl_con.setFixedWidth(64)
        vbox_lbl_con.addWidget(lbl_con)
        vbox_lbl_con.addStretch(1)
        hbox_con.addWidget(lbl_con_col)

        edit_con_col = QWidget()
        vbox_con_edit = QVBoxLayout(edit_con_col)
        vbox_con_edit.setContentsMargins(0, 0, 0, 0)
        action_con = QWidget()
        hbox_action_con = QHBoxLayout(action_con)
        hbox_action_con.setContentsMargins(0, 0, 0, 0)
        vbox_con_edit.addWidget(action_con)
        self.btn_add_con = btn_add_con = QPushButton('Add')
        btn_add_con.setFixedSize(96, 24)
        btn_add_con.setDisabled(True)
        hbox_action_con.addWidget(btn_add_con)
        hbox_action_con.addStretch()
        self.list_con = QListWidget()
        # self.list_con.setFixedHeight(64)
        self.list_con.setViewportMargins(2, 2, 17, 2)
        vbox_con_edit.addWidget(self.list_con)
        # vbox_con_edit.addStretch()
        hbox_con.addWidget(edit_con_col)

        self.setContentLayout(vbox)

    def config_logic(self):
        self.dict_var = {}
        self.dict_obj = {}
        self.dict_con = {}

    def _fit_content(self, list):
        height = list.sizeHintForRow(0) * list.count() + 2 * list.frameWidth() + 4
        height = max(28, min(height, 192))
        list.setFixedHeight(height)

    def fit_content(self):
        return
        self._fit_content(self.list_var)
        self._fit_content(self.list_obj)
        self._fit_content(self.list_con)
