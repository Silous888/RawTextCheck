"""
File        : messagebox.py
Author      : Silous
Created on  : 2025-08-24
Description : Module for displaying popup message boxes.

This module provides a Popup class with static methods to
show different types of message boxes.
(info, warning, error, question).
"""


# == Imports ==================================================================

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget


# == Classes ==================================================================

class Popup:
    @staticmethod
    def info(parent: QWidget | None, title: str, message: str) -> None:
        QMessageBox.information(parent, title, message)

    @staticmethod
    def warning(parent: QWidget | None, title: str, message: str) -> None:
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def error(parent: QWidget | None, title: str, message: str) -> None:
        QMessageBox.critical(parent, title, message)

    @staticmethod
    def question(parent: QWidget | None, title: str, message: str) -> bool:
        reply: QMessageBox.StandardButton = QMessageBox.question(
            parent,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # type: ignore
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes


class PopupManager(QObject):
    show_error = pyqtSignal(str, str)  # title, message


popup_manager = PopupManager()
