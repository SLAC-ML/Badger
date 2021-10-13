from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QCheckBox, QDoubleSpinBox
from .labeled_spinbox import labeled_spinbox


def variable_item(name, range):
    widget = QWidget()
    vbox = QVBoxLayout(widget)
    vbox.setSpacing(0)
    check_name = QCheckBox(name)
    check_name.setChecked(True)
    vbox.addWidget(check_name)
    widget_range = QWidget()
    hbox = QHBoxLayout(widget_range)
    hbox.setContentsMargins(0, 0, 0, 0)
    sb_lower = labeled_spinbox('min', range[0])
    sb_upper = labeled_spinbox('max', range[1])
    hbox.addWidget(sb_lower, 1)
    hbox.addSpacing(16)
    hbox.addWidget(sb_upper, 1)
    vbox.addWidget(widget_range)

    def toggle_item():
        widget_range.setDisabled(not check_name.isChecked())

    check_name.stateChanged.connect(toggle_item)

    return widget
