"""
File        : create_project_model.py
Author      : Silous
Created on  : 2025-06-09
Description : Model for creating a new project in the application.

This module defines the model for creating a new project, including the
language selection and project creation logic.
"""


# == Imports ==================================================================

# -------------------- Import Lib Tier -------------------
from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt

# -------------------- Import Lib User -------------------

from rawtextcheck.default_parameters import (
    DEFAULT_LANGUAGE,
    DEFAULT_PARSER,
    DEFAULT_VALID_ALPHANUMERIC,
    DEFAULT_VALID_PUNCTUATION,
    DEFAULT_VALID_SPACE,
    LANGUAGES_LANGUAGETOOL
)
from rawtextcheck.script import json_projects, parser_loader


# == Classes ==================================================================

class CreateProjectModel():
    """Model for creating a new project.
    This class handles the initialization of the language combo box model and
    provides methods to create a new project.
    Attributes:
        languageComboBoxModel (LanguagesComboBoxModel): The model for the
        language combo box.
    """

    def __init__(self) -> None:
        """Initialize the CreateProjectModel."""
        self.model_start()

    def model_start(self) -> None:
        """Initialize the language combo box model."""
        self.languageComboBoxModel = LanguagesComboBoxModel(LANGUAGES_LANGUAGETOOL)
        self.parserComboBoxModel = ParserComboBoxModel(list(parser_loader.get_all_parsers().keys()))

    def create_project(self, project_name: str, language_code: str, parser: str) -> None:
        """Create a new project with the given name and language code.
        Args:
            project_name (str): The name of the project to create.
            language_code (str): The language code for the project.
            parser (str): The parser for the project
        """
        if not project_name or not language_code or not parser:
            return

        json_projects.create_new_entry(project_name, language_code, parser)

        json_projects.add_valid_characters(project_name, DEFAULT_VALID_ALPHANUMERIC +
                                           DEFAULT_VALID_PUNCTUATION + DEFAULT_VALID_SPACE)

    def is_project_name_valid(self, project_name: str) -> bool:
        return not json_projects.is_project_name_exist(project_name)


class LanguagesComboBoxModel(QAbstractListModel):
    """Model for the language combo box in the project creation dialog.
    This model provides a list of languages sorted by their labels and
    allows retrieval of language codes and labels.
    """
    def __init__(self, data: list[tuple[str, str]], parent: QAbstractListModel | None = None) -> None:
        """Initialize the LanguagesComboBoxModel with the provided data.
        Args:
            data (list[tuple[str, str]]): A list of tuples containing language codes and labels.
            parent (QAbstractListModel | None): The parent model, if any.
        """
        super().__init__(parent)
        self._data: list[tuple[str, str]] = sorted(data, key=lambda x: x[1].lower())

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of rows in the model."""
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        """Return the data for the given index and role.
        Args:
            index (QModelIndex): The index for which to retrieve data.
            role (int): The role of the data to retrieve (e.g., DisplayRole, UserRole).
        Returns:
            QVariant | str: The data for the specified index and role.
        """
        if not index.isValid() or not (0 <= index.row() < len(self._data)):
            return QVariant()

        code, label = self._data[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return label
        if role == Qt.ItemDataRole.UserRole:
            return code

        return QVariant()

    def get_code(self, row: int) -> str:
        """Get the language code for the specified row.
        Args:
            row (int): The row index for which to retrieve the language code.
        Returns:
            str: The language code for the specified row, or an empty string if the row is invalid.
        """
        if 0 <= row < len(self._data):
            return self._data[row][0]
        return ""

    def get_label(self, row: int) -> str:
        """Get the language label for the specified row.
        Args:
            row (int): The row index for which to retrieve the language label.
        Returns:
            str: The language label for the specified row, or an empty string if the row is invalid.
        """
        if 0 <= row < len(self._data):
            return self._data[row][1]
        return ""

    def get_index_by_code(self, code: str) -> int:
        """Get the index of the language with the specified code.
        Args:
            code (str): The language code to search for.
        Returns:
            int: The index of the language with the specified code, or -1 if not found.
        """
        for i, (c, _) in enumerate(self._data):
            if c == code:
                return i
        return -1

    def get_default_index(self) -> int:
        """Get the default index for the language combo box."""
        return self.get_index_by_code(DEFAULT_LANGUAGE)


class ParserComboBoxModel(QAbstractListModel):
    """Model
    Attributes:
        _data (list[tuple[str, str]]): A list of tuples containing language codes and labels.
    """

    def __init__(self, data: list[str], parent: QAbstractListModel | None = None) -> None:
        """Initialize the LanguagesComboBoxModel with the provided data.
        Args:
            data (list[tuple[str, str]]): A list of tuples containing language codes and labels.
            parent (QAbstractListModel | None): The parent model, if any.
        """
        super().__init__(parent)
        self._data: list[str] = data

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of rows in the model.
        Args:
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            int: The number of projects in the model.
        """
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        """Return the data for the given index and role.
        Args:
            index (QModelIndex): The index for which to retrieve data.
            role (int): The role of the data to retrieve (e.g., DisplayRole).
        Returns:
            QVariant | str: The data for the specified index and role.
        """
        if not index.isValid() or index.row() >= len(self._data):
            return QVariant()

        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()]

        return QVariant()

    def get_value(self, index: int) -> str | None:
        """Get the project name for the specified index.
        Args:
            index (int): The index of the project in the combobox.
        Returns:
            str | None: The project name for the specified index, or None if the index is invalid.
        """
        if 0 <= index < len(self._data):
            return self._data[index]
        return None

    def get_default_index(self) -> int:
        """Get the default index for the parser combo box."""
        return self._data.index(DEFAULT_PARSER)
