"""
File        : mainwindow_worker.py
Author      : Silous
Created on  : 2025-04-22
Description : Worker for the main window to handle background tasks.
"""


# == Imports ==================================================================

from PyQt5.QtCore import QObject, pyqtSignal

from checkfrench.script.process import process_file


# == Classes ==================================================================

class WorkerMainWindow(QObject):
    """Worker for the main window to handle background tasks."""

    signal_run_process_start = pyqtSignal(str, str, str)
    signal_run_process_finished = pyqtSignal()

    def __init__(self) -> None:
        """Initialize the WorkerMainWindow."""
        super().__init__()

    def run_process(self, filepath: str, project_name: str, argument_parser: str) -> None:
        """Run the file processing in a separate thread.
        Args:
            filepath (str): The path to the file to process.
            project_name (str): The name of the project.
            argument_parser (str): The parser to use for processing.
        """

        process_file(filepath, project_name, argument_parser)
        self.signal_run_process_finished.emit()
