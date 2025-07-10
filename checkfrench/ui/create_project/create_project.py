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
from checkfrench.ui.create_project.Ui_create_project import Ui_Dialog_createProject
from checkfrench.ui.create_project.create_project_model import CreateProjectModel


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

        self.ui.comboBox_language.setCurrentIndex(self.m_model.languageComboBoxModel.get_default_index())

    def set_up_model(self) -> None:
        """Initialize the model for the dialog."""
        self.m_model = CreateProjectModel()
        self.ui.comboBox_language.setModel(self.m_model.languageComboBoxModel)

    def set_up_connect(self) -> None:
        """Connect slots and signals."""
        # buttons
        self.ui.pushButton_create.clicked.connect(self.pushButton_create_clicked)
        # lineEdits
        self.ui.lineEdit_projectName.editingFinished.connect(self.lineEdit_projectName_editingFinished)

    # -------------------- Slots -------------------

    def pushButton_create_clicked(self) -> None:
        """Slot for the create button click."""
        self.create_new_project()
        self.close()

    def lineEdit_projectName_editingFinished(self) -> None:
        """Slot for when the project name line edit finishes editing."""
        pass

    # -------------------- Methods -------------------

    def create_new_project(self) -> None:
        """Create a new project with the specified name and language."""
        project_name: str = self.ui.lineEdit_projectName.text().strip()
        language_code: str = self.m_model.languageComboBoxModel.get_code(self.ui.comboBox_language.currentIndex())

        if not project_name or not language_code:
            return

        self.m_model.create_project(project_name, language_code)
