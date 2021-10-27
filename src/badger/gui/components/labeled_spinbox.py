from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QDoubleSpinBox


def labeled_spinbox(name, default_value):
    widget = QWidget()
    hbox = QHBoxLayout(widget)
    hbox.setContentsMargins(0, 0, 0, 0)
    label = QLabel(name)
    widget.sb = sb = QDoubleSpinBox()
    sb.setValue(default_value)
    hbox.addWidget(label)
    hbox.addWidget(sb, 1)

    return widget
