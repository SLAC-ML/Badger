from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont


stylesheet_normal = '''
QWidget
{
    background-color: #4C566A;
    border-radius: 2px;
}
QWidget::hover
{
    background-color: #5E81AC;
}
QLabel
{
    background-color: rgba(255, 255, 255, 0);
}
'''

stylesheet_selected = '''
QWidget
{
    background-color: #4B6789;
    border-radius: 2px;
}
QWidget::hover
{
    background-color: #54749A;
}
QLabel
{
    background-color: rgba(255, 255, 255, 0);
}
'''

def routine_item(name, timestamp, callback=None):
    cool_font = QFont()
    cool_font.setWeight(QFont.DemiBold)
    cool_font.setPixelSize(16)

    widget = QWidget()
    widget.setStyleSheet(stylesheet_normal)
    vbox = QVBoxLayout(widget)
    vbox.setContentsMargins(8, 8, 8, 8)
    vbox.setSpacing(0)
    routine_name = QLabel(name)
    routine_name.setFont(cool_font)
    vbox.addWidget(routine_name)
    _timestamp = datetime.fromisoformat(timestamp)
    time_str = _timestamp.strftime('%m/%d/%Y, %H:%M:%S')
    time_created = QLabel(time_str)
    vbox.addWidget(time_created)

    return widget
