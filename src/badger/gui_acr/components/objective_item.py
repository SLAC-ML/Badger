from PyQt5.QtWidgets import QHBoxLayout, QWidget, QCheckBox, QLabel
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate


def objective_item(name, rule, callback=None):
    # rule: 0 for MINIMIZE, 1 for MAXIMIZE
    widget = QWidget()
    hbox = QHBoxLayout(widget)
    hbox.setContentsMargins(2, 2, 2, 2)
    widget.check_name = check_name = QCheckBox(name)
    check_name.setFixedWidth(200)
    check_name.setChecked(True)
    hbox.addWidget(check_name)
    widget_rule = QWidget()
    hbox.addWidget(widget_rule)
    hbox_rule = QHBoxLayout(widget_rule)
    hbox_rule.setContentsMargins(0, 0, 0, 0)
    label = QLabel('rule')
    widget.cb_rule = cb_rule = QComboBox()
    cb_rule.setItemDelegate(QStyledItemDelegate())
    cb_rule.addItems(['MINIMIZE', 'MAXIMIZE'])
    cb_rule.setCurrentIndex(rule)
    hbox_rule.addWidget(label)
    hbox_rule.addWidget(cb_rule, 1)

    def toggle_item():
        widget_rule.setDisabled(not check_name.isChecked())
        if callback is not None:
            callback(name)

    check_name.stateChanged.connect(toggle_item)

    return widget
