"""
File        : mainwindow_worker.py
Author      : Silous
Created on  : 2025-04-22
Description : Worker for the main window to handle background tasks.
"""


# == Imports ==================================================================

from PyQt5.QtCore import QObject


# == Classes ==================================================================

class WorkerMainWindow(QObject):
    """Worker for the main window to handle background tasks."""

    def __init__(self) -> None:
        """Initialize the WorkerMainWindow."""
        super().__init__()
