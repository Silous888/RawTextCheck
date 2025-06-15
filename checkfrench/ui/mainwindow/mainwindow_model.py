# -------------------- Import Lib Tier -------------------
from PyQt5.QtCore import QAbstractListModel, QModelIndex, QThread, QVariant, Qt

# -------------------- Import Lib User -------------------
from checkfrench.newtype import ItemProject
from checkfrench.script import json_projects
from checkfrench.ui.mainwindow.mainwindow_worker import WorkerMainWindow


class MainWindowModel():

    def __init__(self) -> None:
        self.worker_start()
        self.model_start()

    def worker_start(self) -> None:
        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = WorkerMainWindow()
        self.m_worker.moveToThread(self.m_thread)

    def worker_stop(self) -> None:
        if self.m_thread.isRunning():
            self.m_thread.quit()
            self.m_thread.wait()

    def model_start(self) -> None:
        self.titleCombobBoxModel = ProjectTitleComboBoxModel()

    def get_argument_parser(self, index: int) -> str:
        project_name: str | None = self.titleCombobBoxModel.get_value(index)
        if project_name is None:
            return ""
        data: ItemProject | None = json_projects.get_project_data(project_name)
        if data is None:
            return ""
        return data["arg_parser"]


class ProjectTitleComboBoxModel(QAbstractListModel):
    """Model for the combobox in the project manager dialog.
    """

    def __init__(self, parent: QAbstractListModel | None = None) -> None:
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
        return len(self._projects)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        if not index.isValid() or index.row() >= len(self._projects):
            return QVariant()

        if role == Qt.ItemDataRole.DisplayRole:
            return self._projects[index.row()]

        return QVariant()

    def get_value(self, index: int) -> str | None:
        if 0 <= index < len(self._projects):
            return self._projects[index]
        return None
