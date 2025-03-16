from __future__ import annotations

from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWebEngineCore import QWebEngineScript
from PySide6.QtCore import QObject

from browserwindow import BrowserWindow
from translator import qwebchannel_script, translator_script


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
            profile = self._profile = self._create_profile()

        new_window = BrowserWindow(self, profile)
        self._windows.append(new_window)
        new_window.about_to_close.connect(self._remove_window)
        new_window.show()
        return new_window

    def _create_profile(self):
        profile = QWebEngineProfile("stran")

        script = QWebEngineScript()
        script.setSourceCode(qwebchannel_script + translator_script)
        script.setName("translator.js")
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
        profile.scripts().insert(script)

        return profile

    def _remove_window(self):
        w = self.sender()
        if w in self._windows:
            del self._windows[self._windows.index(w)]
