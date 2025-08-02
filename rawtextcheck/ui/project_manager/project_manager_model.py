"""
File        : project_manager_model.py
Author      : Silous
Created on  : 2025-05-31
Description : Model for managing project data in the project manager dialog.

This module provides the model for comboboxes and table views in the project manager dialog.
It includes models for project titles, languages, dictionaries, banwords, ignored codes, rules,
ignored substrings, and the worker for project management tasks.

"""


# == Imports ==================================================================

# -------------------- Import Lib Tier -------------------
from PyQt5.QtCore import QAbstractListModel, QAbstractTableModel, QModelIndex, QVariant, Qt

# -------------------- Import Lib User -------------------
from rawtextcheck.default_parameters import LANGUAGES_LANGUAGETOOL
from rawtextcheck.newtype import ItemProject
from rawtextcheck.script import json_projects, parser_loader


# == Classes ==================================================================

class ProjectManagerModel():
    """Model for managing project data in the project manager dialog.
    This class initializes the models for comboboxes and table views used in the project manager dialog.
    It also handles the worker thread for project management tasks.
    Attributes:
        m_thread (QThread): The thread for running the project management worker.
        m_worker (WorkerProjectManager): The worker for managing project tasks.
        titleComboBoxModel (ProjectTitleComboBoxModel): Model for the project title combobox.
        languageComboBoxModel (LanguagesComboBoxModel): Model for the language combobox.
        dictionaryModel (ListTableModel): Model for the dictionary table view.
        banwordsModel (ListTableModel): Model for the banwords table view.
        rulesModel (ListTableModel): Model for the ignored rules table view.
        codesModel (IgnoredCodesModel): Model for the ignored codes table view.
        substringsModel (IgnoredSubstringsModel): Model for the ignored substrings table view.
    """

    def __init__(self) -> None:
        """Initialize the ProjectManagerModel."""
        self.model_start()

    def model_start(self) -> None:
        """Initialize the models for comboboxes and table views."""
        self.titleComboBoxModel = ProjectTitleComboBoxModel()
        self.languageComboBoxModel = LanguagesComboBoxModel(LANGUAGES_LANGUAGETOOL)
        self.parserComboBoxModel = ParserComboBoxModel(list(parser_loader.get_all_parsers().keys()))
        self.dictionaryModel = ListTableModel()
        self.banwordsModel = ListTableModel()
        self.rulesModel = ListTableModel()
        self.codesModel = IgnoredCodesModel()
        self.substringsModel = IgnoredSubstringsModel()

    def get_project_data(self, project_name: str) -> ItemProject | None:
        """Retrieves the project data for the given project name.
        Args:
            project_name (str): The name of the project to retrieve data for.
        Returns:
            ItemProject | None: The project data if found, otherwise None.
        """
        if not project_name:
            return None
        return json_projects.get_project_data(project_name)

    def rename_project(self, old_name: str, new_name: str) -> None:
        """Renames a project from old_name to new_name.
        Args:
            old_name (str): The current name of the project.
            new_name (str): The new name for the project.
        """
        if new_name not in json_projects.get_projects_name():
            json_projects.set_new_project_name(old_name, new_name)

    def save_project_data(self, project_name: str, data: ItemProject) -> None:
        """Saves the project data for the given project name.
        Args:
            project_name (str): The name of the project to save data for.
            data (ItemProject): The project data to save.
        """
        if not project_name or not data:
            return
        json_projects.set_entry_from_item(project_name, data)

    def export_project_data(self, project_name: str, filepath: str) -> None:
        """Exports the project data for the given project name to the specified file path.
        Args:
            project_name (str): The name of the project to export.
            filepath (str): The file path where the project data should be exported.
        """
        json_projects.export_project_data(project_name, filepath)

    def import_project_data(self, project_name: str, filepath: str) -> None:
        """Imports project data from the specified file path.
        Args:
            project_name (str): The name of the project to import data into.
            filepath (str): The file path from which to import project data.
        """
        data: ItemProject | None = json_projects.load_imported_project_data(filepath)
        if data:
            self.save_project_data(project_name, data)


