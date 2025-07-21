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

from checkfrench.script import json_config


# == Main Application =========================================================

if __name__ == "__main__":

    # create qt application
    translator = QTranslator()

    app = QApplication(sys.argv)

    if translator.load(json_config.load_data()["language"] + ".qm", "translations/"):
        app.installTranslator(translator)

    # Imports where translator neeed to be initialized before
    from checkfrench.ui.mainwindow.mainwindow import MainWindow
    from checkfrench.script import json_projects

    json_config.create_json()
    json_projects.create_json()

    program = MainWindow()

    program.show()
    sys.exit(app.exec())
