from PySide6.QtCore import QObject
from PySide6.QtCore import Slot
from PySide6.QtCore import QFile
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
import json
import requests
from settings import get_settings, API_KEY, TARGET_LANG
import resources.scripts


class TranslatorWorker(QThread):
    result = Signal(str)

    def __init__(self, text: str, api_key: str, target_lang: str):
        super().__init__()
        self._text = text
        self._api_key = api_key
        self._target_lang = target_lang

    def run(self):
        languages = {
            "ko": "한국어",
            "en": "English",
            "ja": "日本語",
            "zh": "中文",
            "es": "Español",
            "fr": "Français",
            "de": "Deutsch",
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._api_key}",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are a translator. Translate the given text to {languages[self._target_lang]}. Only respond with the translated text, without any additional explanation or context.",
                        },
                        {
                            "role": "user",
                            "content": self._text,
                        },
                    ],
                },
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()
            translated_text = data["choices"][0]["message"]["content"].strip()

            self.result.emit(
                json.dumps({"worker": id(self), "translated_text": translated_text})
            )
        except Exception as e:
            self.result.emit(json.dumps({"worker": id(self), "error": str(e)}))


class TranslatorBridge(QObject):
    translationComplete = Signal(str)
    _workers: list[TranslatorWorker]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._workers = []

    @Slot(str, result=str)
    def translate(self, text):
        if not text:
            return json.dumps({"error": "No text provided"})

        settings = get_settings()
        api_key = settings.value(API_KEY, "")
        target_lang = settings.value(TARGET_LANG, "ko")
        if not api_key:
            return json.dumps({"error": "No API key provided"})

        worker = TranslatorWorker(text, api_key, target_lang)
        worker.result.connect(self.translationComplete.emit)
        worker.finished.connect(lambda: self._workers.remove(worker))
        self._workers.append(worker)
        worker.start()
        return json.dumps({"worker": id(worker)})


file = QFile(":/qtwebchannel/qwebchannel.js")
file.open(QFile.ReadOnly)
qwebchannel_script = file.readAll().data().decode("utf8")
file.close()

file = QFile(":translator.js")
file.open(QFile.ReadOnly)
translator_script = file.readAll().data().decode("utf8")
file.close()
