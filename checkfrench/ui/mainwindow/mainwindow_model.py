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
from PyQt5.QtCore import QAbstractListModel, QModelIndex, QThread, QVariant, Qt

# -------------------- Import Lib User -------------------
from checkfrench.newtype import ItemProject
from checkfrench.script import json_projects
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
    def __init__(self) -> None:
        """Initialize the MainWindowModel."""
        self.worker_start()
        self.model_start()

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

    def model_start(self) -> None:
        """Initialize the project title combobox model."""
        self.titleCombobBoxModel = ProjectTitleComboBoxModel()

    def get_argument_parser(self, index: int) -> str:
        """Get the argument parser for the selected project in the combobox.
        Args:
            index (int): The index of the selected project in the combobox.
        Returns:
            str: The argument parser for the selected project, or an empty string if not found.
        """
        project_name: str | None = self.titleCombobBoxModel.get_value(index)
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
