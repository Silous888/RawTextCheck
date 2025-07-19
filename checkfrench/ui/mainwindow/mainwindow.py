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
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu

# -------------------- Import Lib User -------------------
from checkfrench.default_parameters import (
    INVALID_CHAR_TEXT_ERROR_TYPE,
    BANWORD_TEXT_ERROR_TYPE,
    LANGUAGETOOL_SPELLING_CATEGORY,
)
from checkfrench.newtype import ItemResult
from checkfrench.script import json_config
from checkfrench.ui.mainwindow.mainwindow_model import MainWindowModel
from checkfrench.ui.mainwindow.Ui_mainwindow import Ui_MainWindow
from checkfrench.ui.project_manager.project_manager import DialogProjectManager


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

        self.set_up_connect()
        self.set_up_model()

        self.set_enable_file_valid(False)
        self.ui.comboBox_project.setCurrentText(json_config.load_data()["last_project"])

        self.ui.tableView_result.custom_context_actions_requested.connect(self.add_custom_actions_to_menu)

    def set_up_model(self) -> None:
        """Initialize the model for the main window."""
        self.m_model = MainWindowModel(self.ui.comboBox_project.currentText(), "")
        self.ui.comboBox_project.setModel(self.m_model.titleComboBoxModel)
        self.ui.tableView_result.setModel(self.m_model.resultsTableModel)

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # Menu
        self.ui.actionProjects.triggered.connect(self.actionProjects_triggered)
        # combobox
        self.ui.comboBox_project.currentIndexChanged.connect(self.comboBox_project_currentIndexChanged)
        # lineEdit
        self.ui.lineEdit_filepath.textChanged.connect(self.lineEdit_filepath_textChanged)
        # pushbutton
        self.ui.pushButton_process.clicked.connect(self.pushButton_process_clicked)

# -------------------- Slots --------------------

    def actionProjects_triggered(self) -> None:
        """Slot for handling the Projects menu action.
        Opens the project manager dialog."""
        self.dialog_project_manager = DialogProjectManager()
        self.dialog_project_manager.exec()
        self.m_model.titleComboBoxModel.load_data()

    def comboBox_project_currentIndexChanged(self, index: int) -> None:
        """Slot for handling changes in the project combobox.
        Updates the argument line edit with the selected project's argument parser.
        Args:
            index (int): The index of the selected project in the combobox.
        """
        self.ui.lineEdit_argument.setText(self.m_model.get_argument_parser(index))
        self.m_model.resultsTableModel.project_name = self.m_model.titleComboBoxModel.get_value(index) or ""
        self.m_model.resultsTableModel.load_data()

    def lineEdit_filepath_textChanged(self) -> None:
        """Slot for handling text changes in the filepath lineEdit
        if the text is a valid filepath, update ui and model
        if not, clear ui and current data
        """
        if self.m_model.is_file_exist(self.ui.lineEdit_filepath.text()):
            filename: str = self.m_model.get_filename_from_filepath(self.ui.lineEdit_filepath.text())
            self.m_model.resultsTableModel.filename = filename
            self.ui.label_fileOpened.setText(filename)
            self.m_model.resultsTableModel.load_data()
            self.set_enable_file_valid(True)
        else:
            self.m_model.resultsTableModel.filename = ""
            self.ui.label_fileOpened.setText("")
            self.m_model.resultsTableModel.clear_data()
            self.set_enable_file_valid(False)

    def pushButton_process_clicked(self) -> None:
        """Slot when the create project button is clicked.
        """
        project_name: str | None = self.m_model.titleComboBoxModel.get_value(self.ui.comboBox_project.currentIndex())
        if project_name is None:
            return
        self.m_model.generate_result(self.ui.lineEdit_filepath.text(),
                                     project_name,
                                     self.ui.lineEdit_argument.text())
        self.m_model.resultsTableModel.load_data()

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
        self.m_model.model_stop()
        if a0 is not None:
            a0.accept()

# -------------------- Methods --------------------

    def set_enable_file_valid(self, is_valid: bool) -> None:
        self.ui.pushButton_process.setEnabled(is_valid)

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

        item_result: ItemResult = self.m_model.resultsTableModel.data_row(selected[0])

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
        self.m_model.resultsTableModel.add_valid_character(value)

    def action_remove_banword_triggered(self, value: str) -> None:
        """handle removing word from the banword list

        Args:
            value (str): word
        """
        self.m_model.resultsTableModel.remove_banword(value)

    def action_add_rules_triggered(self, value: str) -> None:
        """Handle adding a new rule to ignored rules

        Args:
            value (str): rule type
        """
        self.m_model.resultsTableModel.add_ignored_rule(value)

    def action_action_add_word_dictionary_triggered(self, value: str) -> None:
        """Handle adding a word to the dictionary

        Args:
            value (str): word to add
        """
        self.m_model.resultsTableModel.add_word_dictionary(value)
