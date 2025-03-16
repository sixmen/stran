from __future__ import annotations
from typing import TYPE_CHECKING
from functools import partial

from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWidgets import QTabWidget
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal

from browserwebview import BrowserWebView

if TYPE_CHECKING:
    from browserwindow import BrowserWindow


class BrowserTabWidget(QTabWidget):
    _profile: QWebEngineProfile
    title_changed = Signal(str)
    url_changed = Signal(QUrl)
    close_window = Signal()
    web_action_enabled_changed = Signal(QWebEnginePage.WebAction, bool)
    translation_enabled_changed = Signal(bool)

    def __init__(self, parent: BrowserWindow, profile: QWebEngineProfile):
        super().__init__(parent)

        self._profile = profile

        tab_bar = self.tabBar()
        tab_bar.setTabsClosable(True)
        tab_bar.setMovable(True)
        tab_bar.tabCloseRequested.connect(self.close_tab)

        self.setDocumentMode(True)
        self.setElideMode(Qt.TextElideMode.ElideRight)
        self.currentChanged.connect(self._handle_current_changed)

    def create_tab(self, background=False):
        web_view = BrowserWebView(self._profile)
        web_view.titleChanged.connect(partial(self._title_changed, web_view))
        web_view.urlChanged.connect(partial(self._url_changed, web_view))
        web_view.web_action_enabled_changed.connect(
            partial(self._handle_web_action_enabled_changed, web_view)
        )
        web_view.translation_enabled_changed.connect(
            partial(self._handle_translation_enabled_changed, web_view)
        )
        web_page = web_view.page()
        web_page.windowCloseRequested.connect(
            partial(self._window_close_requested, web_view)
        )

        self.addTab(web_view, "New Tab")
        if not background:
            self.setCurrentWidget(web_view)
        return web_view

    def current_web_view(self) -> BrowserWebView:
        return self._web_view(self.currentIndex())

    def close_tab(self, index: int):
        web_view = self._web_view(index)
        if web_view:
            self.removeTab(index)
            if self.count() == 0:
                self.close_window.emit()
            web_view.deleteLater()

    def set_url(self, url: str):
        current_web_view = self.current_web_view()
        if current_web_view:
            current_web_view.setUrl(url)

    def trigger_web_page_action(self, action: QWebEnginePage.WebAction):
        current_web_view = self.current_web_view()
        if current_web_view:
            current_web_view.triggerPageAction(action)

    def _web_view(self, index: int) -> BrowserWebView | None:
        return self.widget(index)

    def _title_changed(self, web_view: BrowserWebView, title: str):
        index = self.indexOf(web_view)
        if index >= 0:
            self.setTabText(index, title)
            self.setTabToolTip(index, title)

        # update the title of the window if 'web_view' is the current tab
        if self.currentIndex() == index:
            self.title_changed.emit(title)

    def _url_changed(self, web_view: BrowserWebView, url: str):
        index = self.indexOf(web_view)

        # update the url input text of the window if 'web_view' is the current tab
        if self.currentIndex() == index:
            self.url_changed.emit(url)

    def _handle_web_action_enabled_changed(
        self, web_view: BrowserWebView, action: QWebEnginePage.WebAction, enabled: bool
    ):
        index = self.indexOf(web_view)

        # update the enabled state of navigation buttons if 'web_view' is the current tab
        if self.currentIndex() == index:
            self.web_action_enabled_changed.emit(action, enabled)

    def _handle_translation_enabled_changed(
        self, web_view: BrowserWebView, enabled: bool
    ):
        index = self.indexOf(web_view)
        if self.currentIndex() == index:
            self.translation_enabled_changed.emit(enabled)

    def _window_close_requested(self, web_view: BrowserWebView):
        index = self.indexOf(web_view)
        if index >= 0:
            self.close_tab(index)

    def _handle_current_changed(self, index: int):
        if index >= 0:
            current_web_view = self._web_view(index)
            self.title_changed.emit(current_web_view.title())
            self.url_changed.emit(current_web_view.url())
            self.web_action_enabled_changed.emit(
                QWebEnginePage.WebAction.Back,
                current_web_view.is_web_action_enabled(QWebEnginePage.WebAction.Back),
            )
            self.web_action_enabled_changed.emit(
                QWebEnginePage.WebAction.Forward,
                current_web_view.is_web_action_enabled(
                    QWebEnginePage.WebAction.Forward
                ),
            )
            self.translation_enabled_changed.emit(
                current_web_view.is_translation_enabled()
            )
        else:
            self.title_changed.emit("")
            self.url_changed.emit(QUrl())
            self.web_action_enabled_changed.emit(QWebEnginePage.Back, False)
            self.web_action_enabled_changed.emit(QWebEnginePage.Forward, False)
            self.translation_enabled_changed.emit(False)
