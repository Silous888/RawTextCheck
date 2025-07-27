"""
File        : mainwindow_model.py
Author      : Silous
Created on  : 2025-06-15
Description : Model for the main window of the application.

This module defines the model for the main window, including the project title
combobox model and worker thread for background tasks.
"""


# == Imports ==================================================================

import os

# -------------------- Import Lib Tier -------------------
from PyQt5.QtCore import QAbstractListModel, QAbstractTableModel, QModelIndex, QThread, QVariant, Qt
from PyQt5.QtCore import QCoreApplication as QCA

# -------------------- Import Lib User -------------------
from rawtextcheck.default_parameters import (
    INVALID_CHAR_TEXT_ERROR_TYPE,
    BANWORD_TEXT_ERROR_TYPE,
    LANGUAGETOOL_SPELLING_CATEGORY,
)
from rawtextcheck.newtype import ItemProject, ItemResult
from rawtextcheck.script import json_projects, json_results, languagetool
from rawtextcheck.ui.mainwindow.mainwindow_worker import WorkerMainWindow


# == Classes ==================================================================

class MainWindowModel():
    """Model for the main window of the application.
    This class handles the initialization of the worker thread and the project title combobox model.
    Attributes:
        m_thread (QThread): The thread for running background tasks.
        m_worker (WorkerMainWindow): The worker for handling background tasks.
        titleCombobBoxModel (ProjectTitleComboBoxModel): The model for the project title combobox.
    """
    def __init__(self, project_name: str, filename: str) -> None:
        """Initialize the MainWindowModel."""
        self.worker_start()
        self.model_start(project_name, filename)

    def worker_start(self) -> None:
        """Initialize the worker thread and move the worker to it."""
        self.thread = QThread()
        self.thread.start()
        self.worker = WorkerMainWindow()
        self.worker.moveToThread(self.thread)

    def worker_stop(self) -> None:
        """Stop the worker thread if it is running."""
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

    def model_start(self, project_name: str, filename: str) -> None:
        """Initialize the project title combobox model."""
        self.titleComboBoxModel = ProjectTitleComboBoxModel()
        self.resultsTableModel = ResultsTableModel(project_name, filename)

    def model_stop(self) -> None:
        self.worker_stop()
        languagetool.close_tool()

    def get_argument_parser(self, index: int) -> str:
        """Get the argument parser for the selected project in the combobox.
        Args:
            index (int): The index of the selected project in the combobox.
        Returns:
            str: The argument parser for the selected project, or an empty string if not found.
        """
        project_name: str | None = self.titleComboBoxModel.get_value(index)
        if project_name is None:
            return ""
        data: ItemProject | None = json_projects.get_project_data(project_name)
        if data is None:
            return ""
        return data["arg_parser"]

    def is_file_exist(self, filepath: str) -> bool:
        """test if a filepath is correct
        Args:
            filepath (str): the path of the file
        Returns:
            bool: True if the path is a valid file
        """
        return os.path.isfile(filepath)

    def get_filename_from_filepath(self, filepath: str) -> str:
        """get the name of the file given its path
        Args:
            filepath (str): path of the file
        Returns:
            str: name of the file
        """
        return os.path.basename(filepath)

    def generate_result(self, filepath: str, project_name: str, argument_parser: str) -> None:

        self.worker.run_process(filepath, project_name, argument_parser)


