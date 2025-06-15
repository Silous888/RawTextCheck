"""functions of the UI"""

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QCloseEvent

# -------------------- Import Lib User -------------------
from checkfrench.ui.mainwindow.Ui_mainwindow import Ui_MainWindow
from checkfrench.ui.project_manager.project_manager import DialogProjectManager
from checkfrench.ui.mainwindow.mainwindow_model import MainWindowModel


# -------------------------------------------------------------------#
#                         CLASS MAINWINDOW                           #
# -------------------------------------------------------------------#
class MainWindow(QMainWindow):
    """main window of the application

    Args:
        QMainWindow (QMainWindow): main window of the application
    """
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore

        self.set_up_connect()
        self.set_up_model()

    def set_up_model(self) -> None:
        self.m_model = MainWindowModel()
        self.ui.comboBox_project.setModel(self.m_model.titleCombobBoxModel)

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # Menu
        self.ui.actionProjects.triggered.connect(self.actionProjects_triggered)
        # comboboxes
        self.ui.comboBox_project.currentIndexChanged.connect(self.comboBox_project_currentIndexChanged)

    def actionProjects_triggered(self) -> None:
        """slot for actionProjects
        """
        self.dialog_project_manager = DialogProjectManager()
        self.dialog_project_manager.exec()

    def comboBox_project_currentIndexChanged(self, index: int) -> None:
        self.ui.lineEdit_argument.setText(self.m_model.get_argument_parser(index))

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.m_model.worker_stop()
        if a0 is not None:
            a0.accept()
