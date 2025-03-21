from __future__ import annotations
from typing import TYPE_CHECKING, cast
from functools import partial

from PySide6.QtCore import Signal
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMessageBox

from settings import get_api_key
from translator import TranslatorBridge

if TYPE_CHECKING:
    from PySide6.QtGui import QAction
    from browserwindow import BrowserWindow


class BrowserWebView(QWebEngineView):
    web_action_enabled_changed = Signal(QWebEnginePage.WebAction, bool)
    translation_enabled_changed = Signal(bool)
    _translation_enabled: bool = False

    def __init__(self, profile: QWebEngineProfile):
        super().__init__(profile)

        self._connect_webaction_changed(self.page(), QWebEnginePage.WebAction.Forward)
        self._connect_webaction_changed(self.page(), QWebEnginePage.WebAction.Back)
        self.loadFinished.connect(self._on_load_finished)

        self._channel = QWebChannel(self)
        self._channel.registerObject("translator", TranslatorBridge(self))
        self.page().setWebChannel(self._channel)

    def _connect_webaction_changed(
        self, page: QWebEnginePage, web_action: QWebEnginePage.WebAction
    ):
        action = page.action(web_action)
        action.changed.connect(
            partial(self._emit_webactionenabledchanged, action, web_action)
        )

    def _emit_webactionenabledchanged(
        self, action: QAction, web_action: QWebEnginePage.WebAction
    ):
        self.web_action_enabled_changed.emit(web_action, action.isEnabled())

    def _on_load_finished(self):
        self._send_translation_state_changed()

    def is_web_action_enabled(self, web_action: QWebEnginePage.WebAction):
        return self.page().action(web_action).isEnabled()

    def toggle_translation(self):
        api_key = get_api_key()
        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter an API key")
            return
        self._translation_enabled = not self._translation_enabled
        self._send_translation_state_changed()
        self.translation_enabled_changed.emit(self._translation_enabled)

    def _send_translation_state_changed(self):
        self.page().runJavaScript(
            f"window.dispatchEvent(new CustomEvent('translationStateChanged', {{ detail: {{ enabled: {str(self._translation_enabled).lower()} }} }}));"
        )

    def is_translation_enabled(self):
        return self._translation_enabled

    def createWindow(self, type: QWebEnginePage.WebWindowType) -> QWebEngineView | None:  # type: ignore
        main_window = cast(BrowserWindow, self.window())
        if not main_window:
            return None

        if type == QWebEnginePage.WebWindowType.WebBrowserTab:
            return main_window.tab_widget().create_tab()

        if type == QWebEnginePage.WebWindowType.WebBrowserBackgroundTab:
            return main_window.tab_widget().create_tab(False)

        if type == QWebEnginePage.WebWindowType.WebBrowserWindow:
            return main_window.browser().create_window().current_tab()

        return None
