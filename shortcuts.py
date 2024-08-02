from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
class Shortcuts:
    def __init__(self, browser, url_popup_class):
        self.browser = browser
        self.url_popup_class = url_popup_class 
        self.create_shortcuts()

    def create_shortcuts(self):
        reload_shortcut = QShortcut(QKeySequence('Ctrl+R'), self.browser)
        reload_shortcut.activated.connect(self.reload_page)
        
        back_shortcut = QShortcut(QKeySequence('Left'), self.browser)
        back_shortcut.activated.connect(self.go_back)
        
        forward_shortcut = QShortcut(QKeySequence('Right'), self.browser)
        forward_shortcut.activated.connect(self.go_forward)
        
        popup_shortcut = QShortcut(QKeySequence('Ctrl+,'), self.browser)
        popup_shortcut.activated.connect(self.open_url_popup)

    def reload_page(self):
        self.browser.reload()

    def go_back(self):
        if self.browser.history().canGoBack():
            self.browser.back()

    def go_forward(self):
        if self.browser.history().canGoForward():
            self.browser.forward()

    def open_url_popup(self):
        popup = self.url_popup_class(self.browser)
        popup.exec_()
