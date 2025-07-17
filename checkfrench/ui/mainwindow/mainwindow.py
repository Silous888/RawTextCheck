"""
File        : mainwindow.py
Author      : Silous
Created on  : 2025-04-18
Description : Main window of the application.
"""


# == Imports ==================================================================

# -------------------- Import Lib Tier -------------------
from typing import List
from PyQt5.QtCore import QMimeData, QUrl
from PyQt5.QtGui import QCloseEvent, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QMainWindow

# -------------------- Import Lib User -------------------
from checkfrench.ui.mainwindow.Ui_mainwindow import Ui_MainWindow
from checkfrench.ui.project_manager.project_manager import DialogProjectManager
from checkfrench.ui.mainwindow.mainwindow_model import MainWindowModel


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
        self.m_model.model_stop()
        if a0 is not None:
            a0.accept()

# -------------------- Methods --------------------

    def set_enable_file_valid(self, is_valid: bool) -> None:
        self.ui.pushButton_process.setEnabled(is_valid)
