from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QCheckBox
from .labeled_spinbox import labeled_spinbox


def variable_item(name, vrange, callback=None):
    widget = QWidget()
    vbox = QVBoxLayout(widget)
    vbox.setSpacing(0)
    widget.check_name = check_name = QCheckBox(name)
    check_name.setChecked(True)
    vbox.addWidget(check_name)
    widget_range = QWidget()
    hbox = QHBoxLayout(widget_range)
    hbox.setContentsMargins(0, 0, 0, 0)
    widget.sb_lower = sb_lower = labeled_spinbox('min', vrange[0], vrange[0], vrange[1])
    widget.sb_upper = sb_upper = labeled_spinbox('max', vrange[1], vrange[0], vrange[1])
    hbox.addWidget(sb_lower, 1)
    hbox.addSpacing(16)
    hbox.addWidget(sb_upper, 1)
    vbox.addWidget(widget_range)

    def toggle_item():
        widget_range.setDisabled(not check_name.isChecked())
        if callback is not None:
            callback(name)

    check_name.stateChanged.connect(toggle_item)

    return widget
