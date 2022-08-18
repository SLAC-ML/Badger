from PyQt5.QtWidgets import QComboBox, QGridLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QApplication, QStyledItemDelegate
from qdarkstyle import load_stylesheet, DarkPalette, LightPalette
from ...settings import list_settings, read_value, write_value


class BadgerSettingsDialog(QDialog):
    theme_list = ['default', 'light', 'dark']
    theme_idx_dict = {
        'default': 0,
        'light': 1,
        'dark': 2,
    }

    def __init__(self, parent):
        super().__init__(parent)

        self.settings = list_settings()  # store the current settings

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        self.setWindowTitle('Badger settings')
        self.resize(320, 240)

        vbox = QVBoxLayout(self)

        widget_settings = QWidget(self)
        grid = QGridLayout(widget_settings)
        grid.setContentsMargins(0, 0, 0, 0)

        # Theme selector
        theme = self.settings['BADGER_THEME']
        self.lbl_theme = lbl_theme = QLabel('Theme')
        self.cb_theme = cb_theme = QComboBox()
        cb_theme.setItemDelegate(QStyledItemDelegate())
        cb_theme.addItems(self.theme_list)
        cb_theme.setCurrentIndex(self.theme_idx_dict[theme])

        grid.addWidget(lbl_theme, 0, 0)
        grid.addWidget(cb_theme, 0, 1)

        grid.setColumnStretch(1, 1)

        vbox.addWidget(widget_settings)

        self.btns = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)  # type: ignore

        vbox.addStretch(1)
        vbox.addWidget(self.btns)

    def config_logic(self):
        self.cb_theme.currentIndexChanged.connect(self.select_theme)
        self.btns.accepted.connect(self.apply_settings)
        self.btns.rejected.connect(self.restore_settings)

    def set_theme(self, theme):
        app = QApplication.instance()
        if theme == 'dark':
            app.setStyleSheet(load_stylesheet(palette=DarkPalette))
        elif theme == 'light':
            app.setStyleSheet(load_stylesheet(palette=LightPalette))
        else:
            app.setStyleSheet('')

    def select_theme(self, i):
        theme = self.theme_list[i]
        self.set_theme(theme)
        # Update the internal settings
        write_value('BADGER_THEME', theme)

    def apply_settings(self):
        self.accept()

    def restore_settings(self):
        # Reset theme if needed
        theme_curr = read_value('BADGER_THEME')
        theme_prev = self.settings['BADGER_THEME']
        if theme_prev != theme_curr:
            self.set_theme(theme_prev)

        for key in self.settings.keys():
            write_value(key, self.settings[key])

        self.reject()
