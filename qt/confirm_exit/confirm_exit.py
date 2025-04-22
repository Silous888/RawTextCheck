
# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QCloseEvent

# -------------------- Import Lib User -------------------

from qt.confirm_exit.Ui_confirm_exit import Ui_Dialog

from qt.confirm_exit.confirm_exit_worker import WorkerWidgetConfirmExit


class ConfirmExit(QDialog):

    def __init__(self) -> None:
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  # type: ignore

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = WorkerWidgetConfirmExit()
        self.m_worker.moveToThread(self.m_thread)

        self.set_up_connect()

    def set_up_connect(self) -> None:
        """Set up the signal and slot
        """
        self.ui.pushButton_saveAndQuit.clicked.connect(self.pushbutton_saveandquit_clicked)
        self.ui.pushButton_QuitWithoutSaving.clicked.connect(self.pushbutton_quitwithoutsaving_clicked)
        self.m_worker.signal_save_specific_words_start.connect(self.m_worker.save_specific_words_thread)
        self.m_worker.signal_save_specific_words_finished.connect(self.save_specific_words_finished)

    def pushbutton_saveandquit_clicked(self) -> None:
        """Accept event
        """
        self.ui.pushButton_QuitWithoutSaving.setEnabled(False)
        self.ui.pushButton_saveAndQuit.setEnabled(False)
        self.m_worker.signal_save_specific_words_start.emit()

    def pushbutton_quitwithoutsaving_clicked(self) -> None:
        """Reject event
        """
        self.close()

    def save_specific_words_finished(self) -> None:
        """Save specific words finished
        """
        self.close()

    def closeEvent(self, a0: QCloseEvent) -> None:
        """Close event
        """
        a0.accept()
