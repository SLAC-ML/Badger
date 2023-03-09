from PyQt5.QtWidgets import QTextEdit, QHBoxLayout, QVBoxLayout, QCheckBox, QWidget, QMainWindow
from ....factory import get_algo_docs


class BadgerDocsWindow(QMainWindow):
    def __init__(self, parent, algo):
        super().__init__(parent=parent)

        self.algo = algo
        self.render_md = True
        self.docs = None

        self.init_ui()
        self.config_logic()
        self.load_docs()

    def init_ui(self):
        self.setWindowTitle(f'Docs for algorithm {self.algo}')
        self.resize(640, 640)

        doc_panel = QWidget(self)
        vbox = QVBoxLayout(doc_panel)

        # Toolbar
        toolbar = QWidget()
        hbox_tool = QHBoxLayout(toolbar)
        hbox_tool.setContentsMargins(0, 0, 0, 0)
        self.cb_md = cb_md = QCheckBox('Render as Markdown')
        cb_md.setChecked(True)
        hbox_tool.addStretch()
        hbox_tool.addWidget(cb_md)
        vbox.addWidget(toolbar)

        self.markdown_viewer = QTextEdit()
        self.markdown_viewer.setReadOnly(True)
        vbox.addWidget(self.markdown_viewer)

        self.setCentralWidget(doc_panel)

    def config_logic(self):
        self.cb_md.stateChanged.connect(self.switch_render_mode)

    def load_docs(self):
        try:
            self.docs = docs = get_algo_docs(self.algo)
        except Exception as e:
            self.docs = docs = str(e)

        if self.render_md:
            self.markdown_viewer.setMarkdown(docs)
        else:
            self.markdown_viewer.setText(docs)

    def update_docs(self, algo):
        self.algo = algo
        self.setWindowTitle(f'Docs for algorithm {algo}')
        self.load_docs()

    def switch_render_mode(self):
        self.render_md = self.cb_md.isChecked()
        self.load_docs()
