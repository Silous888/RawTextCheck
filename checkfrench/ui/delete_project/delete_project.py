# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog

# -------------------- Import Lib User -------------------
from checkfrench.script.json_projects import delete_entry
from checkfrench.ui.delete_project.Ui_delete_project import Ui_Dialog_deleteProject


class DialogDeleteProject(QDialog):

    def __init__(self, project_name: str) -> None:
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
        """Handle the creation of a new project."""
        self.delete_project()
        self.close()

    def pushButton_no_clicked(self) -> None:
        """Handle the creation of a new project."""
        self.close()

    # -------------------- Methods -------------------

    def delete_project(self) -> None:
        delete_entry(self.m_project_name)
