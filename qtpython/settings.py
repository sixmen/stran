from __future__ import annotations

from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSettings

API_KEY = "api_key"
TARGET_LANG = "target_lang"


def get_settings():
    settings = QSettings("sixmen", "S-Tran")
    if not settings.contains(API_KEY):
        settings.setValue(API_KEY, "")
    if not settings.contains(TARGET_LANG):
        settings.setValue(TARGET_LANG, "ko")
    return settings


def get_api_key():
    settings = get_settings()
    return settings.value(API_KEY, "")


class SettingsDialog(QDialog):
    _settings: QSettings
    _api_key_input: QLineEdit
    _target_lang_select: QComboBox
    _save_button: QPushButton
    _cancel_button: QPushButton

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setWindowTitle("S-Tran Settings")
        self.resize(400, 200)

        self._settings = get_settings()
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        api_key_layout = QVBoxLayout()
        api_key_label = QLabel("OpenAI API Key:")
        self._api_key_input = QLineEdit()
        self._api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._api_key_input.setPlaceholderText("Enter your OpenAI API key")
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self._api_key_input)
        layout.addLayout(api_key_layout)

        target_lang_layout = QVBoxLayout()
        target_lang_label = QLabel("Target Language:")
        self._target_lang_select = QComboBox()
        self._target_lang_select.addItem("한국어", "ko")
        self._target_lang_select.addItem("English", "en")
        self._target_lang_select.addItem("日本語", "ja")
        self._target_lang_select.addItem("中文", "zh")
        self._target_lang_select.addItem("Español", "es")
        self._target_lang_select.addItem("Français", "fr")
        self._target_lang_select.addItem("Deutsch", "de")
        target_lang_layout.addWidget(target_lang_label)
        target_lang_layout.addWidget(self._target_lang_select)
        layout.addLayout(target_lang_layout)

        button_layout = QHBoxLayout()
        self._save_button = QPushButton("Save")
        self._cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self._save_button)
        button_layout.addWidget(self._cancel_button)
        layout.addLayout(button_layout)

        self._save_button.clicked.connect(self._save_settings)
        self._cancel_button.clicked.connect(self.reject)

    def _load_settings(self):
        api_key = self._settings.value(API_KEY, "")
        self._api_key_input.setText(api_key)

        target_lang = self._settings.value(TARGET_LANG, "ko")
        index = self._target_lang_select.findData(target_lang)
        if index >= 0:
            self._target_lang_select.setCurrentIndex(index)

    def _save_settings(self):
        api_key = self._api_key_input.text().strip()
        target_lang = self._target_lang_select.currentData()

        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter an API key")
            return

        self._settings.setValue(API_KEY, api_key)
        self._settings.setValue(TARGET_LANG, target_lang)

        QMessageBox.information(self, "Success", "Settings saved successfully!")
        self.accept()
