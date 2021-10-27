from PyQt5.QtWidgets import QComboBox, QGridLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QApplication
from PyQt5.QtCore import QSettings
from qdarkstyle import load_stylesheet, DarkPalette, LightPalette


class BadgerSettingsDialog(QDialog):
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
        cb_theme.addItems(['light', 'dark'])
        cb_theme.setCurrentIndex(1 if theme == 'dark' else 0)

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
        if i:
            app.setStyleSheet(load_stylesheet(palette=DarkPalette))
            self.settings.setValue('theme', 'dark')
        else:
            app.setStyleSheet(load_stylesheet(palette=LightPalette))
            self.settings.setValue('theme', 'light')

    def apply_settings(self):
        self.accept()

    def restore_settings(self):
        app = QApplication.instance()
        for key in self._settings.keys():
            self.settings.setValue(key, self._settings[key])

        theme = self.settings.value('theme')
        if theme == 'dark':
            app.setStyleSheet(load_stylesheet(palette=DarkPalette))
        else:
            app.setStyleSheet(load_stylesheet(palette=LightPalette))

        self.reject()
