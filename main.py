import sys
import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QListWidget, QListWidgetItem
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer




class CustomBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wbrowser")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon("img/icon.ico"))

        self.browser = QWebEngineView()

        self.browser.setHtml(self.start_page_html())

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter...")
        self.search_bar.textChanged.connect(self.fetch_suggestions)
        self.search_bar.returnPressed.connect(self.load_query)

        self.go_button = QPushButton("Search")
        self.go_button.clicked.connect(self.load_query)

        self.suggestion_list = QListWidget()
        self.suggestion_list.setMaximumHeight(100)
        self.suggestion_list.hide()
        self.suggestion_list.itemClicked.connect(self.select_suggestion)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.search_bar)
        top_layout.addWidget(self.go_button)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.suggestion_list)
        layout.addWidget(self.browser)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update_suggestions)

    def start_page_html(self):
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <title>Welcome to Wbrowser</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    background-color: #0, 0, 0; 
                    text-align: center; 
                    margin-top: 100px; 
                    color: #333;
                }
                h1 { font-size: 48px; margin-bottom: 10px; }
                p { font-size: 18px; margin-bottom: 30px; }
                .logo {
                    width: 120px;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to Wbrowser</h1>
            <p>It's your personal app</p>
            <p>Type a search query above to start browsing.</p>
        </body>
        </html>
        """

    def load_query(self):
        text = self.search_bar.text().strip()

        if "." in text or text.startswith("http"):
            if not text.startswith("http"):
                text = "http://" + text
            url = QUrl(text)
        else:
            url = QUrl(f"https://www.google.com/search?q={text}")

        self.suggestion_list.hide()
        self.browser.setUrl(url)

    def fetch_suggestions(self, text):
        self.timer.start(300)
        self.current_input = text

    def update_suggestions(self):
        text = self.current_input
        if not text:
            self.suggestion_list.hide()
            return

        try:
            response = requests.get(
                "https://suggestqueries.google.com/complete/search",
                params={"client": "firefox", "q": text},
                timeout=2
            )
            suggestions = response.json()[1]
            self.show_suggestions(suggestions)
        except:
            self.suggestion_list.hide()

    def show_suggestions(self, suggestions):
        self.suggestion_list.clear()
        if not suggestions:
            self.suggestion_list.hide()
            return

        for suggestion in suggestions:
            item = QListWidgetItem(suggestion)
            self.suggestion_list.addItem(item)

        self.suggestion_list.show()

    def select_suggestion(self, item):
        self.search_bar.setText(item.text())
        self.load_query()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomBrowser()
    window.show()
    sys.exit(app.exec_())
