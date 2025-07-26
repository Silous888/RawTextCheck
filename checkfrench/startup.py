"""
File        : startup.py
Author      : Silous
Created on  : 2025-07-26
Description : Startup module for the CheckFrench application.

This module handles the initialization of the application,
including creating necessary folders, creating JSON configuration
files, and setting up translations.
"""

import os
import sys

from PyQt5.QtCore import QTranslator

from checkfrench.default_parameters import RESULTS_FOLDER, PLUGIN_PARSER_FOLDER
from checkfrench.script import json_config, json_projects


def create_json_config() -> None:
    """Create the JSON configuration file if it does not exist."""
    json_config.create_json()


def create_json_projects() -> None:
    """Create the JSON projects file if it does not exist."""
    json_projects.create_json()


def create_folders() -> None:
    """Create necessary folders for the application."""
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)
    if not os.path.exists(PLUGIN_PARSER_FOLDER):
        os.makedirs(PLUGIN_PARSER_FOLDER)


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


def init_translator() -> QTranslator | None:
    """Initialize the translator for the application.
    Returns:
        QTranslator | None: The translator object if successful, None otherwise.
    """
    translator = QTranslator()

    if translator.load(translations_path(json_config.load_data()["language"] + ".qm")):
        return translator
    return None
