# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QCloseEvent

# -------------------- Import Lib User -------------------
from checkfrench.ui.project_manager.Ui_project_manager import Ui_Dialog_projectManager
from checkfrench.ui.project_manager.project_manager_worker import WorkerProjectManager


class DialogProjectManager(QDialog):

    def __init__(self) -> None:
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog_projectManager()
        self.ui.setupUi(self)  # type: ignore

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = WorkerProjectManager()
        self.m_worker.moveToThread(self.m_thread)

        self.set_up_connect()

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        pass

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if self.m_thread.isRunning():
            self.m_thread.quit()
            self.m_thread.wait()
        if a0 is not None:
            a0.accept()
