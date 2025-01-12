
# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

# -------------------- Import Lib User -------------------
from qt_files.Ui_dialog_excluded_words import Ui_Dialog
import process


class DialogExcludedWords(QDialog):

    def __init__(self, id_game: int) -> None:
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  # type: ignore
        self.set_up_connect()
        self.id_game: int = id_game

    def load_excluded_word_in_table(self) -> None:
        """load excluded word in the table
        """
        list_excluded_word: list[str] | int = process.get_list_specific_word(sheet_index=self.id_game)
        if isinstance(list_excluded_word, int):
            return
        for word in list_excluded_word:
            self.ui.tableWidget_excludedWords.insertRow(self.ui.tableWidget_excludedWords.rowCount())
            item = QTableWidgetItem(word)
            self.ui.tableWidget_excludedWords.setItem(self.ui.tableWidget_excludedWords.rowCount()-1, 0, item)

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        self.ui.pushButton_resetChange.clicked.connect(self.reset_changes)
        self.ui.pushButton_saveAndQuit.clicked.connect(self.save_and_quit)

    def reset_changes(self) -> None:
        """slot for pushButton_resetChanges
        """
        self.ui.tableWidget_excludedWords.setRowCount(0)
        self.load_excluded_word_in_table()

    def save_and_quit(self) -> None:
        """slot for pushButton_saveAndQuit
        """
