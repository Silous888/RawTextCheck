
"""
File        : delete_project.py
Author      : Silous
Created on  : 2025-06-09
Description : Dialog for deleting a project in the application.

This module provides a dialog that prompts the user to confirm the deletion of a project.
"""


# == Imports ==================================================================

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog

# -------------------- Import Lib User -------------------
from checkfrench.script import json_projects
from checkfrench.ui.delete_project.Ui_delete_project import Ui_Dialog_deleteProject


# == Classes ==================================================================

class DialogDeleteProject(QDialog):
    """Dialog for deleting a project.
    This dialog prompts the user to confirm the deletion of a project and handles the deletion logic.
    Attributes:
        m_project_name (str): The name of the project to be deleted.
    """

    def __init__(self, project_name: str) -> None:
        """Initialize the DialogDeleteProject with the project name.
        Args:
            project_name (str): The name of the project to be deleted.
        """
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog_deleteProject()

        self.ui.setupUi(self)  # type: ignore
        self.m_project_name: str = project_name
        self.ui.label_projectName.setText(project_name)

        self.set_up_connect()

    def set_up_connect(self) -> None:
        """Connect slots and signals."""
        # buttons
        self.ui.pushButton_yes.clicked.connect(self.pushButton_yes_clicked)
        self.ui.pushButton_no.clicked.connect(self.pushButton_no_clicked)

    # -------------------- Slots -------------------

    def pushButton_yes_clicked(self) -> None:
        """Slot for the Yes button click."""
        self.delete_project()
        self.close()

    def pushButton_no_clicked(self) -> None:
        """Slot for the No button click."""
        self.close()

    # -------------------- Methods -------------------

    def delete_project(self) -> None:
        """Delete the project with the specified name."""
        json_projects.delete_entry(self.m_project_name)
