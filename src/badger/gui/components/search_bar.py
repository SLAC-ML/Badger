from PyQt6.QtWidgets import QLineEdit, QCompleter
from ...factory import list_env

def search_bar():
    word_list = list_env()

    completer = QCompleter(word_list)

    line_edit = QLineEdit()
    line_edit.setPlaceholderText('Search')
    line_edit.setCompleter(completer)

    return line_edit
