import sys
from ocr_translator_gui import TranslatorGUI
from PyQt5.QtWidgets import QApplication

# driver for OCR Translator App
app = QApplication(sys.argv)
window = TranslatorGUI()
sys.exit(app.exec_())