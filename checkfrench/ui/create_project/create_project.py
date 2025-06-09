# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog

# -------------------- Import Lib User -------------------
from checkfrench.ui.create_project.Ui_create_project import Ui_Dialog_createProject
from checkfrench.ui.create_project.create_project_model import CreateProjectModel


class DialogCreateProject(QDialog):

    def __init__(self) -> None:
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog_createProject()

        self.ui.setupUi(self)  # type: ignore
        self.set_up_connect()
        self.set_up_model()

        self.ui.comboBox_language.setCurrentIndex(self.m_model.languageComboBoxModel.get_default_index())

    def set_up_model(self) -> None:
        """Set up the model for the project creation dialog."""
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
        """Handle the creation of a new project."""
        self.create_new_project()
        self.close()

    def lineEdit_projectName_editingFinished(self) -> None:
        pass

    def create_new_project(self) -> None:
        project_name: str = self.ui.lineEdit_projectName.text().strip()
        language_code: str = self.m_model.languageComboBoxModel.get_code(self.ui.comboBox_language.currentIndex())

        if not project_name or not language_code:
            return

        self.m_model.create_project(project_name, language_code)
