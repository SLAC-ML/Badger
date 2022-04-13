from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QTextEdit
# from PyQt5.QtWidgets import QFrame, QSizePolicy
from PyQt5.QtGui import QFont
from ...utils import ystring


class BadgerRoutineEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        # self.seperator = seperator = QFrame()
        # seperator.setFrameShape(QFrame.HLine)
        # seperator.setFrameShadow(QFrame.Sunken)
        # seperator.setLineWidth(0)
        # seperator.setMidLineWidth(0)
        # vbox.addWidget(seperator)

        self.routine_edit = routine_edit = QTextEdit()
        routine_edit.setReadOnly(True)
        vbox.addWidget(routine_edit)

        # Action bar
        self.action_bar = action_bar = QWidget()
        # action_bar.hide()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)

        cool_font = QFont()
        cool_font.setWeight(QFont.DemiBold)
        # cool_font.setPixelSize(16)

        self.btn_edit = btn_edit = QPushButton('Edit')
        btn_edit.setFixedSize(128, 32)
        btn_edit.setFont(cool_font)
        hbox_action.addStretch(1)
        hbox_action.addWidget(btn_edit)
        vbox.addWidget(action_bar)

    def config_logic(self):
        pass

    def set_routine(self, routine):
        self.routine_edit.setText(ystring(routine))

    def clear(self):
        self.routine_edit.clear()
