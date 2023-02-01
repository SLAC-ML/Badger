from PyQt5.QtWidgets import QHBoxLayout, QWidget, QCheckBox
from .labeled_spinbox import labeled_spinbox


def variable_item(name, vrange, callback=None):
    widget = QWidget()
    hbox = QHBoxLayout(widget)
    hbox.setContentsMargins(2, 2, 2, 2)
    widget.check_name = check_name = QCheckBox(name)
    check_name.setFixedWidth(200)
    check_name.setChecked(True)
    hbox.addWidget(check_name)
    # hbox.addSpacing(8)
    widget_range = QWidget()
    hbox.addWidget(widget_range)
    hbox_range = QHBoxLayout(widget_range)
    hbox_range.setContentsMargins(0, 0, 0, 0)
    widget.sb_lower = sb_lower = labeled_spinbox('min', vrange[0], vrange[0], vrange[1])
    widget.sb_upper = sb_upper = labeled_spinbox('max', vrange[1], vrange[0], vrange[1])
    hbox_range.addWidget(sb_lower, 1)
    hbox_range.addWidget(sb_upper, 1)

    def toggle_item():
        widget_range.setDisabled(not check_name.isChecked())
        if callback is not None:
            callback(name)

    check_name.stateChanged.connect(toggle_item)

    return widget
