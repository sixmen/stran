from PySide6.QtCore import QFile
import resources.scripts

file = QFile(":translator.js")
file.open(QFile.ReadOnly)
translator_script = file.readAll().data().decode("utf8")
file.close()
