from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget, QDoubleSpinBox, QAbstractSpinBox
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate


def constraint_item(options, remove_item, decimals=4):
    widget = QWidget()
    hbox = QHBoxLayout(widget)
    # hbox.setContentsMargins(0, 0, 0, 0)
    # hbox.setSpacing(0)
    widget.cb_obs = cb_obs = QComboBox()
    cb_obs.setItemDelegate(QStyledItemDelegate())
    cb_obs.addItems(options)
    cb_obs.setCurrentIndex(0)

    widget.cb_rel = cb_rel = QComboBox()
    cb_rel.setItemDelegate(QStyledItemDelegate())
    cb_rel.addItems(['>', '<', '='])
    cb_rel.setFixedWidth(64)
    cb_rel.setCurrentIndex(0)

    widget.sb = sb = QDoubleSpinBox()
    sb.setDecimals(decimals)
    lb = -1e3
    ub = 1e3
    default_value = 0
    sb.setRange(lb, ub)
    sb.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
    sb.setValue(default_value)

    widget.btn_del = btn_del = QPushButton('Remove')
    btn_del.setFixedSize(72, 24)

    hbox.addWidget(cb_obs, 1)
    hbox.addWidget(cb_rel)
    hbox.addWidget(sb, 1)
    hbox.addWidget(btn_del)

    btn_del.clicked.connect(remove_item)

    return widget
