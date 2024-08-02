import ctypes as ct
import winreg
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer

def get_windows_theme():
    """
    Retourne 'dark' si le thème Windows est sombre, 'light' sinon.
    """
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
            value, _ = winreg.QueryValueEx(key, "SystemUsesLightTheme")
            return 'light' if value == 1 else 'dark'
    except Exception as e:
        print(f"Erreur lors de la récupération du thème Windows : {e}")
        return 'light'

def apply_theme(window: QMainWindow, theme: str):
    """
    Applique le thème à la fenêtre principale.
    :param window: Instance de QMainWindow
    :param theme: 'dark' ou 'light'
    """
    if theme == 'dark':
        dark_title_bar(window)
    else:
        light_title_bar(window)

def dark_title_bar(window: QMainWindow):
    """
    Applique le mode sombre à la barre de titre de la fenêtre sous Windows 10.
    :param window: Instance de QMainWindow
    """
    window.update()
    
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19
    
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute

    hwnd = window.winId()
    hwnd = int(hwnd) 
    hwnd = ct.c_void_p(hwnd)  
    
    value = ct.c_int(2)  
    
    if ct.windll.dwmapi.DwmIsCompositionEnabled(ct.byref(ct.c_int())):
        set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ct.byref(value), ct.sizeof(value))
    else:
        set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1, ct.byref(value), ct.sizeof(value))

def light_title_bar(window: QMainWindow):
    """
    Réinitialise la barre de titre à un mode clair sous Windows 10.
    :param window: Instance de QMainWindow
    """
    window.update()
    
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute

    hwnd = window.winId()
    hwnd = int(hwnd) 
    hwnd = ct.c_void_p(hwnd) 
    
    value = ct.c_int(0)
    
    if ct.windll.dwmapi.DwmIsCompositionEnabled(ct.byref(ct.c_int())):
        set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ct.byref(value), ct.sizeof(value))

def monitor_theme_changes(window: QMainWindow):
    current_theme = get_windows_theme()
    apply_theme(window, current_theme)
    
    def check_theme_change():
        nonlocal current_theme
        new_theme = get_windows_theme()
        if new_theme != current_theme:
            current_theme = new_theme
            apply_theme(window, current_theme)

    timer = QTimer(window)
    timer.timeout.connect(check_theme_change)
    timer.start(1000)
