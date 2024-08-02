from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
import json
from windows_theme_manager import dark_title_bar, light_title_bar, get_windows_theme, apply_theme

class UrlPopup(QDialog):
    def __init__(self, browser, parent=None):
        super().__init__(parent)
        self.browser = browser  # Référence au navigateur
        self.setWindowTitle("Modifier l'URL")
        self.setWindowIcon(QIcon('icon/icon.png'))
        self.setFixedSize(300, 150)  # Taille fixe pour la popup

        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowSystemMenuHint)

        theme = get_windows_theme()
        apply_theme(self, theme)
        
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Entrez l'URL...")
        
        self.save_button = QPushButton("Sauvegarder", self)
        self.save_button.clicked.connect(self.save_url)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("URL actuelle :"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        
        self.load_current_url()

    def load_current_url(self):
        """Charge l'URL actuelle depuis le fichier config.json."""
        try:
            with open('config/config.json', 'r') as file:
                config = json.load(file)
                self.url_input.setText(config.get('url', ''))
        except (FileNotFoundError, json.JSONDecodeError):
            self.url_input.setText('')

    def save_url(self):
        """Sauvegarde l'URL dans le fichier config.json et recharge la page."""
        new_url = self.url_input.text()
        
        # Sauvegarder l'URL dans le fichier config.json
        try:
            with open('config/config.json', 'r') as file:
                config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {}
        
        config['url'] = new_url
        
        with open('config/config.json', 'w') as file:
            json.dump(config, file, indent=4)
        
        # Recharger la page avec la nouvelle URL
        self.browser.setUrl(QUrl(new_url))
        
        # Fermer la popup
        self.accept()
