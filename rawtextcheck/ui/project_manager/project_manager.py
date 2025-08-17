"""
File        : project_manager.py
Author      : Silous
Created on  : 2025-05-29
Description : Dialog for managing projects in the application.

This module provides a dialog for managing projects, including creating, deleting, and editing project settings.
"""


# == Imports ==================================================================

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog, QFileDialog

# -------------------- Import Lib User -------------------
from rawtextcheck.default_parameters import NOBREAK_SPACE, NARROW_NOBREAK_SPACE
from rawtextcheck.newtype import ItemProject
from rawtextcheck.ui.create_project.create_project import DialogCreateProject
from rawtextcheck.ui.delete_project.delete_project import DialogDeleteProject
from rawtextcheck.ui.project_manager.Ui_project_manager import Ui_Dialog_projectManager
from rawtextcheck.ui.project_manager.project_manager_model import ProjectManagerModel


# == Classes ==================================================================

class DialogProjectManager(QDialog):
    """Dialog for managing projects in the application.
    This dialog allows users to create, delete, and edit project settings.
    Attributes:
        m_model (ProjectManagerModel): The model for managing project data and logic.
    """

    def __init__(self, current_project: str) -> None:
        """Initialize the DialogProjectManager."""
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog_projectManager()

        self.ui.setupUi(self)  # type: ignore
        self.set_up_connect()
        self.set_up_model()

        self.load_project_data(self.ui.comboBox_project.currentIndex())

        self.ui.comboBox_project.setCurrentText(current_project)
        self.set_enabled_has_project(self.ui.comboBox_project.count() > 0)

    def set_up_model(self) -> None:
        """Initialize the model for managing project data."""
        self.model = ProjectManagerModel()
        self.ui.comboBox_project.setModel(self.model.titleComboBoxModel)
        self.ui.comboBox_language.setModel(self.model.languageComboBoxModel)
        self.ui.comboBox_parser.setModel(self.model.parserComboBoxModel)
        self.ui.dataTableView_dictionary.setModel(self.model.dictionaryModel)
        self.ui.dataTableView_banwords.setModel(self.model.banwordsModel)
        self.ui.dataTableView_ignoredCodes.setModel(self.model.codesModel)
        self.ui.dataTableView_rules.setModel(self.model.rulesModel)
        self.ui.dataTableView_ignoredSubstrings.setModel(self.model.substringsModel)

    def set_up_connect(self) -> None:
        """connect slots and signals"""
        # buttons
        self.ui.pushButton_createProject.clicked.connect(self.pushButton_createProject_clicked)
        self.ui.pushButton_deleteProject.clicked.connect(self.pushButton_deleteProject_clicked)
        self.ui.pushButton_restore.clicked.connect(self.pushButton_restore_clicked)
        self.ui.pushButton_save.clicked.connect(self.pushButton_save_clicked)
        self.ui.pushButton_saveAndQuit.clicked.connect(self.pushButton_saveAndQuit_clicked)
        self.ui.pushButton_import.clicked.connect(self.pushButton_import_clicked)
        self.ui.pushButton_export.clicked.connect(self.pushButton_export_clicked)
        # comboboxes
        self.ui.comboBox_project.currentIndexChanged.connect(self.comboBox_project_currentIndexChanged)
        self.ui.comboBox_parser.currentIndexChanged.connect(self.comboBox_parser_currentIndexChanged)

    # -------------------- Slots -------------------

    def pushButton_createProject_clicked(self) -> None:
        """Slot when the create project button is clicked.
        Opens a dialog to create a new project."""
        dialog: DialogCreateProject = DialogCreateProject()
        result: int = dialog.exec_()
        if result == QDialog.Accepted:  # type: ignore
            project_name: str = dialog.get_project_name()
            self.model.titleComboBoxModel.load_data()
            self.ui.comboBox_project.setCurrentText(project_name)

    def pushButton_deleteProject_clicked(self) -> None:
        """Slot when the delete project button is clicked.
        Opens a dialog to confirm deletion of the selected project."""
        index: int = self.ui.comboBox_project.currentIndex()
        project_name: str | None = self.model.titleComboBoxModel.get_value(index)

        if project_name is None:
            return
        dialog: DialogDeleteProject = DialogDeleteProject(project_name)
        dialog.exec_()
        self.model.titleComboBoxModel.load_data()
        self.ui.comboBox_project.setCurrentText(project_name)
        self.load_project_data(self.ui.comboBox_project.currentIndex())
        self.set_enabled_has_project(self.ui.comboBox_project.count() > 0)

    def pushButton_restore_clicked(self) -> None:
        """Slot when the restore button is clicked.
        Reloads the current project data."""
        index: int = self.ui.comboBox_project.currentIndex()
        if index >= 0:
            self.load_project_data(index)

    def pushButton_save_clicked(self) -> None:
        """Slot when the save button is clicked.
        Saves the current project data."""
        project_name: str | None = self.model.titleComboBoxModel.get_value(self.ui.comboBox_project.currentIndex())
        if project_name is not None:
            self.save_project_data(project_name)

    def pushButton_saveAndQuit_clicked(self) -> None:
        """Slot when the save and quit button is clicked.
        Saves the current project data and closes the dialog."""
        project_name: str | None = self.model.titleComboBoxModel.get_value(self.ui.comboBox_project.currentIndex())
        if project_name is not None:
            self.save_project_data(project_name)
        self.close()

    def pushButton_import_clicked(self) -> None:
        """Slot when the import button is clicked.
        Opens a file dialog to choose a project file to import."""
        self.import_process(self.ui.comboBox_project.currentText())

    def pushButton_export_clicked(self) -> None:
        """Slot when the export button is clicked.
        Open a window to choose where to save the project export and export it."""
        self.export_process(self.ui.comboBox_project.currentText())

    def comboBox_project_currentIndexChanged(self, index: int) -> None:
        """Slot when the project combobox index is changed.
        Loads the project data for the selected project.
        Args:
            index (int): The index of the selected project in the combobox.
        """
        if index < 0:
            return
        self.load_project_data(index)
        self.set_enabled_has_project(self.ui.comboBox_project.count() > 0)

    def comboBox_parser_currentIndexChanged(self, index: int) -> None:
        """Slot when the parser combobox index is changed.
        Loads the keys of the parser arguments in the lineEdit
        Args:
            index (int): The index of the selected parser in the combobox.
        """
        if index < 0:
            return
        parser_name: str = self.ui.comboBox_parser.currentText()
        self.ui.lineEdit_argParser.setText(self.model.get_default_parser_arg(parser_name))
        return

    # -------------------- Methods -------------------

    def set_enabled_has_project(self, has_project: bool) -> None:
        """Sets the enabled state of UI elements based on whether a project exists.
        Args:
            has_project (bool): True if a project exists, False otherwise.
        """
        self.ui.comboBox_project.setEnabled(has_project)
        self.ui.pushButton_export.setEnabled(has_project)
        self.ui.pushButton_import.setEnabled(has_project)
        self.ui.pushButton_save.setEnabled(has_project)
        self.ui.pushButton_saveAndQuit.setEnabled(has_project)
        self.ui.pushButton_restore.setEnabled(has_project)
        self.ui.comboBox_language.setEnabled(has_project)
        self.ui.comboBox_parser.setEnabled(has_project)
        self.ui.lineEdit_argParser.setEnabled(has_project)
        self.ui.lineEdit_projectName.setEnabled(has_project)
        self.ui.textEdit_validCharacters.setEnabled(has_project)
        self.ui.checkBox_space.setEnabled(has_project)
        self.ui.checkBox_narrowNobreakSpace.setEnabled(has_project)
        self.ui.checkBox_nobreakSpace.setEnabled(has_project)
        self.ui.tabWidget_editArea.setEnabled(has_project)
        self.ui.pushButton_deleteProject.setEnabled(has_project)

    def load_project_data(self, index: int) -> None:
        """Loads the project data for the selected project index.
        Args:
            index (int): The index of the selected project in the combobox.
        """
        # Get the project name from the combobox model
        project_name: str | None = self.model.titleComboBoxModel.get_value(index)

        if project_name is None:
            return
        data: ItemProject | None = self.model.get_project_data(project_name)
        if data is None:
            return

        # Set the UI elements with the loaded project data
        self.ui.lineEdit_projectName.setText(project_name)
        self.ui.comboBox_language.setCurrentIndex(
            self.model.languageComboBoxModel.get_index_by_code(data["language"]))
        self.ui.comboBox_parser.setCurrentText(data["parser"])
        self.ui.lineEdit_argParser.setText(data["arg_parser"])

        # space in checkboxes
        validCharacters: str = data["valid_characters"]

        self.ui.checkBox_space.setChecked(" " in validCharacters)
        self.ui.checkBox_narrowNobreakSpace.setChecked(NARROW_NOBREAK_SPACE in validCharacters)
        self.ui.checkBox_nobreakSpace.setChecked(NOBREAK_SPACE in validCharacters)

        validCharacters = validCharacters.replace(" ", "")
        validCharacters = validCharacters.replace(NARROW_NOBREAK_SPACE, "")
        validCharacters = validCharacters.replace(NOBREAK_SPACE, "")

        self.ui.textEdit_validCharacters.setPlainText(validCharacters)

        self.model.dictionaryModel.load_data(data["dictionary"])
        self.model.banwordsModel.load_data(data["banwords"])
        self.model.codesModel.load_data(data["ignored_codes_into_space"],
                                        data["ignored_codes_into_nothing"])
        self.model.substringsModel.load_data(data["ignored_substrings_into_space"],
                                             data["ignored_substrings_into_nothing"])
        self.model.rulesModel.load_data(data["ignored_rules"])

    def save_project_data(self, project_name: str) -> None:
        """Saves the current project data to the model.
        Args:
            project_name (str): The name of the project to save.
        """
        parser: str | None = self.model.parserComboBoxModel.get_value(self.ui.comboBox_parser.currentIndex())
        if parser is None:
            parser = "textfile"

        validcharacters: str = self.ui.textEdit_validCharacters.toPlainText()
        if self.ui.checkBox_space.isChecked():
            validcharacters = validcharacters + " "
        if self.ui.checkBox_narrowNobreakSpace.isChecked():
            validcharacters = validcharacters + NARROW_NOBREAK_SPACE
        if self.ui.checkBox_nobreakSpace.isChecked():
            validcharacters = validcharacters + NOBREAK_SPACE

        data: ItemProject = {
            "language": self.model.languageComboBoxModel.get_code(self.ui.comboBox_language.currentIndex()),
            "parser": parser,
            "arg_parser": self.ui.lineEdit_argParser.text(),
            "valid_characters": validcharacters,
            "dictionary": self.model.dictionaryModel.get_data(),
            "banwords": self.model.banwordsModel.get_data(),
            "ignored_codes_into_space": self.model.codesModel.get_data()[0],
            "ignored_codes_into_nothing": self.model.codesModel.get_data()[1],
            "ignored_substrings_into_space": self.model.substringsModel.get_data()[0],
            "ignored_substrings_into_nothing": self.model.substringsModel.get_data()[1],
            "ignored_rules": self.model.rulesModel.get_data()
        }
        # Save the project data using the model
        self.model.save_project_data(project_name, data)

        if self.ui.lineEdit_projectName.text() != project_name:
            project_name_new: str = self.ui.lineEdit_projectName.text()
            self.model.rename_project(project_name, project_name_new)
            self.model.titleComboBoxModel.load_data()
            self.ui.comboBox_project.setCurrentText(project_name_new)

    def export_process(self, project_name: str) -> None:
        """Exports the project data to a JSON file.
        Args:
            project_name (str): The name of the project to export.
        """
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Export Project"),
            f"{project_name}.json",
            self.tr("JSON Files (*.json);;All Files (*)")
        )

        if not filepath:
            return  # User cancelled

        self.model.export_project_data(project_name, filepath)

    def import_process(self, project_name: str) -> None:
        """Imports project data from a JSON file.
        Args:
            project_name (str): The name of the project to import data into.
        """
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Import Project"),
            "",
            self.tr("JSON Files (*.json);;All Files (*)")
        )

        if not filepath:
            return
        self.model.import_project_data(project_name, filepath)
        self.load_project_data(self.ui.comboBox_project.currentIndex())
