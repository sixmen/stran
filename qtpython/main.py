from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from browser import Browser
import resources.icons

if __name__ == "__main__":
    app = QApplication([])
    browser = Browser()
    browser.create_window()
    sys.exit(app.exec())