class ProjectTitleComboBoxModel(QAbstractListModel):
    """Model for the project title combobox in the main window.
    This model provides a list of project names sorted alphabetically and allows retrieval of project names by index.
    Attributes:
        _projects (list[str]): The list of project names.
    """

    def __init__(self, parent: QAbstractListModel | None = None) -> None:
        """Initialize the ProjectTitleComboBoxModel.
        Args:
            parent (QAbstractListModel | None): The parent model, if any.
        """
        super().__init__(parent)
        self._projects = []
        self.load_data()

    def load_data(self) -> None:
        """Loads and sorts the projects name list from JSON."""
        self.beginResetModel()
        self._projects: list[str] = json_projects.get_projects_name()
        self._projects.sort(key=lambda proj: proj.lower())
        self._projects = sorted(self._projects,
                                key=lambda v: (v.upper(), v[0].islower()))
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of rows in the model.
        Args:
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            int: The number of projects in the model.
        """
        return len(self._projects)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        """Return the data for the given index and role.
        Args:
            index (QModelIndex): The index for which to retrieve data.
            role (int): The role of the data to retrieve (e.g., DisplayRole).
        Returns:
            QVariant | str: The data for the specified index and role.
        """
        if not index.isValid() or index.row() >= len(self._projects):
            return QVariant()

        if role == Qt.ItemDataRole.DisplayRole:
            return self._projects[index.row()]

        return QVariant()

    def get_value(self, index: int) -> str | None:
        """Get the project name for the specified index.
        Args:
            index (int): The index of the project in the combobox.
        Returns:
            str | None: The project name for the specified index, or None if the index is invalid.
        """
        if 0 <= index < len(self._projects):
            return self._projects[index]
        return None


class ResultsTableModel(QAbstractTableModel):
    """Model for displaying ItemResult data in a QTableView.
    Each row represents an error result entry from a JSON file.
    Attributes:
        _keys (list[str]): List of IDs (keys) for the result items.
        _data (dict[str, ItemResult]): Mapping of ID to result data.
    """

    HEADERS: list[str] = [QCA.translate("column title", "Line Number"),
                          QCA.translate("column title", "Line"),
                          QCA.translate("column title", "Error"),
                          QCA.translate("column title", "Type"),
                          QCA.translate("column title", "Explanation"),
                          QCA.translate("column title", "Suggestion")]

    def __init__(self, project_name: str, file_name: str) -> None:
        """Initialize the ResultsTableModel.
        Args:
            project_name (str): The name of the project for which results are displayed.
            data (dict[str, ItemResult] | None): Initial data to populate the model.
        """
        super().__init__()
        self.project_name: str = project_name
        self.filename: str = file_name
        self._keys: list[str] = []
        if file_name != "":
            self.load_data()

    def load_data(self) -> None:
        """Load the result data into the model from the JSON file.
        """
        if not json_results.is_result_exists(self.project_name, self.filename):
            self.clear_data()
            return
        self.beginResetModel()
        self._data: dict[str, ItemResult] = json_results.get_file_data(self.project_name, self.filename)
        self._keys = list(self._data.keys())
        self.endResetModel()

    def clear_data(self) -> None:
        self.beginResetModel()
        self._data = {}
        self._keys = []
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of rows in the model."""
        return len(self._keys)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of columns in the model."""
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        """Return the data at the given index."""
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return QVariant()

        item_id: str = self._keys[index.row()]
        item: ItemResult = self._data[item_id]

        match index.column():
            case 0: return item["line_number"]
            case 1: return item["line"]
            case 2: return item["error"]
            case 3: return item["error_type"]
            case 4: return item["explanation"]
            case 5: return item["suggestion"]
            case _: return QVariant()

    def data_row(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | ItemResult:
        """Return the data at the given index."""
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return QVariant()

        item_id: str = self._keys[index.row()]
        return self._data[item_id]

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        """Return the header data."""
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()
        if orientation == Qt.Orientation.Horizontal and 0 <= section < len(self.HEADERS):
            return self.HEADERS[section]
        return QVariant()

    def removeRow(self, row: int, parent: QModelIndex = QModelIndex()) -> bool:
        """Remove rows from the model at the specified row index.
        Args:
            row (int): The row index at which to start removing rows.
            count (int): The number of rows to remove.
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            bool: True if the row was successfully removed, False otherwise.
        """

        err_nb: int = json_results.delete_entry(self.project_name, self.filename, self._keys[row])
        if err_nb != 0:
            return False
        self.beginRemoveRows(parent, row, row)
        del self._data[self._keys[row]]
        del self._keys[row]
        self.endRemoveRows()
        return True

    def get_data(self) -> dict[str, ItemResult]:
        """Return the full data."""
        return self._data

    def add_valid_character(self, character: str) -> None:
        """Add the character in the project config
        Delete every error related to this character

        Args:
            character (str): character to add
        """
        json_projects.add_valid_characters(self.project_name, character)
        json_results.delete_specific_error_with_type(self.project_name, self.filename,
                                                     INVALID_CHAR_TEXT_ERROR_TYPE, character)
        self.load_data()

    def remove_banword(self, word: str) -> None:
        """Remove word from the banword list in the project config
        Delete every error related to this banword

        Args:
            word (str): banword to remove
        """
        json_projects.remove_banword(self.project_name, word)
        json_results.delete_specific_error_with_type(self.project_name,
                                                     self.filename,
                                                     BANWORD_TEXT_ERROR_TYPE,
                                                     word)
        self.load_data()

    def add_word_dictionary(self, word: str) -> None:
        """Add word to dictionary in the project config
        Delete every spelling error of this word

        Args:
            word (str): word to add
        """
        json_projects.add_dictionary_word(self.project_name, word)
        json_results.delete_specific_error_with_category(self.project_name, self.filename,
                                                         LANGUAGETOOL_SPELLING_CATEGORY, word)
        self.load_data()

    def add_ignored_rule(self, rule: str) -> None:
        """Add rule to ignored rules in the project config
        Delete every error related to this rule

        Args:
            rule (str): rule to ignore
        """
        json_projects.add_ignored_rules(self.project_name, rule)
        json_results.delete_error_type(self.project_name, self.filename, rule)
        self.load_data()
