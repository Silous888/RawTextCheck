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

from checkfrench import startup


# == Main Application =========================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    startup.create_folders()
    startup.create_json_config()

    translator: QTranslator | None = startup.init_translator()
    if translator is not None:
        app.installTranslator(translator)

    startup.create_json_projects()

    # Imports where translator neeed to be initialized before
    from checkfrench.ui.mainwindow.mainwindow import MainWindow

    program = MainWindow()

    program.show()
    sys.exit(app.exec())
