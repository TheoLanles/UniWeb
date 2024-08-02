from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
import json
from windows_theme_manager import get_windows_theme, apply_theme
class UrlPopup(QDialog):
    def __init__(self, browser, parent=None):
        super().__init__(parent)
        self.browser = browser 
        self.setWindowTitle("Edit URL")
        self.setWindowIcon(QIcon('icon/icon.png'))
        self.setFixedSize(300, 150)

        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowSystemMenuHint)

        theme = get_windows_theme()
        apply_theme(self, theme)
        
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL...")
        
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_url)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Current URL :"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        self.center_on_browser()
        
        self.load_current_url()

    def load_current_url(self):
        try:
            with open('config/config.json', 'r') as file:
                config = json.load(file)
                self.url_input.setText(config.get('url', ''))
        except (FileNotFoundError, json.JSONDecodeError):
            self.url_input.setText('')

    def save_url(self):
        new_url = self.url_input.text()
        
        try:
            with open('config/config.json', 'r') as file:
                config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {}
        
        config['url'] = new_url
        
        with open('config/config.json', 'w') as file:
            json.dump(config, file, indent=4)
    
        self.browser.setUrl(QUrl(new_url))
        
        self.accept()

    def center_on_browser(self):
        """Centre la boîte de dialogue sur la fenêtre du navigateur."""
        if self.browser:
            # Obtenez les dimensions de la fenêtre principale
            main_window_rect = self.browser.parent().geometry()
            main_window_center = main_window_rect.center()

            # Obtenez les dimensions de la boîte de dialogue
            dialog_rect = self.geometry()
            dialog_width = dialog_rect.width()
            dialog_height = dialog_rect.height()

            # Calculez la position de la boîte de dialogue
            x = main_window_center.x() - dialog_width // 2
            y = main_window_center.y() - dialog_height // 2

            # Définissez la nouvelle position de la boîte de dialogue
            self.move(x, y)