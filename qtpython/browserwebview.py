from __future__ import annotations
from typing import TYPE_CHECKING
from functools import partial

from PySide6.QtCore import Signal
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView

if TYPE_CHECKING:
    from PySide6.QtGui import QAction
    from browserwindow import BrowserWindow


class BrowserWebView(QWebEngineView):
    web_action_enabled_changed = Signal(QWebEnginePage.WebAction, bool)

    def __init__(self, profile: QWebEngineProfile):
        super().__init__(profile)

        self._connect_webaction_changed(self.page(), QWebEnginePage.WebAction.Forward)
        self._connect_webaction_changed(self.page(), QWebEnginePage.WebAction.Back)

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

    def is_web_action_enabled(self, web_action: QWebEnginePage.WebAction):
        return self.page().action(web_action).isEnabled()

    def createWindow(self, type: QWebEnginePage.WebWindowType) -> QWebEngineView | None:
        main_window: BrowserWindow = self.window()
        if not main_window:
            return None

        if type == QWebEnginePage.WebWindowType.WebBrowserTab:
            return main_window.tab_widget().create_tab()

        if type == QWebEnginePage.WebWindowType.WebBrowserBackgroundTab:
            return main_window.tab_widget().create_tab(False)

        if type == QWebEnginePage.WebWindowType.WebBrowserWindow:
            return main_window.browser().create_window().current_tab()

        return None
