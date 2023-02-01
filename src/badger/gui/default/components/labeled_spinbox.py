from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QDoubleSpinBox, QAbstractSpinBox
from PyQt5.QtCore import Qt
from ..utils import MouseWheelWidgetAdjustmentGuard


def labeled_spinbox(name, default_value, lb, ub, decimals=4):
    widget = QWidget()
    hbox = QHBoxLayout(widget)
    hbox.setContentsMargins(0, 0, 0, 0)
    label = QLabel(name)
    widget.sb = sb = QDoubleSpinBox()
    sb.setDecimals(decimals)
    sb.setFocusPolicy(Qt.StrongFocus)
    sb.installEventFilter(MouseWheelWidgetAdjustmentGuard(sb))

    # Sanity check
    if lb is None:
        lb = -1e3
    if ub is None:
        ub = 1e3
    if default_value is None:
        default_value = 0

    sb.setRange(lb, ub)
    sb.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
    sb.setValue(default_value)
    hbox.addWidget(label)
    hbox.addWidget(sb, 1)

    return widget
