from __future__ import annotations
from typing import TYPE_CHECKING
import sys

from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QIcon
from PySide6.QtGui import QAction
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal

from browsertabwidget import BrowserTabWidget

if TYPE_CHECKING:
    from PySide6.QtWebEngineCore import QWebEngineProfile
    from browser import Browser


class BrowserWindow(QMainWindow):
    about_to_close = Signal()

    _browser: Browser
    _profile: QWebEngineProfile

    _toolbar: QToolBar
    _history_back_action: QAction
    _history_forward_action: QAction
    _url_line_edit: QLineEdit

    _tab_widget: BrowserTabWidget

    def __init__(self, browser: Browser, profile: QWebEngineProfile):
        super().__init__()

        self._browser = browser
        self._profile = profile

        menu_bar = self.menuBar()
        menu_bar.addMenu(self._create_file_menu())

        [
            self._toolbar,
            self._history_back_action,
            self._history_forward_action,
            self._url_line_edit,
        ] = self._create_tool_bar()
        self.addToolBar(self._toolbar)
        self.addToolBarBreak()

        self._tab_widget = self._create_tab_widget(profile)
        self.setCentralWidget(self._tab_widget)

        self._handle_web_view_title_changed("")
        self._tab_widget.create_tab()

        self.setGeometry(100, 100, 800, 600)

    def _create_tool_bar(self):
        navigation_bar = QToolBar("Navigation")
        navigation_bar.setMovable(False)

        history_back_action = QAction(self)
        history_back_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        history_back_action.triggered.connect(self._go_back)
        navigation_bar.addAction(history_back_action)

        history_forward_action = QAction(self)
        history_forward_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext))
        history_forward_action.triggered.connect(self._go_forward)
        navigation_bar.addAction(history_forward_action)

        url_line_edit = QLineEdit(self)
        url_line_edit.setClearButtonEnabled(True)
        navigation_bar.addWidget(url_line_edit)

        url_line_edit.returnPressed.connect(self._address_return_pressed)

        focus_url_line_edit_action = QAction(self)
        self.addAction(focus_url_line_edit_action)
        focus_url_line_edit_action.setShortcut(
            QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_L)
        )
        focus_url_line_edit_action.triggered.connect(self._focus_url_line_edit)

        return [
            navigation_bar,
            history_back_action,
            history_forward_action,
            url_line_edit,
        ]

    def _go_back(self):
        self._tab_widget.trigger_web_page_action(QWebEnginePage.WebAction.Back)

    def _go_forward(self):
        self._tab_widget.trigger_web_page_action(QWebEnginePage.WebAction.Forward)

    def _address_return_pressed(self):
        url = QUrl.fromUserInput(self._url_line_edit.text())
        self._tab_widget.set_url(url)

    def _focus_url_line_edit(self):
        self._url_line_edit.setFocus(Qt.FocusReason.ShortcutFocusReason)

    def _create_tab_widget(self, profile: QWebEngineProfile) -> BrowserTabWidget:
        tab_widget = BrowserTabWidget(self, profile)

        tab_widget.title_changed.connect(self._handle_web_view_title_changed)
        tab_widget.url_changed.connect(self._url_changed)
        tab_widget.web_action_enabled_changed.connect(
            self._handle_web_action_enabled_changed
        )
        tab_widget.close_window.connect(self.close)

        return tab_widget

    def _url_changed(self, url):
        self._url_line_edit.setText(url.toDisplayString())

    def _create_file_menu(self):
        file_menu = QMenu("File")
        file_menu.addAction(
            "&New Window",
            QKeySequence.StandardKey.New,
            self._new_window,
        )

        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcuts(QKeySequence.StandardKey.AddTab)
        new_tab_action.triggered.connect(self._new_tab)
        file_menu.addAction(new_tab_action)

        close_tab_action = QAction("Close Tab", self)
        close_tab_action.setShortcuts(QKeySequence.StandardKey.Close)
        close_tab_action.triggered.connect(self._close_current_tab)
        file_menu.addAction(close_tab_action)

        close_action = QAction("Quit", self)
        close_action.setShortcut(QKeySequence.StandardKey.Quit)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        return file_menu

    def _new_window(self):
        window = self._browser.create_window()
        window._url_line_edit.setFocus()

        current_geometry = self.geometry()
        window.setGeometry(
            current_geometry.x() + 20,
            current_geometry.y() + 20,
            current_geometry.width(),
            current_geometry.height(),
        )

    def _new_tab(self):
        self._tab_widget.create_tab()
        self._url_line_edit.setFocus()

    def _close_current_tab(self):
        self._tab_widget.close_tab(self._tab_widget.currentIndex())

    def _handle_web_action_enabled_changed(self, action, enabled):
        if action == QWebEnginePage.WebAction.Back:
            self._history_back_action.setEnabled(enabled)
        elif action == QWebEnginePage.WebAction.Forward:
            self._history_forward_action.setEnabled(enabled)

    def _handle_web_view_title_changed(self, title):
        suffix = "S-Tran"
        if title:
            self.setWindowTitle(f"{title} - {suffix}")
        else:
            self.setWindowTitle(suffix)

    def closeEvent(self, event):
        count = self._tab_widget.count()
        if count > 1:
            ret = QMessageBox.warning(
                self,
                "Confirm close",
                "Are you sure you want to close the window?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if ret == QMessageBox.StandardButton.No:
                event.ignore()
                return

        event.accept()
        self.about_to_close.emit()
        self.deleteLater()

    def tab_widget(self):
        return self._tab_widget

    def current_tab(self):
        return self._tab_widget.current_web_view()

    def browser(self) -> Browser:
        return self._browser
