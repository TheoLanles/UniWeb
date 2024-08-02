from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

class Shortcuts:
    def __init__(self, browser, url_popup_class):
        self.browser = browser
        self.url_popup_class = url_popup_class  # Classe de la popup à utiliser
        self.create_shortcuts()

    def create_shortcuts(self):
        # Crée un raccourci pour recharger la page (Ctrl + R)
        reload_shortcut = QShortcut(QKeySequence('Ctrl+R'), self.browser)
        reload_shortcut.activated.connect(self.reload_page)
        
        # Crée un raccourci pour naviguer en arrière (Flèche gauche)
        back_shortcut = QShortcut(QKeySequence('Left'), self.browser)
        back_shortcut.activated.connect(self.go_back)
        
        # Crée un raccourci pour naviguer en avant (Flèche droite)
        forward_shortcut = QShortcut(QKeySequence('Right'), self.browser)
        forward_shortcut.activated.connect(self.go_forward)
        
        # Crée un raccourci pour ouvrir la popup (Ctrl + ,)
        popup_shortcut = QShortcut(QKeySequence('Ctrl+,'), self.browser)
        popup_shortcut.activated.connect(self.open_url_popup)

    def reload_page(self):
        # Recharge la page actuelle
        self.browser.reload()

    def go_back(self):
        # Navigue en arrière dans l'historique
        if self.browser.history().canGoBack():
            self.browser.back()

    def go_forward(self):
        # Navigue en avant dans l'historique
        if self.browser.history().canGoForward():
            self.browser.forward()

    def open_url_popup(self):
        # Ouvre la popup pour modifier l'URL
        popup = self.url_popup_class(self.browser)
        popup.exec_()  # Affiche la popup en modal, bloquant l'interaction avec la fenêtre principale jusqu'à sa fermeture
