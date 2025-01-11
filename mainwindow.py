"""functions of the UI"""

import os

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QObject, QThread

# -------------------- Import Lib User -------------------
from Ui_mainwindow import Ui_MainWindow



# -------------------------------------------------------------------#
#                          CLASS WORKER                              #
# -------------------------------------------------------------------#
class _Worker(QObject):

    def __init__(self) -> None:
        super().__init__()


# -------------------------------------------------------------------#
#                         CLASS MAINWINDOW                           #
# -------------------------------------------------------------------#
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = _Worker()
        self.m_worker.moveToThread(self.m_thread)

        self.set_up_connect()

    def set_up_connect(self) -> None:
        pass
