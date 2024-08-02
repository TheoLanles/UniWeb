import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QIcon
from shortcuts import Shortcuts
from windows_theme_manager import dark_title_bar, light_title_bar, get_windows_theme, apply_theme
from popup_url import UrlPopup

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()

        self.load_config()
        self.browser.setUrl(QUrl(self.url))

        self.browser.titleChanged.connect(self.update_title)

        self.setCentralWidget(self.browser)
        self.showMaximized()

        self.setWindowIcon(QIcon('icon/icon.png'))
        
        self.setWindowTitle('UniWeb')

        self.timer = QTimer(self)
        self.timer.setInterval(6000)
        self.timer.timeout.connect(self.update_title_with_delay)
        self.timer.start()

        self.shortcuts = Shortcuts(self.browser, UrlPopup)

        theme = get_windows_theme()
        apply_theme(self, theme)

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

def main():
    app = QApplication(sys.argv)
    window = Browser()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 