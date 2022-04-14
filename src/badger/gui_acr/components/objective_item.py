from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QCheckBox, QLabel
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate


def objective_item(name, rule, callback=None):
    # rule: 0 for MINIMIZE, 1 for MAXIMIZE
    widget = QWidget()
    vbox = QVBoxLayout(widget)
    vbox.setSpacing(0)
    widget.check_name = check_name = QCheckBox(name)
    check_name.setChecked(True)
    vbox.addWidget(check_name)
    widget_rule = QWidget()
    hbox = QHBoxLayout(widget_rule)
    hbox.setContentsMargins(0, 0, 0, 0)
    label = QLabel('rule')
    widget.cb_rule = cb_rule = QComboBox()
    cb_rule.setItemDelegate(QStyledItemDelegate())
    cb_rule.addItems(['MINIMIZE', 'MAXIMIZE'])
    cb_rule.setCurrentIndex(rule)
    hbox.addWidget(label)
    hbox.addWidget(cb_rule, 1)
    vbox.addWidget(widget_rule)

    def toggle_item():
        widget_rule.setDisabled(not check_name.isChecked())
        if callback is not None:
            callback(name)

    check_name.stateChanged.connect(toggle_item)

    return widget
