"""
File        : mainwindow.py
Author      : Silous
Created on  : 2025-04-18
Description : Main window of the application.
"""


# == Imports ==================================================================

from typing import List

# -------------------- Import Lib Tier -------------------
from PyQt5.QtCore import QMimeData, QModelIndex, QUrl, QItemSelectionModel
from PyQt5.QtGui import QCloseEvent, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QActionGroup, QFileDialog

# -------------------- Import Lib User -------------------
from rawtextcheck.api import google_sheet_api
from rawtextcheck.default_parameters import (
    INVALID_CHAR_TEXT_ERROR_TYPE,
    BANWORD_TEXT_ERROR_TYPE,
    LANGUAGETOOL_SPELLING_CATEGORY,
    LANGUAGES
)
from rawtextcheck.newtype import ItemResult
from rawtextcheck.script import json_config
from rawtextcheck.ui.mainwindow.mainwindow_model import MainWindowModel
from rawtextcheck.ui.mainwindow.Ui_mainwindow import Ui_MainWindow
from rawtextcheck.ui.project_manager.project_manager import DialogProjectManager


# == Classes ==================================================================

class MainWindow(QMainWindow):
    """Main window of the application.
    This class initializes the main window.
    Attributes:
        m_model (MainWindowModel): The model for the main window, handling data and logic.
    """
    def __init__(self) -> None:
        """Initialize the MainWindow."""
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore

        self.ui.tableView_result.set_columns_hidden_by_default(json_config.load_data()["hidden_column"])
        self.set_up_language_menu()
        self.set_up_model()
        self.set_up_connect()

        self.set_enabled_file_valid(False)
        self.set_enabled_project_has_project(self.ui.comboBox_project.count() > 0)
        self.ui.comboBox_project.setCurrentText(json_config.load_data()["last_project"])
        self.model.resultsTableModel.project_name = self.ui.comboBox_project.currentText()
        self.ui.lineEdit_argument.setText(self.model.get_argument_parser(self.ui.comboBox_project.currentIndex()))

        self.ui.label_fileOpened.setText("")
        self.ui.label_updateResult.hide()

        self.ui.tableView_result.custom_context_actions_requested.connect(self.add_custom_actions_to_menu)

    def set_up_language_menu(self) -> None:
        self.action_language = QAction(self.tr("Language"), self)
        language_menu = QMenu(self.tr("Language"), self)

        self.language_group = QActionGroup(self)
        self.language_group.setExclusive(True)

        default_language_code: str = json_config.load_data()["language"]

        for code, name in LANGUAGES:
            action = QAction(name, self)
            action.setCheckable(True)
            action.setData(code)
            language_menu.addAction(action)  # type: ignore
            self.language_group.addAction(action)

            if code == default_language_code:
                action.setChecked(True)

        self.action_language.setMenu(language_menu)
        self.ui.menuPreference.addAction(self.action_language)  # type: ignore

    def set_up_model(self) -> None:
        """Initialize the model for the main window."""
        self.model = MainWindowModel(self.ui.comboBox_project.currentText(), "")
        self.ui.comboBox_project.setModel(self.model.titleComboBoxModel)
        self.ui.tableView_result.setModel(self.model.resultsTableModel)

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # Menu
        self.ui.actionProjects.triggered.connect(self.actionProjects_triggered)
        self.ui.actionAdd_google_credentials.triggered.connect(self.actionAdd_google_credentials_triggered)
        self.language_group.triggered.connect(self.language_selected)
        # combobox
        self.ui.comboBox_project.currentIndexChanged.connect(self.comboBox_project_currentIndexChanged)
        # lineEdit
        self.ui.lineEdit_filepath.textChanged.connect(self.lineEdit_filepath_textChanged)
        # pushbutton
        self.ui.pushButton_process.clicked.connect(self.pushButton_process_clicked)
        # worker
        self.model.worker.signal_run_process_start.connect(self.model.worker.run_process)
        self.model.worker.signal_run_process_finished.connect(self.run_process_finished)

