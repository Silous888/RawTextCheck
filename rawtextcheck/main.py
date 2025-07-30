"""
File        : main.py
Author      : Silous
Created on  : 2025-04-18
Description : Main entry point for the application.

This script initializes the application, sets up the main window, and starts the Qt event loop.
"""


# == Imports ==================================================================

import sys

from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication

from rawtextcheck import startup_translation


# == Main Application =========================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    translator: QTranslator | None = startup_translation.init_translator()
    if translator is not None:
        app.installTranslator(translator)

    # Imports where translator neeed to be initialized before
    from rawtextcheck import startup
    from rawtextcheck.ui.mainwindow.mainwindow import MainWindow

    startup.startup_everything()

    program = MainWindow()

    program.show()
    sys.exit(app.exec())
