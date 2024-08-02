from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from windows_theme_manager import get_windows_theme, apply_theme, monitor_theme_changes
from PyQt5.QtGui import QIcon

class FindPopup(QDialog):
    def __init__(self, browser, parent=None):
        super().__init__(parent)
        self.browser = browser
        self.setWindowTitle("Search on page")
        self.setFixedSize(300, 150)  # Taille fixe pour la popup
        self.setWindowIcon(QIcon('icon/icon.png'))

        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowSystemMenuHint)

        apply_theme(self, get_windows_theme())
        monitor_theme_changes(self)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter the text to be searched...")

        self.search_button = QPushButton("Find", self)
        self.search_button.clicked.connect(self.search_text)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Text to search for :"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.search_button)
        self.setLayout(layout)

        self.center_on_browser()

    def search_text(self):
        search_text = self.url_input.text()
        if search_text:
            self.browser.page().findText(search_text)
            print(f"Recherche de: {search_text}")
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
