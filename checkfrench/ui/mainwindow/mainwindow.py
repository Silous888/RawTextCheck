"""
File        : mainwindow.py
Author      : Silous
Created on  : 2025-04-18
Description : Main window of the application.
"""


# == Imports ==================================================================

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QCloseEvent

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

    def set_up_model(self) -> None:
        """Initialize the model for the main window."""
        self.m_model = MainWindowModel(self.ui.comboBox_project.currentText(),
                                       self.ui.label_fileOpened.text())
        self.ui.comboBox_project.setModel(self.m_model.titleComboBoxModel)
        self.ui.tableView_result.setModel(self.m_model.resultsTableModel)

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # Menu
        self.ui.actionProjects.triggered.connect(self.actionProjects_triggered)
        # comboboxes
        self.ui.comboBox_project.currentIndexChanged.connect(self.comboBox_project_currentIndexChanged)

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

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        """Handle the close event of the main window."""
        self.m_model.worker_stop()
        if a0 is not None:
            a0.accept()