# -------------------- Slots --------------------

    def actionProjects_triggered(self) -> None:
        """Slot for handling the Projects menu action.
        Opens the project manager dialog."""
        current_project: str = self.ui.comboBox_project.currentText()
        self.dialog_project_manager = DialogProjectManager(current_project)
        self.dialog_project_manager.exec()
        self.model.titleComboBoxModel.load_data()
        self.ui.comboBox_project.setCurrentText(current_project)

    def actionAdd_google_credentials_triggered(self) -> None:
        """Slot for handling the Add Google Credentials menu action.
        Opens a dialog to add Google API credentials."""
        self.add_google_creadentials_process()

    def comboBox_project_currentIndexChanged(self, index: int) -> None:
        """Slot for handling changes in the project combobox.
        Updates the argument line edit with the selected project's argument parser.
        Args:
            index (int): The index of the selected project in the combobox.
        """
        self.ui.lineEdit_argument.setText(self.model.get_argument_parser(index))
        self.model.resultsTableModel.project_name = self.model.titleComboBoxModel.get_value(index) or ""
        self.model.resultsTableModel.load_data()
        self.set_enabled_project_has_project(self.ui.comboBox_project.count() > 0)

    def lineEdit_filepath_textChanged(self) -> None:
        """Slot for handling text changes in the filepath lineEdit
        if the text is a valid filepath, update ui and model
        if not, clear ui and current data
        """
        if self.model.is_file_exist(
            self.ui.comboBox_project.currentText(),
            self.ui.lineEdit_filepath.text()
        ):
            filename: str = self.model.get_filename_from_filepath(self.ui.comboBox_project.currentText(),
                                                                  self.ui.lineEdit_filepath.text())
            self.model.resultsTableModel.filename = filename
            self.ui.label_fileOpened.setText(filename)
            self.model.resultsTableModel.load_data()
            self.set_enabled_file_valid(True)
        else:
            self.model.resultsTableModel.filename = ""
            self.ui.label_fileOpened.setText("")
            self.model.resultsTableModel.clear_data()
            self.set_enabled_file_valid(False)

    def pushButton_process_clicked(self) -> None:
        """Slot when the create project button is clicked.
        """
        project_name: str | None = self.model.titleComboBoxModel.get_value(self.ui.comboBox_project.currentIndex())
        if project_name is None:
            return
        self.set_enabled_during_process(False)
        self.model.worker.signal_run_process_start.emit(
            self.ui.lineEdit_filepath.text(),
            project_name,
            self.ui.lineEdit_argument.text()
            )

    def run_process_finished(self) -> None:
        """Slot when the worker process is finished.
        Updates the model and UI after processing is complete.
        """
        self.set_enabled_during_process(True)
        self.model.resultsTableModel.load_data()

# -------------------- Events --------------------

    def dragEnterEvent(self, a0: QDragEnterEvent | None) -> None:
        """dragEnterEvent override, accept if one file

        Args:
            a0 (QDragEnterEvent | None): drag event
        """
        if a0 is None:
            return
        mime_data: QMimeData | None = a0.mimeData()
        if mime_data is None:
            return
        if mime_data.hasUrls() and len(mime_data.urls()) == 1:
            a0.acceptProposedAction()
        else:
            a0.ignore()

    def dropEvent(self, a0: QDropEvent | None) -> None:
        """dropEvent override, get url of the file and put it
        in lineEdit_filepath text.

        Args:
            a0 (QDragEnterEvent | None): drop event
        """
        if a0 is None:
            return
        mime_data: QMimeData | None = a0.mimeData()
        if mime_data is None:
            return
        if mime_data.hasUrls():
            urls: List[QUrl] = mime_data.urls()
            if not urls:
                return

            self.ui.lineEdit_filepath.setText(urls[0].toLocalFile())

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        """closeEvent override, stop the model

        Args:
            a0 (QDragEnterEvent | None): close event
        """
        json_config.set_last_project(self.ui.comboBox_project.currentText())
        json_config.set_hidden_column(self.ui.tableView_result.get_hidden_columns_labels())
        self.model.model_stop()
        if a0 is not None:
            a0.accept()

