from datetime import datetime
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


stylesheet_normal = '''
    background-color: #4C566A;
    border-radius: 2px;
'''

stylesheet_normal_hover = '''
    background-color: #5E81AC;
    border-radius: 2px;
'''

stylesheet_activate = '''
    background-color: #4B6789;
    border-radius: 2px;
'''

stylesheet_activate_hover = '''
    background-color: #54749A;
    border-radius: 2px;
'''

stylesheet_del = '''
QPushButton:hover:pressed
{
    background-color: #BF616A;
}
QPushButton:hover
{
    background-color: #A9444E;
}
QPushButton
{
    background-color: none;
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
}
'''

class BadgerRoutineItem(QWidget):
    sig_del = pyqtSignal(str)

    def __init__(self, name, timestamp, parent=None):
        super().__init__(parent)

        self.activated = False
        self.hover = False
        self.name = name
        self.timestamp = timestamp

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet(stylesheet_normal)

        cool_font = QFont()
        cool_font.setWeight(QFont.DemiBold)
        cool_font.setPixelSize(16)

        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        info_panel = QWidget()
        hbox.addWidget(info_panel, 1)
        vbox = QVBoxLayout(info_panel)
        vbox.setContentsMargins(8, 8, 8, 8)
        vbox.setSpacing(0)
        routine_name = QLabel(self.name)
        routine_name.setFont(cool_font)
        vbox.addWidget(routine_name)
        _timestamp = datetime.fromisoformat(self.timestamp)
        time_str = _timestamp.strftime('%m/%d/%Y, %H:%M:%S')
        time_created = QLabel(time_str)
        vbox.addWidget(time_created)

        self.btn_del = btn_del = QPushButton('X')
        btn_del.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        btn_del.setFixedWidth(24)
        btn_del.setStyleSheet(stylesheet_del)
        btn_del.hide()
        hbox.addWidget(btn_del)

    def config_logic(self):
        self.btn_del.clicked.connect(self.delete_routine)

    def activate(self):
        self.activated = True
        if self.hover:
            self.setStyleSheet(stylesheet_activate_hover)
        else:
            self.setStyleSheet(stylesheet_activate)

    def deactivate(self):
        self.activated = False
        if self.hover:
            self.setStyleSheet(stylesheet_normal_hover)
        else:
            self.setStyleSheet(stylesheet_normal)

    def enterEvent(self, event):
        self.hover = True
        self.btn_del.show()
        if self.activated:
            self.setStyleSheet(stylesheet_activate_hover)
        else:
            self.setStyleSheet(stylesheet_normal_hover)

    def leaveEvent(self, event):
        self.hover = False
        self.btn_del.hide()
        if self.activated:
            self.setStyleSheet(stylesheet_activate)
        else:
            self.setStyleSheet(stylesheet_normal)

    def delete_routine(self):
        self.sig_del.emit(self.name)
