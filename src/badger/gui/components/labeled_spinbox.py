from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QDoubleSpinBox, QAbstractSpinBox


def labeled_spinbox(name, default_value, lb, ub, decimals=4):
    widget = QWidget()
    hbox = QHBoxLayout(widget)
    hbox.setContentsMargins(0, 0, 0, 0)
    label = QLabel(name)
    widget.sb = sb = QDoubleSpinBox()
    sb.setDecimals(decimals)
    sb.setRange(lb, ub)
    sb.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
    sb.setValue(default_value)
    hbox.addWidget(label)
    hbox.addWidget(sb, 1)

    return widget
