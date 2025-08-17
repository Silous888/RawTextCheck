"""
File        : create_project.py
Author      : Silous
Created on  : 2025-06-09
Description : pop-up dialog for creating a new project.

This module defines a dialog for creating a new project, allowing users to specify the project name and language.
"""


# == Imports ==================================================================

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog

# -------------------- Import Lib User -------------------
from rawtextcheck.ui.create_project.Ui_create_project import Ui_Dialog_createProject
from rawtextcheck.ui.create_project.create_project_model import CreateProjectModel


# == Classes ==================================================================

class DialogCreateProject(QDialog):
    """Dialog for creating a new project.
    This dialog allows users to enter a project name and select a language for the new project.
    Attributes:
        m_model (CreateProjectModel): The model for managing project creation data and logic.
    """

    def __init__(self) -> None:
        """Initialize the DialogCreateProject."""
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog_createProject()

        self.ui.setupUi(self)  # type: ignore
        self.set_up_connect()
        self.set_up_model()

        self.ui.comboBox_language.setCurrentIndex(self.model.languageComboBoxModel.get_default_index())
        self.ui.comboBox_parser.setCurrentIndex(self.model.parserComboBoxModel.get_default_index())

        self.ui.pushButton_create.setEnabled(False)

    def set_up_model(self) -> None:
        """Initialize the model for the dialog."""
        self.model = CreateProjectModel()
        self.ui.comboBox_language.setModel(self.model.languageComboBoxModel)
        self.ui.comboBox_parser.setModel(self.model.parserComboBoxModel)

    def set_up_connect(self) -> None:
        """Connect slots and signals."""
        # buttons
        self.ui.pushButton_create.clicked.connect(self.pushButton_create_clicked)
        # lineEdits
        self.ui.lineEdit_projectName.textChanged.connect(self.lineEdit_projectName_textChanged)

    # -------------------- Slots -------------------

    def pushButton_create_clicked(self) -> None:
        """Slot for the create button click."""
        self.create_new_project()
        self.accept()
        self.close()

    def lineEdit_projectName_textChanged(self) -> None:
        """Slot for when the project name line edit text changed"""
        if not self.ui.lineEdit_projectName.text().strip():
            self.ui.pushButton_create.setEnabled(False)
        elif self.model.is_project_name_valid(self.ui.lineEdit_projectName.text()):
            self.ui.pushButton_create.setEnabled(True)
        else:
            self.ui.pushButton_create.setEnabled(False)

    # -------------------- Methods -------------------

    def create_new_project(self) -> None:
        """Create a new project with the specified name and language."""
        project_name: str = self.ui.lineEdit_projectName.text().strip()
        language_code: str = self.model.languageComboBoxModel.get_code(self.ui.comboBox_language.currentIndex())
        parser: str | None = self.model.parserComboBoxModel.get_value(self.ui.comboBox_parser.currentIndex())

        if not parser:
            return

        self.model.create_project(project_name, language_code, parser)

    def get_project_name(self) -> str:
        """get project name of the project created

        Returns:
            str: name of the project
        """
        return self.ui.lineEdit_projectName.text().strip()
