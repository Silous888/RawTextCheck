# -------------------- Import Lib Tier -------------------
from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt

# -------------------- Import Lib User -------------------
from checkfrench.default_parameters import LANGUAGES_LANGUAGETOOL
from checkfrench.script import json_projects

# ---------------------- Constants ---------------------
DEFAULT_LANGUAGE = "en"


class CreateProjectModel():

    def __init__(self) -> None:
        self.model_start()

    def model_start(self) -> None:
        self.languageComboBoxModel = LanguagesComboBoxModel(LANGUAGES_LANGUAGETOOL)

    def create_project(self, project_name: str, language_code: str) -> None:
        """Create a new project with the given name and language code."""
        if not project_name or not language_code:
            raise ValueError("Project name and language code cannot be empty.")

        json_projects.create_new_entry(project_name, language_code)


class LanguagesComboBoxModel(QAbstractListModel):
    def __init__(self, data: list[tuple[str, str]], parent: QAbstractListModel | None = None) -> None:
        super().__init__(parent)
        self._data: list[tuple[str, str]] = sorted(data, key=lambda x: x[1].lower())

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        if not index.isValid() or not (0 <= index.row() < len(self._data)):
            return QVariant()

        code, label = self._data[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return label
        if role == Qt.ItemDataRole.UserRole:
            return code

        return QVariant()

    def get_code(self, row: int) -> str:
        if 0 <= row < len(self._data):
            return self._data[row][0]
        return ""

    def get_label(self, row: int) -> str:
        if 0 <= row < len(self._data):
            return self._data[row][1]
        return ""

    def get_index_by_code(self, code: str) -> int:
        for i, (c, _) in enumerate(self._data):
            if c == code:
                return i
        return -1

    def get_default_index(self) -> int:
        """Get the default index for the language combo box."""
        return self.get_index_by_code(DEFAULT_LANGUAGE)
