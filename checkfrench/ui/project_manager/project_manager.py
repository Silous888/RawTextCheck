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

        self.set_up_connect()

        self.m_model = ProjectManagerModel()
        self.ui.comboBox_project.setModel(self.m_model.comboBoxModel)

        self.ui.dataTableView_dictionary.setModel(self.m_model.dictionaryModel)
        self.ui.dataTableView_banwords.setModel(self.m_model.banwordsModel)
        self.ui.dataTableView_ignoredCodes.setModel(self.m_model.codesModel)
        self.ui.dataTableView_rules.setModel(self.m_model.rulesModel)

        self.load_project_data(self.ui.comboBox_project.currentIndex())

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
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
        pass

    def pushButton_deleteProject_clicked(self) -> None:
        pass

    def pushButton_restore_clicked(self) -> None:
        """Slot for the restore button click."""
        index: int = self.ui.comboBox_project.currentIndex()
        if index >= 0:
            self.load_project_data(index)

    def pushButton_save_clicked(self) -> None:
        project_name: str | None = self.m_model.comboBoxModel.get_value(self.ui.comboBox_project.currentIndex())
        if project_name is not None:
            self.save_project_data(project_name)

    def pushButton_saveAndQuit_clicked(self) -> None:
        pass

    def pushButton_SearchDictionary_clicked(self) -> None:
        pass

    def pushButton_validCharacters_clicked(self) -> None:
        pass

    def comboBox_project_currentIndexChanged(self, index: int) -> None:
        """Slot for the combobox project index change."""
        if index < 0:
            return
        self.load_project_data(index)

    def lineEdit_projectName_editingFinished(self) -> None:
        pass

    def lineEdit_pathDictionary_editingFinished(self) -> None:
        pass

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.m_model.worker_stop()
        if a0 is not None:
            a0.accept()

    def load_project_data(self, index: int) -> None:
        """Load project data from the model."""

        project_name: str | None = self.m_model.comboBoxModel.get_value(index)

        if project_name is None:
            return
        data: Item | None = self.m_model.get_project_data(project_name)
        if data is None:
            return

        self.ui.lineEdit_projectName.setText(project_name)
        self.ui.lineEdit_argParser.setText(data["arg_parser"])
        self.ui.textEdit_validCharacters.setPlainText(data["valid_characters"])
        self.m_model.dictionaryModel.load_data(data["dictionary"])
        self.m_model.banwordsModel.load_data(data["banwords"])
        self.m_model.codesModel.load_data(data["ignored_codes_into_space"], data["ignored_codes_into_nothing"])
        self.m_model.rulesModel.load_data(data["ignored_rules"])
        self.ui.lineEdit_synchronizedPath.setText(data["synchronized_path"])

    def save_project_data(self, project_name: str) -> None:
        """Save project data to the model."""
        data: Item = {
            "language": "fr",
            "parser": "generic",
            "arg_parser": self.ui.lineEdit_argParser.text(),
            "valid_characters": self.ui.textEdit_validCharacters.toPlainText(),
            "dictionary": self.m_model.dictionaryModel.get_data(),
            "banwords": self.m_model.banwordsModel.get_data(),
            "ignored_codes_into_space": self.m_model.codesModel.get_data()[0],
            "ignored_codes_into_nothing": self.m_model.codesModel.get_data()[1],
            "ignored_substrings_into_space": {},
            "ignored_substrings_into_nothing": {},
            "ignored_rules": self.m_model.rulesModel.get_data(),
            "synchronized_path": self.ui.lineEdit_synchronizedPath.text()
        }
        # Save the data to the model or JSON file
        self.m_model.save_project_data(project_name, data)
