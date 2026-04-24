import logging
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QLineEdit, QWidget, QVBoxLayout
from PySide6.QtCore import Qt


class SearchLineEdit(QLineEdit):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.main_window.search_text(self.text())


class HTMLViewer(QWidget):
    def __init__(self, input_file) -> None:
        super().__init__()
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing HTMLViewer...")
        self.input_file = input_file

        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(
            self.webView.settings().WebAttribute.PluginsEnabled, True
        )
        self.webView.settings().setAttribute(
            self.webView.settings().WebAttribute.HTMLViewerEnabled, True
        )

        self.search_input = SearchLineEdit(self)

        self.search_input.setPlaceholderText("Enter text to search...")

        layout = QVBoxLayout(self)
        layout.addWidget(self.search_input)
        layout.addWidget(self.webView)
        self.setLayout(layout)

        self.load_file(self.input_file)

    def load_file(self, filename):
        self.webView.setUrl(QUrl("file:///" + filename.replace("\\", "/")))

    def search_text(self, text):
        flag = QWebEnginePage.FindFlag.FindCaseSensitively
        if text:
            self.webView.page().findText(text, flag)
        else:
            self.webView.page().stopFinding()
