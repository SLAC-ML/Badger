from inspect import stack
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QTextEdit, QStackedWidget, QScrollArea
# from PyQt5.QtWidgets import QFrame, QSizePolicy
from PyQt5.QtGui import QFont
from .routine_page import BadgerRoutinePage
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

        # Routine stacks
        self.stacks = stacks = QStackedWidget()

        self.routine_edit = routine_edit = QTextEdit()
        routine_edit.setReadOnly(True)
        stacks.addWidget(routine_edit)

        self.scroll_area = scroll_area = QScrollArea()
        self.routine_page = routine_page = BadgerRoutinePage()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(routine_page)
        stacks.addWidget(scroll_area)

        stacks.setCurrentIndex(1)
        vbox.addWidget(stacks)

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
        self.btn_edit.clicked.connect(self.edit_routine)

    def set_routine(self, routine):
        self.routine_edit.setText(ystring(routine))
        self.routine_page.refresh_ui(routine)

    def edit_routine(self):
        self.stacks.setCurrentIndex(1)

    def clear(self):
        self.routine_edit.clear()