class ProjectTitleComboBoxModel(QAbstractListModel):
    """Model for the project title combobox in the project manager dialog.
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
        """Load the project names from the JSON projects file and sort them alphabetically."""
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


class LanguagesComboBoxModel(QAbstractListModel):
    """Model for the languages combobox in the project manager dialog.
    This model provides a list of languages sorted by their labels and allows retrieval of language codes and labels.
    Attributes:
        _data (list[tuple[str, str]]): A list of tuples containing language codes and labels.
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
        """Return the number of rows in the model.
        Args:
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            int: The number of languages in the model.
        """
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
        return "!!!"

    def get_label(self, row: int) -> str:
        """Get the language label for the specified row.
        Args:
            row (int): The row index for which to retrieve the language label.
        Returns:
            str: The language label for the specified row, or an empty string if the row is invalid.
        """
        if 0 <= row < len(self._data):
            return self._data[row][1]
        return "!!!"

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


class ListTableModel(QAbstractTableModel):
    """Model for a list table view in the project manager dialog.
    This model provides a simple list of strings that can be edited and displayed in a table view.
    Attributes:
        _values (list[str]): The list of strings to be displayed in the table view.
    """

    def __init__(self, values: list[str] = []) -> None:
        """Initialize the ListTableModel with the provided values.
        Args:
            values (list[str]): A list of strings to initialize the model with.
        """
        super().__init__()
        values.append("")
        self._values: list[str] = values

    def load_data(self, values: list[str] | None = None) -> None:
        """Load the data into the model.
        Args:
            values (list[str] | None): A list of strings to load into the model.
                                       If None, the model is cleared.
        """
        self.beginResetModel()
        if values is not None:
            self._values = list(set(values))
        else:
            self._values = []
        self._values.sort(key=lambda word: word.lower())
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of rows in the model.
        Args:
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            int: The number of rows in the model, including an empty row at the end.
        """
        return len(self._values) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of columns in the model.
        Args:
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            int: The number of columns in the model, which is always 1.
        """
        return 1

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        """Return the data for the given index and role.
        Args:
            index (QModelIndex): The index for which to retrieve data.
            role (int): The role of the data to retrieve (e.g., DisplayRole, EditRole).
        Returns:
            QVariant | str: The data for the specified index and role.
        """
        if not index.isValid() or index.column() != 0:
            return QVariant()

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if index.row() < len(self._values):
                return self._values[index.row()]
            else:
                return ""  # For the last empty row

        return QVariant()

    def setData(self, index: QModelIndex, value: str, role: int = Qt.ItemDataRole.EditRole) -> bool:
        """Set the data for the given index and role.
        Args:
            index (QModelIndex): The index for which to set data.
            value (str): The value to set for the specified index.
            role (int): The role of the data to set (e.g., EditRole).
        Returns:
            bool: True if the data was set successfully, False otherwise.
        """
        if not index.isValid() or index.column() != 0 or role != Qt.ItemDataRole.EditRole:
            return False

        value = str(value).strip()

        if index.row() < len(self._values):
            self._values[index.row()] = value
        elif index.row() == len(self._values) and value != "":
            self.beginInsertRows(QModelIndex(), len(self._values), len(self._values))
            self._values.append(value)
            self.endInsertRows()
        else:
            return False

        self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Return the flags for the given index.
        Args:
            index (QModelIndex): The index for which to retrieve flags.
        Returns:
            Qt.ItemFlags: The flags for the specified index, allowing editing and selection.
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags  # type: ignore
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable  # type: ignore

    def insertRows(self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        """Insert rows into the model at the specified row index.
        Args:
            row (int): The row index at which to insert new rows.
            count (int): The number of rows to insert.
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            bool: Always True, indicating that the rows were inserted successfully.
        """
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            self._values.insert(row, "")
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        """Remove rows from the model at the specified row index.
        Args:
            row (int): The row index at which to start removing rows.
            count (int): The number of rows to remove.
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            bool: Always True, indicating that the rows were removed successfully.
        """
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            del self._values[row]
        self.endRemoveRows()
        return True

    def get_data(self) -> list[str]:
        """Get the list of values from the model.
        Returns:
            list[str]: A list of non-empty unique values from the model.
        """
        return [word for word in self._values if word.strip()]


class IgnoredCodesModel(QAbstractTableModel):
    """Model for the ignored codes table in the project manager dialog.
    This model provides a table view for managing codes that should be ignored in the project.
    Attributes:
        checkbox_col (int): The index of the checkbox column.
        code_col (int): The index of the code column.
    """

    checkbox_col: int = 0
    code_col: int = 1

    def __init__(self, space_list: list[str] = [], nospace_list: list[str] = []) -> None:
        """Initialize the IgnoredCodesModel with the provided space and nospace lists.
        Args:
            space_list (list[str]): A list of codes that should be replaced with a space.
            nospace_list (list[str]): A list of codes that should not be replaced with a space.
        """
        super().__init__()
        self._data: list[tuple[str, bool]] = (
            [(code, True) for code in space_list] +
            [(code, False) for code in nospace_list]
        )

    def load_data(self, space_list: list[str] | None = None,
                  nospace_list: list[str] | None = None) -> None:
        """Load the data into the model.
        Args:
            space_list (list[str] | None): A list of codes that should be replaced with
                a space. If None, the model is cleared.
            nospace_list (list[str] | None): A list of codes that should not be replaced
                with a space. If None, the model is cleared.
        """
        self.beginResetModel()
        if space_list is not None:
            self._data = [(code, True) for code in space_list if code]
        else:
            self._data = []
        if nospace_list is not None:
            self._data += [(code, False) for code in nospace_list if code]
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of rows in the model.
        Args:
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            int: The number of rows in the model, including an empty row at the end.
        """
        return len(self._data) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of columns in the model.
        Args:
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            int: The number of columns in the model, which is always 2 (checkbox and code).
        """
        return 2

    def data(self, index: QModelIndex,
             role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | Qt.CheckState | str:
        """Return the data for the given index and role.
        Args:
            index (QModelIndex): The index for which to retrieve data.
            role (int): The role of the data to retrieve (e.g., DisplayRole, CheckStateRole).
        Returns:
            QVariant | Qt.CheckState | str: The data for the specified index and role.
        """
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self._data):
            if role == Qt.ItemDataRole.DisplayRole:
                return ""
            if role == Qt.ItemDataRole.CheckStateRole and index.column() == self.checkbox_col:
                return Qt.CheckState.Checked
            return QVariant()

        code, is_space = self._data[index.row()]

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if index.column() == self.code_col:
                return code
        if role == Qt.ItemDataRole.CheckStateRole and index.column() == self.checkbox_col:
            return Qt.CheckState.Checked if is_space else Qt.CheckState.Unchecked

        return QVariant()

    def setData(self, index: QModelIndex, value: str, role: int = Qt.ItemDataRole.EditRole) -> bool:
        """Set the data for the given index and role.
        Args:
            index (QModelIndex): The index for which to set data.
            value (str): The value to set for the specified index.
            role (int): The role of the data to set (e.g., EditRole, CheckStateRole).
        Returns:
            bool: True if the data was set successfully, False otherwise.
        """
        if not index.isValid():
            return False

        row: int = index.row()
        col: int = index.column()

        if row == len(self._data):
            if col == self.code_col and role == Qt.ItemDataRole.EditRole and value:
                self.beginInsertRows(QModelIndex(), row, row)
                self._data.append((value, True))
                self.endInsertRows()
                return True
            return False

        code, is_space = self._data[row]

        if col == self.checkbox_col and role == Qt.ItemDataRole.CheckStateRole:
            self._data[row] = (code, value == Qt.CheckState.Checked)
            self.dataChanged.emit(index, index)
            return True

        if col == self.code_col and role == Qt.ItemDataRole.EditRole:
            self._data[row] = (str(value), is_space)
            self.dataChanged.emit(index, index)
            return True

        return False

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str:
        """Return the header data for the given section and orientation.
        Args:
            section (int): The section index for which to retrieve header data.
            orientation (Qt.Orientation): The orientation of the header (horizontal or vertical).
            role (int): The role of the header data to retrieve (e.g., DisplayRole).
        Returns:
            QVariant | str: The header data for the specified section and orientation.
        """
        labelReplaceWithSpace: str = self.tr("Replace with space")
        labelCode: str = self.tr("Code")
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return labelReplaceWithSpace if section == self.checkbox_col else labelCode
            return str(section + 1)
        return QVariant()

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Return the flags for the given index.
        Args:
            index (QModelIndex): The index for which to retrieve flags.
        Returns:
            Qt.ItemFlags: The flags for the specified index, allowing editing and selection.
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags  # type: ignore
        if index.column() == self.checkbox_col:
            return (
                Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable  # type: ignore
            )
        return (
            Qt.ItemFlag.ItemIsEditable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable  # type: ignore
        )

    def insertRows(self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        """Insert rows into the model at the specified row index.
        Args:
            row (int): The row index at which to insert new rows.
            count (int): The number of rows to insert.
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            bool: Always True, indicating that the rows were inserted successfully.
        """
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            self._data.insert(row, ("", True))
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        """Remove rows from the model at the specified row index.
        Args:
            row (int): The row index at which to start removing rows.
            count (int): The number of rows to remove.
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            bool: Always True, indicating that the rows were removed successfully.
        """
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            if row < len(self._data):
                del self._data[row]
        self.endRemoveRows()
        return True

    def get_data(self) -> tuple[list[str], list[str]]:
        """Returns two lists: one for space codes and one for nospace codes.
        Removes duplicates and empty values.

        Returns:
            tuple[list[str], list[str]]: A tuple containing two lists.
            - The first list is ignored_space.
            - The second list is ignored_nospace.
        """
        space: list[str] = [code for code, is_space in self._data if is_space and code]
        nospace: list[str] = [code for code, is_space in self._data if not is_space and code]
        return space, nospace


class IgnoredSubstringsModel(QAbstractTableModel):
    """Model for the ignored substrings table in the project manager dialog.
    This model provides a table view for managing substrings that should be ignored in the project.
    Attributes:
        check_col (int): The index of the checkbox column.
        start_col (int): The index of the start substring column.
        end_col (int): The index of the end substring column.
    """

    check_col = 0
    start_col = 1
    end_col = 2

    def __init__(self, space_dict: dict[str, list[str]] | None = None,
                 nospace_dict: dict[str, list[str]] | None = None) -> None:
        """Initialize the IgnoredSubstringsModel with the provided space and nospace dictionaries.
        Args:
            space_dict (dict[str, list[str]] | None): A dictionary where keys are start substrings
                and values are lists of end substrings that should be replaced with a space.
            nospace_dict (dict[str, list[str]] | None): A dictionary where keys are
                start substrings and values are lists of end substrings that should not be replaced with a space.
        """
        super().__init__()
        self._data: list[tuple[str, str, bool]] = []
        self.load_data(space_dict or {}, nospace_dict or {})

    def load_data(self, space_dict: dict[str, list[str]], nospace_dict: dict[str, list[str]]) -> None:
        """Load the data into the model from the provided dictionaries.
        Args:
            space_dict (dict[str, list[str]]): A dictionary where keys are start substrings
                and values are lists of end substrings that should be replaced with a space.
            nospace_dict (dict[str, list[str]]): A dictionary where keys are start substrings
                and values are lists of end substrings that should not be replaced with a space.
        """
        self.beginResetModel()
        self._data = [
            (start, end, True)
            for start, ends in space_dict.items()
            for end in ends
        ] + [
            (start, end, False)
            for start, ends in nospace_dict.items()
            for end in ends
        ]
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of rows in the model.
        Args:
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            int: The number of rows in the model, including an empty row at the end.
        """
        return len(self._data) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of columns in the model.
        Args:
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            int: The number of columns in the model, which is always 3 (checkbox, start substring, end substring).
        """
        return 3

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant | str | Qt.CheckState:
        """Return the data for the given index and role.
        Args:
            index (QModelIndex): The index for which to retrieve data.
            role (int): The role of the data to retrieve (e.g., DisplayRole, EditRole, CheckStateRole).
        Returns:
            QVariant | str | Qt.CheckState: The data for the specified index and role.
        """
        if not index.isValid():
            return QVariant()

        row, col = index.row(), index.column()
        is_last: bool = row >= len(self._data)

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if is_last:
                return ""
            start, end, _ = self._data[row]
            if col == self.start_col:
                return start
            if col == self.end_col:
                return end

        if role == Qt.ItemDataRole.CheckStateRole and col == self.check_col:
            if is_last:
                return Qt.CheckState.Checked
            return Qt.CheckState.Checked if self._data[row][2] else Qt.CheckState.Unchecked

        return QVariant()

    def setData(self, index: QModelIndex, value: str, role: int = Qt.ItemDataRole.EditRole) -> bool:
        """Set the data for the given index and role.
        Args:
            index (QModelIndex): The index for which to set data.
            value (str): The value to set for the specified index.
            role (int): The role of the data to set (e.g., EditRole, CheckStateRole).
        Returns:
            bool: True if the data was set successfully, False otherwise.
        """
        if not index.isValid():
            return False

        row, col = index.row(), index.column()

        if row >= len(self._data):
            if col in (self.start_col, self.end_col) and value:
                start: str = value if col == self.start_col else ""
                end: str = value if col == self.end_col else ""
                self.beginInsertRows(QModelIndex(), row, row)
                self._data.append((start, end, True))
                self.endInsertRows()
                return True
            return False

        start, end, is_space = self._data[row]

        if col == self.check_col and role == Qt.ItemDataRole.CheckStateRole:
            self._data[row] = (start, end, value == Qt.CheckState.Checked)
        elif col == self.start_col and role == Qt.ItemDataRole.EditRole:
            self._data[row] = (str(value), end, is_space)
        elif col == self.end_col and role == Qt.ItemDataRole.EditRole:
            self._data[row] = (start, str(value), is_space)
        else:
            return False

        self.dataChanged.emit(index, index)
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Return the flags for the given index.
        Args:
            index (QModelIndex): The index for which to retrieve flags.
        Returns:
            Qt.ItemFlags: The flags for the specified index, allowing editing and selection.
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags  # type: ignore
        if index.column() == self.check_col:
            return (
                Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable  # type: ignore
            )
        return (
            Qt.ItemFlag.ItemIsEditable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable  # type: ignore
        )

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole) -> str | QVariant:
        """Return the header data for the given section and orientation.
        Args:
            section (int): The section index for which to retrieve header data.
            orientation (Qt.Orientation): The orientation of the header (horizontal or vertical).
            role (int): The role of the header data to retrieve (e.g., DisplayRole).
        Returns:
            str | QVariant: The header data for the specified section and orientation.
        """
        labelReplaceWithSpace: str = self.tr("Replace with space")
        labelStart: str = self.tr("Start")
        labelEnd: str = self.tr("End")
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return [labelReplaceWithSpace, labelStart, labelEnd][section]
        return QVariant()

    def insertRows(self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        """Insert rows into the model at the specified row index.
        Args:
            row (int): The row index at which to insert new rows.
            count (int): The number of rows to insert.
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            bool: Always True, indicating that the rows were inserted successfully.
        """
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            self._data.insert(row, ("", "", True))
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        """Remove rows from the model at the specified row index.
        Args:
            row (int): The row index at which to start removing rows.
            count (int): The number of rows to remove.
            parent (QModelIndex): The parent index, not used in this model.
        Returns:
            bool: Always True, indicating that the rows were removed successfully.
        """
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            if row < len(self._data):
                del self._data[row]
        self.endRemoveRows()
        return True

    def get_data(self) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        """Returns two dictionaries: one for space substrings and one for nospace substrings.
        Removes duplicates and empty values.
        Returns:
            tuple[dict[str, list[str]], dict[str, list[str]]]: A tuple containing two dictionaries.
            - The first dictionary is space_dict, where keys are start substrings
              and values are lists of end substrings that should be replaced with a space.
            - The second dictionary is nospace_dict, where keys are start substrings
                and values are lists of end substrings that should not be replaced with a space.
        """
        space_dict: dict[str, list[str]] = {}
        nospace_dict: dict[str, list[str]] = {}
        for start, end, is_space in self._data:
            if not start or not end:
                continue
            target: dict[str, list[str]] = space_dict if is_space else nospace_dict
            if start not in target:
                target[start] = []
            if end not in target[start]:
                target[start].append(end)
        return space_dict, nospace_dict
