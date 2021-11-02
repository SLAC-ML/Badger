from PyQt5.QtWidgets import QComboBox, QGridLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QApplication, QStyledItemDelegate
from PyQt5.QtCore import QSettings
from qdarkstyle import load_stylesheet, DarkPalette, LightPalette


class BadgerSettingsDialog(QDialog):
    theme_list = ['default', 'light', 'dark']
    theme_idx_dict = {
        'default': 0,
        'light': 1,
        'dark': 2,
    }

    def __init__(self, parent):
        super().__init__(parent)

        self.settings = QSettings('SLAC-ML', 'Badger')
        self._settings = {}  # previous settings
        keys = self.settings.allKeys()
        for key in keys:
            self._settings[key] = self.settings.value(key)

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
        theme = self.settings.value('theme')
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
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        vbox.addStretch(1)
        vbox.addWidget(self.btns)

    def config_logic(self):
        self.cb_theme.currentIndexChanged.connect(self.select_theme)
        self.btns.accepted.connect(self.apply_settings)
        self.btns.rejected.connect(self.restore_settings)

    def select_theme(self, i):
        app = QApplication.instance()
        theme = self.theme_list[i]
        if theme == 'dark':
            app.setStyleSheet(load_stylesheet(palette=DarkPalette))
        elif theme == 'light':
            app.setStyleSheet(load_stylesheet(palette=LightPalette))
        else:
            app.setStyleSheet('')
        self.settings.setValue('theme', theme)

    def apply_settings(self):
        self.accept()

    def restore_settings(self):
        app = QApplication.instance()
        for key in self._settings.keys():
            self.settings.setValue(key, self._settings[key])

        theme = self.settings.value('theme')
        if theme == 'dark':
            app.setStyleSheet(load_stylesheet(palette=DarkPalette))
        elif theme == 'light':
            app.setStyleSheet(load_stylesheet(palette=LightPalette))
        else:
            app.setStyleSheet('')

        self.reject()
