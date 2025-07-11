"""
File        : project_manager_worker.py
Author      : Silous
Created on  : 2025-05-29
Description : Worker for project_manager dialog.
"""


# == Imports ==================================================================

from PyQt5.QtCore import QObject


# == Classes ==================================================================

class WorkerProjectManager(QObject):
    """Worker for the project manager dialog."""

    def __init__(self) -> None:
        """Initialize the WorkerProjectManager."""
        super().__init__()
