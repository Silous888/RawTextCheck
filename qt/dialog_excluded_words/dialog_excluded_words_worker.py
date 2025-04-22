
from PyQt5.QtCore import QObject, pyqtSignal
from script import process as process


class WorkerDialogExcludedWords(QObject):

    signal_set_list_specific_word_start = pyqtSignal(list)

    signal_set_list_specific_word_finished = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    def set_list_specific_word_thread(self, excluded_words: list[str]) -> None:
        process.set_list_specific_word(excluded_words)
        self.signal_set_list_specific_word_finished.emit()
