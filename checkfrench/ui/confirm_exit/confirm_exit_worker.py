
from PyQt5.QtCore import QObject, pyqtSignal

# from checkfrench.script import process as process


class WorkerWidgetConfirmExit(QObject):

    signal_save_specific_words_start = pyqtSignal()

    signal_save_specific_words_finished = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    def save_specific_words_thread(self) -> None:
        # process.add_list_specific_word()
        self.signal_save_specific_words_finished.emit()
