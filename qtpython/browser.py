from __future__ import annotations

from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtCore import QObject

from browserwindow import BrowserWindow


class Browser(QObject):
    _windows: list[BrowserWindow]
    _profile: QWebEngineProfile | None

    def __init__(self):
        super().__init__()
        self._windows = []
        self._profile = None

    def create_window(self):
        profile = self._profile
        if not self._profile:
            profile = self._profile = QWebEngineProfile("stran")

        new_window = BrowserWindow(self, profile)
        self._windows.append(new_window)
        new_window.about_to_close.connect(self._remove_window)
        new_window.show()
        return new_window

    def _remove_window(self):
        w = self.sender()
        if w in self._windows:
            del self._windows[self._windows.index(w)]
