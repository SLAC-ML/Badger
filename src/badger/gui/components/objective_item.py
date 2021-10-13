from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QCheckBox, QLabel, QComboBox


def objective_item(name, rule):
    # rule: 0 for MINIMIZE, 1 for MAXIMIZE
    widget = QWidget()
    vbox = QVBoxLayout(widget)
    vbox.setSpacing(0)
    check_name = QCheckBox(name)
    check_name.setChecked(True)
    vbox.addWidget(check_name)
    widget_rule = QWidget()
    hbox = QHBoxLayout(widget_rule)
    # hbox.setSpacing(0)
    hbox.setContentsMargins(0, 0, 0, 0)
    label = QLabel('rule')
    cb_rule = QComboBox()
    cb_rule.addItems(['MINIMIZE', 'MAXIMIZE'])
    cb_rule.setCurrentIndex(rule)
    hbox.addWidget(label)
    hbox.addWidget(cb_rule, 1)
    vbox.addWidget(widget_rule)

    def toggle_item():
        widget_rule.setDisabled(not check_name.isChecked())

    check_name.stateChanged.connect(toggle_item)

    return widget
