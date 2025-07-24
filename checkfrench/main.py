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


import os


def translations_path(relative_path: str) -> str:
    """Get the absolute path to a translation file.
    This function handles both development and PyInstaller environments.
    Args:
        relative_path (str): The relative path to the translation file.
    Returns:
        str: The absolute path to the translation file.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: resource is in the _internal folder
        base_path: str = sys._MEIPASS  # type: ignore
        return os.path.join(base_path, 'translations', relative_path)  # type: ignore
    else:
        # Dev: resource is in local 'translations' directory
        return os.path.join('translations', relative_path)


# == Main Application =========================================================

if __name__ == "__main__":

    translator = QTranslator()

    app = QApplication(sys.argv)

    json_config.create_json()
    if translator.load(translations_path(json_config.load_data()["language"] + ".qm")):
        app.installTranslator(translator)

    # Imports where translator neeed to be initialized before
    from checkfrench.ui.mainwindow.mainwindow import MainWindow
    from checkfrench.script import json_projects

    json_projects.create_json()

    program = MainWindow()

    program.show()
    sys.exit(app.exec())
