# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QCloseEvent

# -------------------- Import Lib User -------------------
from checkfrench.newtype import Item
from checkfrench.ui.project_manager.Ui_project_manager import Ui_Dialog_projectManager
from checkfrench.ui.project_manager.project_manager_model import ProjectManagerModel


class DialogProjectManager(QDialog):

    def __init__(self) -> None:
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog_projectManager()
        self.ui.setupUi(self)  # type: ignore

        self.m_model = ProjectManagerModel()
        self.ui.comboBox_project.setModel(self.m_model.comboBoxModel)
        self.ui.tableView_banwords.setModel(self.m_model.banwordsModel)
        self.ui.tableView_rules.setModel(self.m_model.rulesModel)

        self.set_up_connect()

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # buttons
        self.ui.pushButton_createProject.clicked.connect(self.pushButton_createProject_clicked)
        self.ui.pushButton_deleteProject.clicked.connect(self.pushButton_deleteProject_clicked)
        self.ui.pushButton_save.clicked.connect(self.pushButton_save_clicked)
        self.ui.pushButton_saveAndQuit.clicked.connect(self.pushButton_saveAndQuit_clicked)
        self.ui.pushButton_SearchDictionary.clicked.connect(self.pushButton_SearchDictionary_clicked)
        self.ui.pushButton_validCharacters.clicked.connect(self.pushButton_validCharacters_clicked)

        # comboboxes
        self.ui.comboBox_project.currentIndexChanged.connect(self.comboBox_project_currentIndexChanged)

        # lineEdits
        self.ui.lineEdit_projectName.editingFinished.connect(self.lineEdit_projectName_editingFinished)
        self.ui.lineEdit_pathDictionary.editingFinished.connect(self.lineEdit_pathDictionary_editingFinished)

    # -------------------- Slots -------------------

    def pushButton_createProject_clicked(self) -> None:
        pass

    def pushButton_deleteProject_clicked(self) -> None:
        pass

    def pushButton_save_clicked(self) -> None:

        pass

    def pushButton_saveAndQuit_clicked(self) -> None:
        pass

    def pushButton_SearchDictionary_clicked(self) -> None:
        pass

    def pushButton_validCharacters_clicked(self) -> None:
        pass

    def comboBox_project_currentIndexChanged(self, index: int) -> None:
        project_name: str | None = self.m_model.comboBoxModel.get_value(index)
        if project_name is not None:
            self.load_project_data(project_name)

    def lineEdit_projectName_editingFinished(self) -> None:
        pass

    def lineEdit_pathDictionary_editingFinished(self) -> None:
        pass

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.m_model.worker_stop()
        if a0 is not None:
            a0.accept()

    def load_project_data(self, project_name: str) -> None:
        """Load project data from the model."""
        data: Item | None = self.m_model.get_project_data(project_name)
        if data is None:
            return
        self.ui.lineEdit_projectName.setText(project_name)
        self.ui.lineEdit_specificArgument.setText(data['specific_argument'])
        self.ui.textEdit_validCharacters.setPlainText(data['valid_characters'])
        self.m_model.banwordsModel.load_data(data['banwords'])
        self.ui.lineEdit_pathDictionary.setText(data['path_dictionary'])
        self.m_model.rulesModel.load_data(data['ignored_rules_languagetool'])
