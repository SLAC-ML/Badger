from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QMainWindow
from ....factory import get_algo_docs


class BadgerDocsWindow(QMainWindow):
    def __init__(self, parent, algo):
        super().__init__(parent=parent)

        self.algo = algo

        self.init_ui()
        self.load_docs()

    def init_ui(self):
        self.setWindowTitle(f'Docs for algorithm {self.algo}')
        self.resize(640, 640)

        doc_panel = QWidget(self)
        vbox = QVBoxLayout(doc_panel)
        self.markdown_viewer = QTextEdit()
        self.markdown_viewer.setReadOnly(True)
        vbox.addWidget(self.markdown_viewer)

        self.setCentralWidget(doc_panel)

    def load_docs(self):
        try:
            docs = get_algo_docs(self.algo)
        except Exception as e:
            docs = str(e)

        self.markdown_viewer.setMarkdown(docs)

    def update_docs(self, algo):
        self.algo = algo
        self.setWindowTitle(f'Docs for algorithm {algo}')
        self.load_docs()
