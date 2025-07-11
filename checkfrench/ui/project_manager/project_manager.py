"""
File        : project_manager.py
Author      : Silous
Created on  : 2025-05-29
Description : Dialog for managing projects in the application.

This module provides a dialog for managing projects, including creating, deleting, and editing project settings.
"""


# == Imports ==================================================================

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QCloseEvent

# -------------------- Import Lib User -------------------
from checkfrench.newtype import ItemProject
from checkfrench.ui.create_project.create_project import DialogCreateProject
from checkfrench.ui.delete_project.delete_project import DialogDeleteProject
from checkfrench.ui.project_manager.Ui_project_manager import Ui_Dialog_projectManager
from checkfrench.ui.project_manager.project_manager_model import ProjectManagerModel


# == Classes ==================================================================

class DialogProjectManager(QDialog):
    """Dialog for managing projects in the application.
    This dialog allows users to create, delete, and edit project settings.
    Attributes:
        m_model (ProjectManagerModel): The model for managing project data and logic.
    """

    def __init__(self) -> None:
        """Initialize the DialogProjectManager."""
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog_projectManager()

        self.ui.setupUi(self)  # type: ignore
        self.set_up_connect()
        self.set_up_model()

        self.load_project_data(self.ui.comboBox_project.currentIndex())

    def set_up_model(self) -> None:
        """Initialize the model for managing project data."""
        self.m_model = ProjectManagerModel()
        self.ui.comboBox_project.setModel(self.m_model.titleComboBoxModel)
        self.ui.comboBox_language.setModel(self.m_model.languageComboBoxModel)
        self.ui.dataTableView_dictionary.setModel(self.m_model.dictionaryModel)
        self.ui.dataTableView_banwords.setModel(self.m_model.banwordsModel)
        self.ui.dataTableView_ignoredCodes.setModel(self.m_model.codesModel)
        self.ui.dataTableView_rules.setModel(self.m_model.rulesModel)
        self.ui.dataTableView_ignoredSubstrings.setModel(self.m_model.substringsModel)

    def set_up_connect(self) -> None:
        """connect slots and signals"""
        # buttons
        self.ui.pushButton_createProject.clicked.connect(self.pushButton_createProject_clicked)
        self.ui.pushButton_deleteProject.clicked.connect(self.pushButton_deleteProject_clicked)
        self.ui.pushButton_restore.clicked.connect(self.pushButton_restore_clicked)
        self.ui.pushButton_save.clicked.connect(self.pushButton_save_clicked)
        self.ui.pushButton_saveAndQuit.clicked.connect(self.pushButton_saveAndQuit_clicked)
        self.ui.pushButton_validCharacters.clicked.connect(self.pushButton_validCharacters_clicked)

        # comboboxes
        self.ui.comboBox_project.currentIndexChanged.connect(self.comboBox_project_currentIndexChanged)

        # lineEdits
        self.ui.lineEdit_projectName.editingFinished.connect(self.lineEdit_projectName_editingFinished)

    # -------------------- Slots -------------------

    def pushButton_createProject_clicked(self) -> None:
        """Slot when the create project button is clicked.
        Opens a dialog to create a new project."""
        dialog: DialogCreateProject = DialogCreateProject()
        dialog.exec_()
        self.m_model.titleComboBoxModel.load_data()

    def pushButton_deleteProject_clicked(self) -> None:
        """Slot when the delete project button is clicked.
        Opens a dialog to confirm deletion of the selected project."""
        index: int = self.ui.comboBox_project.currentIndex()
        project_name: str | None = self.m_model.titleComboBoxModel.get_value(index)

        if project_name is None:
            return
        dialog: DialogDeleteProject = DialogDeleteProject(project_name)
        dialog.exec_()
        self.m_model.titleComboBoxModel.load_data()
        self.ui.comboBox_project.setCurrentText(project_name)
        self.load_project_data(self.ui.comboBox_project.currentIndex())

    def pushButton_restore_clicked(self) -> None:
        """Slot when the restore button is clicked.
        Reloads the current project data."""
        index: int = self.ui.comboBox_project.currentIndex()
        if index >= 0:
            self.load_project_data(index)

    def pushButton_save_clicked(self) -> None:
        """Slot when the save button is clicked.
        Saves the current project data."""
        project_name: str | None = self.m_model.titleComboBoxModel.get_value(self.ui.comboBox_project.currentIndex())
        if project_name is not None:
            self.save_project_data(project_name)

    def pushButton_saveAndQuit_clicked(self) -> None:
        """Slot when the save and quit button is clicked.
        Saves the current project data and closes the dialog."""
        project_name: str | None = self.m_model.titleComboBoxModel.get_value(self.ui.comboBox_project.currentIndex())
        if project_name is not None:
            self.save_project_data(project_name)
        self.close()

    def pushButton_validCharacters_clicked(self) -> None:
        """Slot when the valid characters button is clicked."""
        pass

    def comboBox_project_currentIndexChanged(self, index: int) -> None:
        """Slot when the project combobox index is changed.
        Loads the project data for the selected project.
        Args:
            index (int): The index of the selected project in the combobox.
        """
        if index < 0:
            return
        self.load_project_data(index)

    def lineEdit_projectName_editingFinished(self) -> None:
        """Slot when the project name line edit editing is finished."""
        pass

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        """Handles the close event of the dialog.
        Args:
            a0 (QCloseEvent | None): The close event, if any.
        """
        self.m_model.worker_stop()
        if a0 is not None:
            a0.accept()

    # -------------------- Methods -------------------

    def load_project_data(self, index: int) -> None:
        """Loads the project data for the selected project index.
        Args:
            index (int): The index of the selected project in the combobox.
        """
        # Get the project name from the combobox model
        project_name: str | None = self.m_model.titleComboBoxModel.get_value(index)

        if project_name is None:
            return
        data: ItemProject | None = self.m_model.get_project_data(project_name)
        if data is None:
            return

        # Set the UI elements with the loaded project data
        self.ui.lineEdit_projectName.setText(project_name)
        self.ui.comboBox_language.setCurrentIndex(
            self.m_model.languageComboBoxModel.get_index_by_code(data["language"]))
        self.ui.lineEdit_argParser.setText(data["arg_parser"])
        self.ui.textEdit_validCharacters.setPlainText(data["valid_characters"])
        self.m_model.dictionaryModel.load_data(data["dictionary"])
        self.m_model.banwordsModel.load_data(data["banwords"])
        self.m_model.codesModel.load_data(data["ignored_codes_into_space"],
                                          data["ignored_codes_into_nothing"])
        self.m_model.substringsModel.load_data(data["ignored_substrings_into_space"],
                                               data["ignored_substrings_into_nothing"])
        self.m_model.rulesModel.load_data(data["ignored_rules"])
        self.ui.lineEdit_synchronizedPath.setText(data["synchronized_path"])

    def save_project_data(self, project_name: str) -> None:
        """Saves the current project data to the model.
        Args:
            project_name (str): The name of the project to save.
        """
        # Prepare the data to be saved
        data: ItemProject = {
            "language": self.m_model.languageComboBoxModel.get_code(self.ui.comboBox_language.currentIndex()),
            "parser": "generic",
            "arg_parser": self.ui.lineEdit_argParser.text(),
            "valid_characters": self.ui.textEdit_validCharacters.toPlainText(),
            "dictionary": self.m_model.dictionaryModel.get_data(),
            "banwords": self.m_model.banwordsModel.get_data(),
            "ignored_codes_into_space": self.m_model.codesModel.get_data()[0],
            "ignored_codes_into_nothing": self.m_model.codesModel.get_data()[1],
            "ignored_substrings_into_space": self.m_model.substringsModel.get_data()[0],
            "ignored_substrings_into_nothing": self.m_model.substringsModel.get_data()[1],
            "ignored_rules": self.m_model.rulesModel.get_data(),
            "synchronized_path": self.ui.lineEdit_synchronizedPath.text()
        }
        # Save the project data using the model
        self.m_model.save_project_data(project_name, data)