# -------------------- Methods --------------------

    def set_enabled_file_valid(self, is_valid: bool) -> None:
        """Enable or disable UI elements based on file validity.
        Args:
            is_valid (bool): True if the file is valid, False otherwise.
        """
        self.ui.pushButton_process.setEnabled(is_valid)

    def set_enabled_project_has_project(self, has_project: bool) -> None:
        """Enable or disable UI elements based on whether a project is selected.
        Args:
            has_project (bool): True if a project is selected, False otherwise.
        """
        self.ui.comboBox_project.setEnabled(has_project)
        self.ui.pushButton_process.setEnabled(has_project)
        self.ui.lineEdit_argument.setEnabled(has_project)
        self.ui.lineEdit_filepath.setEnabled(has_project)
        self.ui.tableView_result.setEnabled(has_project)

    def set_enabled_during_process(self, is_enabled: bool) -> None:
        """Enable or disable UI elements during processing.
        Args:
            is_enabled (bool): True to enable, False to disable.
        """
        self.ui.lineEdit_argument.setEnabled(is_enabled)
        self.ui.comboBox_project.setEnabled(is_enabled)
        self.ui.lineEdit_filepath.setEnabled(is_enabled)
        self.ui.pushButton_process.setEnabled(is_enabled)
        self.ui.tableView_result.setEnabled(is_enabled)
        self.ui.menuManage.setEnabled(is_enabled)
        self.ui.menuPreference.setEnabled(is_enabled)

    def add_google_creadentials_process(self) -> None:

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Select Google Credentials JSON File"),
            "",
            self.tr("JSON Files (*.json)")
        )

        if not filepath:
            return
        credentials: dict[str, str] | None = json_config.load_imported_credentials(filepath)
        if credentials is not None:
            json_config.set_credentials_google(credentials)
            google_sheet_api.set_credentials_info(credentials, reload=True)

    def language_selected(self, action: QAction) -> None:
        selected_code = action.data()
        json_config.set_language(selected_code)

    def add_custom_actions_to_menu(self, menu: QMenu) -> None:
        """Add several actions to contextmenu of table_result

        delete error by word, letter, rule
        add to dictionnary, to valid character, to rules
        "add" actions perform delete error too.
        remove from banlist.
        comparer au texte pour savoir si faute mot, char.

        Args:
            menu (QMenu): menu
        """
        selection_model: QItemSelectionModel | None = self.ui.tableView_result.selectionModel()
        if not (selection_model and selection_model.selectedRows()):
            return
        selected: List[QModelIndex] = selection_model.selectedRows()
        if len(selected) != 1:
            return

        item_result: ItemResult = self.model.resultsTableModel.data_row(selected[0])

        if item_result["error_type"] == INVALID_CHAR_TEXT_ERROR_TYPE:
            action_add_valid_character = QAction(self.tr("Add character to valid characters"), self)
            action_add_valid_character.triggered.connect(lambda _, value=str(item_result["error"]):  # type: ignore
                                                         self.action_add_valid_character_triggered(value))
            menu.addAction(action_add_valid_character)  # type: ignore

        elif item_result["error_type"] == BANWORD_TEXT_ERROR_TYPE:
            action_remove_banword = QAction(self.tr("Remove word from the banword list"), self)
            action_remove_banword.triggered.connect(lambda _, value=str(item_result["error"]):  # type: ignore
                                                    self.action_remove_banword_triggered(value))
            menu.addAction(action_remove_banword)  # type: ignore

        elif item_result["error_issue_type"] == LANGUAGETOOL_SPELLING_CATEGORY:
            action_add_word_dictionary = QAction(self.tr("Add this word to dictionary"), self)
            action_add_word_dictionary.triggered.connect(lambda _, value=str(item_result["error"]):  # type: ignore
                                                         self.action_action_add_word_dictionary_triggered(value))
            menu.addAction(action_add_word_dictionary)  # type: ignore

        else:
            action_add_rules = QAction(self.tr(f"Add {item_result['error_type']} to ignored rules"), self)
            action_add_rules.triggered.connect(lambda _, value=str(item_result["error_type"]):  # type: ignore
                                               self.action_add_rules_triggered(value))
            menu.addAction(action_add_rules)  # type: ignore

    def action_add_valid_character_triggered(self, value: str) -> None:
        """handle characters added to valid characters

        Args:
            value (str): _description_
        """
        self.model.resultsTableModel.add_valid_character(value)

    def action_remove_banword_triggered(self, value: str) -> None:
        """handle removing word from the banword list

        Args:
            value (str): word
        """
        self.model.resultsTableModel.remove_banword(value)

    def action_add_rules_triggered(self, value: str) -> None:
        """Handle adding a new rule to ignored rules

        Args:
            value (str): rule type
        """
        self.model.resultsTableModel.add_ignored_rule(value)

    def action_action_add_word_dictionary_triggered(self, value: str) -> None:
        """Handle adding a word to the dictionary

        Args:
            value (str): word to add
        """
        self.model.resultsTableModel.add_word_dictionary(value)
