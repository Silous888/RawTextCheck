"""
File        : main.py
Author      : Silous
Created on  : 2025-04-18
Description : Main entry point for the application.

This script initializes the application, sets up the main window, and starts the Qt event loop.
"""


# == Imports ==================================================================

import sys

from PyQt5.QtWidgets import QApplication

from checkfrench.script import json_config, json_projects
from checkfrench.ui.mainwindow.mainwindow import MainWindow

# == Main Application =========================================================

if __name__ == "__main__":

    json_config.create_json()
    json_projects.create_json()

    # create qt application
    app = QApplication(sys.argv)
    program = MainWindow()

    program.show()
    sys.exit(app.exec())
