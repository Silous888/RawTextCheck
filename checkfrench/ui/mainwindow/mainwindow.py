"""functions of the UI"""

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtGui import QCloseEvent

# -------------------- Import Lib User -------------------
from checkfrench.ui.mainwindow.Ui_mainwindow import Ui_MainWindow
from checkfrench.ui.project_manager.project_manager import DialogProjectManager
from checkfrench.ui.mainwindow.mainwindow_worker import WorkerMainWindow


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

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = WorkerMainWindow()
        self.m_worker.moveToThread(self.m_thread)

        self.is_url_correct: bool = False
        self.is_languagetool_available: bool = False

        self.ui.label_sheetOpened.setText("")
        self.ui.label_updateFolder.setText("")

        self.urlsheet_timer = QTimer(self)
        self.urlsheet_timer.setSingleShot(True)
        self.urlsheet_timer.setInterval(1000)

        self.url_type: str = ""  # spreadsheet, folder
        self.folder_process_finished: bool = False

        self.set_up_connect()

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # Menu
        self.ui.actionProjects.triggered.connect(self.actionProjects_triggered)
        # pushButton
        self.ui.pushButton_process.clicked.connect(self.pushbutton_process_clicked)
        # lineEdit
        self.ui.lineEdit_urlSheet.textChanged.connect(self.lineedit_urlsheet_textchanged)
        self.urlsheet_timer.timeout.connect(self.check_urlsheet_access)
        # thread start
        self.m_worker.signal_get_name_sheet_start.connect(self.m_worker.get_name_sheet_thread)
        self.m_worker.signal_languagetool_initialize_start.connect(self.m_worker.languagetool_initialize_thread)
        self.m_worker.signal_language_tool_process_start.connect(self.m_worker.language_tool_process_thread)
        # thread finish
        self.m_worker.signal_languagetool_initialize_finished.connect(self.languagetool_initialize_finished)

    def actionProjects_triggered(self) -> None:
        """slot for actionProjects
        """
        self.dialog_project_manager = DialogProjectManager()
        self.dialog_project_manager.exec()

    def pushbutton_process_clicked(self) -> None:
        """Slot for pushButton_method_2."""
        pass

    def lineedit_urlsheet_textchanged(self) -> None:
        """slot for lineEdit_urlSheet
        """
        self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ui.label_sheetOpened.setText("")
        text: str = self.ui.lineEdit_urlSheet.text()
        self.is_url_correct = False
        if len(text) > 0:
            self.urlsheet_timer.start()

    def check_urlsheet_access(self) -> None:
        """test after some time if url can be accessed"""
        text: str = self.ui.lineEdit_urlSheet.text()
        self.m_worker.signal_get_name_sheet_start.emit(text)

    def languagetool_initialize_finished(self) -> None:
        """slot for signal languagetool_initialize_finished
        """
        self.is_languagetool_available = True
        # self.ui.pushButton_method_2.setEnabled(bool(self.ui.comboBox_game.currentIndex() and self.is_url_correct))

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.urlsheet_timer.stop()
        if self.m_thread.isRunning():
            self.m_thread.quit()
            self.m_thread.wait()
        if a0 is not None:
            a0.accept()
