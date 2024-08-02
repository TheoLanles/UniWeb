from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from find_popup import *
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

        clear_cache_shortcut = QShortcut(QKeySequence('Ctrl+Shift+R'), self.browser)
        clear_cache_shortcut.activated.connect(self.clear_cache_and_cookies)

        mute_audio_shortcut = QShortcut(QKeySequence('Ctrl+Shift+M'), self.browser)
        mute_audio_shortcut.activated.connect(self.toggle_audio_mute)

        zoom_in_shortcut = QShortcut(QKeySequence('Ctrl++'), self.browser)
        zoom_in_shortcut.activated.connect(self.zoom_in)
        
        zoom_out_shortcut = QShortcut(QKeySequence('Ctrl+-'), self.browser)
        zoom_out_shortcut.activated.connect(self.zoom_out)

        find_shortcut = QShortcut(QKeySequence('Ctrl+F'), self.browser)
        find_shortcut.activated.connect(self.open_find_popup)

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

    def clear_cache_and_cookies(self):
        profile = QWebEngineProfile.defaultProfile()
        profile.clearHttpCache()
        profile.cookieStore().deleteAllCookies()
        print("Cache et cookies vidés.")

    def toggle_audio_mute(self):
        page = self.browser.page()
        is_muted = page.isAudioMuted()
        page.setAudioMuted(not is_muted)
        print("Audio muted" if not is_muted else "Audio unmuted")

    def zoom_in(self):
        current_zoom = self.browser.zoomFactor()
        new_zoom = current_zoom + 0.1
        self.browser.setZoomFactor(new_zoom)
        print(f"Zoom avant: {int(new_zoom * 100)}%")
    
    def zoom_out(self):
        current_zoom = self.browser.zoomFactor()
        new_zoom = current_zoom - 0.1
        self.browser.setZoomFactor(new_zoom)
        print(f"Zoom arrière: {int(new_zoom * 100)}%")

    def open_find_popup(self):
        popup = FindPopup(self.browser)
        popup.exec_()