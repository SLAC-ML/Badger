from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QLabel
from .collapsible_box import CollapsibleBox


class BadgerFilterBox(CollapsibleBox):

    def __init__(self, parent=None, title="", tags = []):
        super().__init__(parent, title)
        
        self.tags = tags

        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
        
        # Machine filter
        mach = QWidget()
        hbox_mach = QHBoxLayout(mach)
        hbox_mach.setContentsMargins(0, 0, 0, 0)
        lbl = QLabel('Machine')
        lbl.setFixedWidth(64)
        self.cb_mach = cb_mach = QComboBox()
        cb_mach.setItemDelegate(QStyledItemDelegate())
        cb_mach.addItems(['']+self.tags)
        cb_mach.setCurrentIndex(-1)
        hbox_mach.addWidget(lbl)
        hbox_mach.addWidget(cb_mach, 1)
        vbox.addWidget(mach)

        # Obj filter
        obj = QWidget()
        hbox_obj = QHBoxLayout(obj)
        hbox_obj.setContentsMargins(0, 0, 0, 0)
        lbl = QLabel('Objective')
        lbl.setFixedWidth(64)
        self.cb_obj = cb_obj = QComboBox()
        cb_obj.setItemDelegate(QStyledItemDelegate())
        cb_obj.addItems([''])
        cb_obj.setCurrentIndex(-1)
        hbox_obj.addWidget(lbl)
        hbox_obj.addWidget(cb_obj, 1)
        vbox.addWidget(obj)

        # Region filter
        region = QWidget()
        hbox_reg = QHBoxLayout(region)
        hbox_reg.setContentsMargins(0, 0, 0, 0)
        lbl = QLabel('Region')
        lbl.setFixedWidth(64)
        self.cb_reg = cb_reg = QComboBox()
        cb_reg.setItemDelegate(QStyledItemDelegate())
        cb_reg.addItems([''])
        cb_reg.setCurrentIndex(-1)
        hbox_reg.addWidget(lbl)
        hbox_reg.addWidget(cb_reg, 1)
        vbox.addWidget(region)

        # Gain filter
        gain = QWidget()
        hbox_gain = QHBoxLayout(gain)
        hbox_gain.setContentsMargins(0, 0, 0, 8)
        lbl = QLabel('Gain')
        lbl.setFixedWidth(64)
        self.cb_gain = cb_gain = QComboBox()
        cb_gain.setItemDelegate(QStyledItemDelegate())
        cb_gain.addItems([''])
        cb_gain.setCurrentIndex(-1)
        hbox_gain.addWidget(lbl)
        hbox_gain.addWidget(cb_gain, 1)
        vbox.addWidget(gain)

        self.setContentLayout(vbox)
