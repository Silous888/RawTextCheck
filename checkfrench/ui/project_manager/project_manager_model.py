from PyQt5.QtCore import QAbstractListModel, QAbstractTableModel, QModelIndex, QThread, QVariant, Qt


from checkfrench.newtype import Item
from checkfrench.script import json_projects
from checkfrench.ui.project_manager.project_manager_worker import WorkerProjectManager


class ProjectManagerModel():

    def __init__(self) -> None:
        self.worker_start()
        self.model_start()

    def worker_start(self) -> None:
        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = WorkerProjectManager()
        self.m_worker.moveToThread(self.m_thread)

    def worker_stop(self) -> None:
        if self.m_thread.isRunning():
            self.m_thread.quit()
            self.m_thread.wait()

    def model_start(self) -> None:
        self.comboBoxModel = ProjectManagerComboBoxModel()
        self.banwordsModel = ListTableModel()
        self.rulesModel = ListTableModel()

    def get_project_data(self, project_name: str) -> Item | None:
        """Returns the project data from the JSON file."""
        if not project_name:
            return None
        return json_projects.get_project_data(project_name)


class ProjectManagerComboBoxModel(QAbstractListModel):
    """Model for the combobox in the project manager dialog.
    """

    def __init__(self, parent: QAbstractListModel | None = None) -> None:
        super().__init__(parent)
        self._projects = []
        self.load_data()

    def load_data(self):
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


class ListTableModel(QAbstractTableModel):

    def __init__(self, values: list[str] | None = None) -> None:
        super().__init__()
        self._values: list[str] = values if values else []

    def load_data(self, values: list[str] | None = None) -> None:
        self.beginResetModel()
        if values is not None:
            self._values = list(set(values))
        else:
            self._values = []
        self._values.sort(key=lambda word: word.lower())
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._values)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 1  # Only one column

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        if not index.isValid() or role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return QVariant()
        return self._values[index.row()]

    def setData(self, index: QModelIndex, value: str, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False

        new_value: str = str(value).strip()

        if not new_value or new_value in self._values:
            return False  # Reject empty or duplicate values

        self._values[index.row()] = new_value
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags  # type: ignore
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable  # type: ignore

    def insertRows(self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            self._values.insert(row, "")
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            del self._values[row]
        self.endRemoveRows()
        return True

    def get_data(self) -> list[str]:
        # Return only non-empty unique values
        return [word for word in self._values if word.strip()]

    def add_banword(self, word: str) -> bool:
        clean_word: str = word.strip()
        if clean_word and clean_word not in self._values:
            self.beginInsertRows(QModelIndex(), len(self._values), len(self._values))
            self._values.append(clean_word)
            self.endInsertRows()
            return True
        return False
