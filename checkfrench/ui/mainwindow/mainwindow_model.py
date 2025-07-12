"""
File        : mainwindow_model.py
Author      : Silous
Created on  : 2025-06-15
Description : Model for the main window of the application.

This module defines the model for the main window, including the project title
combobox model and worker thread for background tasks.
"""


# == Imports ==================================================================

# -------------------- Import Lib Tier -------------------
from PyQt5.QtCore import QAbstractListModel, QAbstractTableModel, QModelIndex, QThread, QVariant, Qt

# -------------------- Import Lib User -------------------
from checkfrench.newtype import ItemProject, ItemResult
from checkfrench.script import json_projects, json_results
from checkfrench.ui.mainwindow.mainwindow_worker import WorkerMainWindow


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
        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = WorkerMainWindow()
        self.m_worker.moveToThread(self.m_thread)

    def worker_stop(self) -> None:
        """Stop the worker thread if it is running."""
        if self.m_thread.isRunning():
            self.m_thread.quit()
            self.m_thread.wait()

    def model_start(self, project_name: str, filename: str) -> None:
        """Initialize the project title combobox model."""
        self.titleComboBoxModel = ProjectTitleComboBoxModel()
        self.resultsTableModel = ResultsTableModel(project_name, filename)

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

    HEADERS: list[str] = ["Line Number", "Line", "Error", "Type", "Explanation", "Suggestion"]

    def __init__(self, project_name: str, file_name: str) -> None:
        """Initialize the ResultsTableModel.
        Args:
            project_name (str): The name of the project for which results are displayed.
            data (dict[str, ItemResult] | None): Initial data to populate the model.
        """
        super().__init__()
        self.project_name: str = project_name
        self.file_name: str = file_name
        self._keys: list[str] = []
        if file_name != "":
            self.load_data()

    def load_data(self) -> None:
        """Load the result data into the model from the JSON file.
        """
        self.beginResetModel()
        self._data: dict[str, ItemResult] = json_results.get_file_data(self.project_name, self.file_name + ".json")
        self._keys = list(self._data.keys())
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

        err_nb: int = json_results.delete_entry(self.project_name, self.file_name, self._keys[row])
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
