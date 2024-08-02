import sys
import json
import os
import mimetypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QIcon
from shortcuts import Shortcuts
from windows_theme_manager import get_windows_theme, apply_theme, monitor_theme_changes
from popup_url import UrlPopup
import qdarktheme

DEFAULT_DOWNLOAD_PATH = os.path.expanduser("~\Downloads")

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        qdarktheme.setup_theme()
        qdarktheme.setup_theme("auto")

        self.load_config()
        self.browser.setUrl(QUrl(self.url))

        self.browser.titleChanged.connect(self.update_title)

        self.browser.page().profile().downloadRequested.connect(self.handle_download)

        self.setCentralWidget(self.browser)
        self.showMaximized()

        self.setWindowIcon(QIcon('icon/icon.png'))
        
        self.setWindowTitle('UniWeb')

        self.timer = QTimer(self)
        self.timer.setInterval(6000)
        self.timer.timeout.connect(self.update_title_with_delay)
        self.timer.start()

        self.shortcuts = Shortcuts(self.browser, UrlPopup)

        apply_theme(self, get_windows_theme())
        monitor_theme_changes(self)

    def load_config(self):
        try:
            with open('config/config.json', 'r') as file:
                config = json.load(file)
                self.url = config.get('url')
        except FileNotFoundError:
            print("Fichier config.json non trouvé. Utilisation de l'URL par défaut.")
            self.url = 'https://github.com/TheoLanles/UniWeb'
        except json.JSONDecodeError:
            print("Erreur de décodage du fichier config.json. Utilisation de l'URL par défaut.")
            self.url = 'https://github.com/TheoLanles/UniWeb'

    def update_title(self):
        self.setWindowTitle(self.browser.page().title())

    def update_title_with_delay(self):
        self.timer.stop()
        self.update_title()

    def handle_download(self, download):
        suggested_file_name = download.suggestedFileName()
        default_file_path = os.path.join(DEFAULT_DOWNLOAD_PATH, suggested_file_name)
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', default_file_path)

        if file_path:
            if not os.path.splitext(file_path)[1]: 
                mime_type = download.mimeType()
                extension = mimetypes.guess_extension(mime_type)
                if extension:
                    file_path += extension
                else:
                    file_path += '.download'

            download.setPath(file_path)
            download.accept()
        else:
            download.cancel()
def main():
    app = QApplication(sys.argv)
    window = Browser()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()